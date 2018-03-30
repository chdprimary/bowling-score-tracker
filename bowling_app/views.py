from django.shortcuts import redirect, render
from bowling_app.models import Game, Frame, Roll

import logging
logging.basicConfig(level=logging.DEBUG, format=' * %(levelname)s - %(message)s')
# Uncomment following line to suppress debug logging to stdout
# logging.disable(logging.DEBUG)

def home_page(request):
    return render(request, 'home.html')

def new_game(request):
    new_game = Game.objects.create()

    new_frame = Frame.objects.create(game=new_game)
    new_frame.frame_id_offset = 0
    new_frame.save()

    new_game.start_frame_id = new_frame.id
    new_game.current_frame_id = new_game.start_frame_id
    new_game.save()

    return add_roll(request, new_game.id)

def view_game(request, game_id):
    game = Game.objects.get(id=game_id)
    return render(request, 'game.html', {'game': game})

def add_roll(request, game_id):
    def _translate_input(roll_value, curr_frame_rolls):
        # Symbol translation
        # If user inputs numeric equivalent of strike or spare, we store 'X' or '/' symbols (to denote unresolved values)
        # expected ValueError occurs on int('X') or int('/')
        ret = roll_value
        try:
            if (num_rolls_in_curr_frame == 0 or num_rolls_in_curr_frame == 1) and roll_value == '10':
                ret = 'X'
            elif num_rolls_in_curr_frame == 1 and int(curr_frame_rolls.first().score) + int(roll_value) == 10:
                ret = '/'
            elif num_rolls_in_curr_frame == 2:
                # This is the fill/final ball, go ahead and resolve value as numeric equivalent (b/c no future compounding possible)
                if roll_value == 'X':
                    ret = '10'
                elif roll_value == '/':
                    ret = str(10 - int(curr_frame_rolls[1].score))
        except ValueError:
            pass
        return ret

    def _is_valid_input(roll_value, curr_frame_rolls):
        VALID_ROLL_SYMBOLS = ['0','1','2','3','4','5','6','7','8','9','10','X','/']
        # User 'roll' input validation
        # Duck typing - expected ValueError occurs on int('X') or int('/')
        # TODO: assuming input is valid by default, should assume invalid by default
        try:
            if roll_value not in VALID_ROLL_SYMBOLS:
                return False
            else:
                is_final_frame = (True if Frame.objects.get(id=game.current_frame_id).frame_id_offset == 9 else False)
                if is_final_frame:
                    logging.debug('_is_valid_input(): is final frame is True')
                    if ((curr_frame_rolls.count() == 0 and roll_value == '/')
                     or (curr_frame_rolls.count() == 1 and roll_value == '/' and (curr_frame_rolls[0].score == 'X' or curr_frame_rolls[0].score == '/'))
                     or (curr_frame_rolls.count() == 1 and roll_value == 'X' and curr_frame_rolls[0].score != 'X')
                     or (curr_frame_rolls.count() == 2 and roll_value == '/' and (curr_frame_rolls[1].score == 'X' or curr_frame_rolls[1].score == '/'))
                     or (curr_frame_rolls.count() == 2 and roll_value == 'X' and curr_frame_rolls[1].score != 'X')
                     or (curr_frame_rolls.count() == 1 and int(curr_frame_rolls[0].score) + int(roll_value) > 10)
                     or (curr_frame_rolls.count() == 2 and int(curr_frame_rolls[1].score) + int(roll_value) > 10)):
                        logging.debug('[*] _is_valid_input(): {} attempted invalid symbol input: {}'.format([r.score for r in curr_frame_rolls], roll_value))
                        return False
                else:
                    if ((curr_frame_rolls.count() == 0 and roll_value == '/')
                     or (curr_frame_rolls.count() == 1 and roll_value == 'X')
                     or (curr_frame_rolls.count() == 1 and int(curr_frame_rolls.first().score) + int(roll_value) > 10)):
                        logging.debug('[*] _is_valid_input(): {} attempted invalid symbol input: {}'.format([r.score for r in curr_frame_rolls], roll_value))
                        return False
        except ValueError:
            pass
        return True

    def _resolve_all_frames(curr_game_frames):
        for frame in curr_game_frames:
            if frame.frame_score == -1:
                # We know that frame score is unresolved because of unresolved symbol
                curr_unresolved_frame_rolls = Roll.objects.filter(frame=frame)
                logging.debug('unresolved_frame_rolls: {}'.format(curr_unresolved_frame_rolls))
                if curr_unresolved_frame_rolls.count() == 3:
                    # 1:strike 2:strike = 20 + fill
                    # 1:strike 2:num1   = 10 + num1 + fill
                    # 1:num1   2:spare  = 10 + fill
                    if curr_unresolved_frame_rolls[0].score == 'X':
                        if curr_unresolved_frame_rolls[1].score == 'X':
                            frame.frame_score = 20 + int(curr_unresolved_frame_rolls[2].score)
                        else:
                            frame.frame_score = 10 + int(curr_unresolved_frame_rolls[1].score) + int(curr_unresolved_frame_rolls[2].score)
                    else:
                        frame.frame_score = 10 + int(curr_unresolved_frame_rolls[2].score)
                    frame.save()
                # TODO: find better method than adding magic number to roll id (fails concurrent games use case)
                elif curr_unresolved_frame_rolls.count() == 2:
                    try:
                        spare_roll = curr_unresolved_frame_rolls.get(score='/')
                        logging.debug('spare roll: {}'.format(spare_roll))
                        resolving_roll = Roll.objects.get(id=spare_roll.id+1)
                        logging.debug('resolving_roll: {}'.format(resolving_roll))
                        # We are likely dealing with an unresolved 'spare' frame
                        frame.frame_score = (20 if resolving_roll.score == 'X' else 10+int(resolving_roll.score))
                        frame.save()
                    except Roll.DoesNotExist:
                        pass
                # TODO: find better method than adding magic number to roll id (fails concurrent games use case)
                elif curr_unresolved_frame_rolls.count() == 1:
                    try:
                        strike_roll = curr_unresolved_frame_rolls.get(score='X')
                        logging.debug('strike roll: {}'.format(strike_roll))
                        resolving_rolls = [Roll.objects.get(id=strike_roll.id+1), Roll.objects.get(id=strike_roll.id+2)]
                        logging.debug('resolving_rolls: {}'.format(resolving_rolls))
                        # We are likely dealing with an unresolved 'strike' frame
                        # 1:strike 2:strike = 30 
                        # 1:strike 2:num1   = 20+num1
                        # 1:num1   2:spare  = 20
                        # 1:num1   2:num2   = 10+num1+num2
                        if resolving_rolls[0].score == 'X':
                            if resolving_rolls[1].score == 'X':
                                frame.frame_score = 30
                            else:
                                frame.frame_score = 20 + int(resolving_rolls[1].score)
                        else:
                            if resolving_rolls[1].score == '/':
                                frame.frame_score = 20
                            else:
                                frame.frame_score = 10 + int(resolving_rolls[0].score) + int(resolving_rolls[1].score)
                        frame.save()
                    except Roll.DoesNotExist:
                        pass

    game = Game.objects.get(id=game_id)
    curr_frame = Frame.objects.get(id=game.current_frame_id)
    curr_frame_rolls = Roll.objects.filter(frame=curr_frame)
    num_rolls_in_curr_frame = curr_frame_rolls.count()

    roll_value = _translate_input(request.POST['roll_char'].upper(), curr_frame_rolls)

    if not _is_valid_input(roll_value, curr_frame_rolls):
        return redirect(f'/games/{game.id}/')

    logging.debug('BEFORE: Game ID: {}'.format(game.id))
    logging.debug('BEFORE: Game.current_frame_id: {}'.format(game.current_frame_id))
    logging.debug('BEFORE: curr_frame_rolls: {}'.format(curr_frame_rolls))

    Roll.objects.create(score=roll_value, frame=curr_frame)

    curr_frame_rolls = Roll.objects.filter(frame=curr_frame)
    # If frame is full, process it and any previous unresolved frames
    if curr_frame_rolls.count() >= 2 or (curr_frame_rolls.count() == 1 and curr_frame_rolls.first().score == 'X'):
        # Update this finished frame's frame_score
        # int('X') and int('/') will raise ValueError, and frame_score will remain at default -1 value to denote 'unresolved'
        try:
            frame_total = sum([int(roll.score) for roll in curr_frame_rolls])
            curr_frame.frame_score = frame_total
            curr_frame.save()
        except ValueError:
            pass

        # Try to resolve all unresolved frames
        curr_game_frames = Frame.objects.filter(game=game.id)
        _resolve_all_frames(curr_game_frames)

        # Update the game's running total
        game.running_total_score = sum([frame.frame_score for frame in curr_game_frames if frame.frame_score >= 0])
        game.save()

        # Check if that was the final (10th) frame
        if curr_game_frames.count() == 10:
            if curr_game_frames.last().frame_score != -1:
                game.finished = True
                game.save()
            return redirect(f'/games/{game.id}/')

        # If it's not game over yet, we add a new frame
        curr_frame = Frame.objects.create(game=game)
        curr_frame.frame_id_offset = curr_frame.id - game.start_frame_id
        curr_frame.save()
        game.current_frame_id = curr_frame.id
        game.save()

    curr_frame_rolls = Roll.objects.filter(frame=curr_frame)
    logging.debug('AFTER: Game ID: {}'.format(game.id))
    logging.debug('AFTER: Game.current_frame_id: {}'.format(game.current_frame_id))
    logging.debug('AFTER: curr_frame_rolls: {}'.format(curr_frame_rolls))

    return redirect(f'/games/{game.id}/')
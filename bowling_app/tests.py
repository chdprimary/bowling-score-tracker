from django.test import TestCase

from bowling_app.models import Game, Frame, Roll

class HomePageTest(TestCase):
    def test_homepage_view_uses_home_template(self):
        response = self.client.get('/')
        self.assertTemplateUsed(response, 'home.html')

class NewGameTest(TestCase):
    # Should change POST to PUT?
    def test_can_save_a_new_game_POST_request(self):
        self.client.post('/games/new', data={'roll_char': '5'})

        self.assertEquals(Frame.objects.count(), 1)
        first_frame = Frame.objects.first()
        self.assertEqual(Roll.objects.count(), 1)
        first_roll = Roll.objects.first()

        self.assertEqual(first_roll.score, '5')
        self.assertEqual(first_roll.frame, first_frame)

    def test_redirects_to_game_score_view_after_POST_request(self):
        response = self.client.post('/games/new', data={'roll_char': '5'})
        new_game = Game.objects.first()
        self.assertRedirects(response, f'/games/{new_game.id}/')

class NewRollTest(TestCase):
    def test_can_save_a_new_roll_POST_request_to_existing_game(self):
        existing_game = Game.objects.create()
        existing_frame = Frame.objects.create(game=existing_game)

        self.client.post(
            f'/games/{existing_game.id}/add_roll',
            data={'roll_char': '3'}
        )

        self.assertEqual(Roll.objects.count(), 1)
        first_roll = Roll.objects.first()
        self.assertEqual(first_roll.score, '3')
        self.assertEqual(first_roll.frame, existing_frame)

    def test_redirects_back_to_game_score_view_after_POST_request(self):
        game = Game.objects.create()
        frame = Frame.objects.create(game=game)

        response = self.client.post(
            f'/games/{game.id}/add_roll',
            data={'roll_char': '4'}
        )

        self.assertRedirects(response, f'/games/{game.id}/')

class GameViewTest(TestCase):
    def test_game_view_uses_game_template(self):
        game = Game.objects.create()
        response = self.client.get(f'/games/{game.id}/')
        self.assertTemplateUsed(response, 'game.html')

    def test_passes_correct_game_to_game_template(self):
        incorrect_game = Game.objects.create()
        correct_game = Game.objects.create()
        response = self.client.get(f'/games/{correct_game.id}/')
        self.assertEqual(response.context['game'], correct_game)

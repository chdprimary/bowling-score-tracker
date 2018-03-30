from django.db import models

class Game(models.Model):
    start_frame_id = models.IntegerField(default=1)
    current_frame_id = models.IntegerField(default=1)
    running_total_score = models.IntegerField(default=0)
    finished = models.BooleanField(default=False)

class Frame(models.Model):
    game = models.ForeignKey(Game, default=None)
    frame_id_offset = models.IntegerField(default=0)
    frame_score = models.IntegerField(default=-1)
    def __str__(self):
        return str(self.id)

class Roll(models.Model):
    frame = models.ForeignKey(Frame, default=None)
    # This will be a digit, 'X', or '/'
    score = models.CharField(max_length=1, default='')
    def __str__(self):
        return 'Frame ID: ' + str(self.frame) + ' Score: ' + str(self.score)
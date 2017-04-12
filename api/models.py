from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Flight(models.Model):
    name = models.CharField(max_length=63, db_index=True)
    year = models.IntegerField(db_index=True)
    ntrp = models.CharField(max_length=31, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    MALE = 1
    FEMALE = 2
    Genders = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    name = models.CharField(max_length=63, db_index=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=31, blank=True, null=True)
    gender = models.IntegerField(choices=Genders, blank=True, null=True)
    users = models.ManyToManyField(User, related_name='players')
    flights = models.ManyToManyField(Flight, related_name='players')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_gender_from_string(cls, gender_str):
        if gender_str.lower() == 'm':
            gender_str = 'male'
        if gender_str.lower() == 'f':
            gender_str = 'female'
        for g in cls.Genders:
            if g[1] == gender_str:
                return g[0]
        return None

    def __str__(self):
        return self.name

class Match(models.Model):
    HOME = 1
    VISITOR = 2
    DBL_DEFAULT = 3
    Winners = (
        (HOME, 'home'),
        (VISITOR, 'visitor'),
        (DBL_DEFAULT, 'double default'),
    )

    flight = models.ForeignKey(Flight, related_name='matches', on_delete=models.CASCADE)
    year = models.IntegerField(db_index=True)
    status = models.CharField(max_length=63, blank=True, null=True)
    home_player = models.ForeignKey(Player, related_name='home_matches', on_delete=models.CASCADE)
    visitor_player = models.ForeignKey(Player, related_name='visitor_matches', on_delete=models.CASCADE)
    score = models.CharField(max_length=63, blank=True, null=True)
    winner = models.IntegerField(choices=Winners, blank=True, null=True)
    scheduled_date = models.DateField(blank=True, null=True)
    played_date = models.DateField(blank=True, null=True)
    entry_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def get_winner_from_string(cls, winner_str):
        for w in cls.Winners:
            if w[1] == winner_str:
                return w[0]
        return None

    def __str__(self):
        return u'{} vs. {}'.format(self.visitor_player, self.home_player)

    def get_loser(self):
        if self.winner == self.HOME:
            return self.visitor_player
        elif self.winner == self.VISITOR:
            return self.home_player
        return None

    def get_parsed_score(self):
        """returns a list of lists corresponding to set scores [[winner_score, loser_score], [ws, ls] ...]"""
        if self.winner == self.HOME or self.winner == self.VISITOR:
            str_scores = re.findall('([0-9]+)-([0-9]+)', self.score)
            scores = [ [int(n) for n in set_score] for set_score in str_scores ]
        else:
            scores = None
        return scores

    def get_winner(self):
        if self.winner == self.HOME:
            return self.home_player
        elif self.winner == self.VISITOR:
            return self.visitor_player
        return None

    def is_retired(self):
        return self.status.strip().lower() == 'retired'

    def player_is_winner(self, player):
        if self.winner == self.HOME:
            return player == self.home_player
        elif self.winner == self.VISITOR:
            return player == self.visitor_player
        return None



from django.db import models
from django.contrib.auth.models import User

class League(models.Model):
    """Used to group all players who signed up for a Round Robin event/season.
    
    This class is used to present a list of players to divide up
    into flights. It also groups those flights together after they are created.
    """
    name = models.CharField(max_length=63, db_index=True)
    # WA Event id
    event_id = models.CharField(max_length=63, db_index=True)
    year = models.IntegerField(db_index=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name    

class Flight(models.Model):
    """Represents a single grouping of players/matches for the Round Robin.
    """
    league = models.ForeignKey(League, related_name='flights', on_delete=models.CASCADE)
    name = models.CharField(max_length=63, db_index=True)
    year = models.IntegerField(db_index=True)
    ntrp = models.CharField(max_length=31, blank=True, null=True)
    start_date = models.DateField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Player(models.Model):
    """Represents a player in a league/flight.

    This holds the contact info for the player and also maps them to flights/matches
    for their leagues. Note that a Player is not a one-to-one mapping with a human.
    There will be a new Player entry for each separate event registration by a User.
    """
    # this is sort of a hack but makes life much easier due to not having to translate.
    MALE = 'male'
    FEMALE = 'female'
    Genders = (
        (MALE, 'male'),
        (FEMALE, 'female'),
    )

    name = models.CharField(max_length=63, db_index=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    phone = models.CharField(max_length=31, blank=True, null=True)
    gender = models.CharField(max_length=31, choices=Genders, blank=True, null=True)
    # player NTRP is the level the user registered for. Doesn't necessarily match Flight ntrp.
    ntrp = models.CharField(max_length=31, blank=True, null=True)
    user = models.ForeignKey(User, related_name='players', on_delete=models.CASCADE)
    flight = models.ForeignKey(Flight, related_name='players', on_delete=models.SET_NULL, blank=True, null=True)
    league = models.ForeignKey(League, related_name='players', on_delete=models.CASCADE, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class Match(models.Model):
    """Represents a single match between two players in the same flight.
    """
    HOME = 'home'
    VISITOR = 'visitor'
    DBL_DEFAULT = 'double default'
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
    winner = models.CharField(max_length=31, choices=Winners, blank=True, null=True)
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

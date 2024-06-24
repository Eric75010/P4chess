import re


class Player:
    """
    Class representing a player.

    :param name: The player's last name.
    :type name: str
    :param firstname: The player's first name.
    :type firstname: str
    :param date_of_birth: The player's date of birth.
    :type date_of_birth: str
    :param id: The player's identifier.
    :type id : str
    :raises valueError: if the id format is invalid.
    """

    def __init__(self, name, firstname, date_of_birth, id):
        if self.validate_id(id):
            self.id = id
        else:
            raise ValueError(
                "Invalid id format,"
                " id must contain 2 letters followed by 5 numbers!"
            )
        self.name = name
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.points = 0
        self.players = []

    def __str__(self):
        """
        Return a string representation of the player.

        :return: Player's name and points.
        :rtype: str
        """
        return f"{self.name} ({self.points} points)"

    def update_points(self, match_result):
        """
        Update the player's points based on match result.

        :param match_result: The result of the match ('win', 'lose', 'draw').
        :type match_result: str
        """
        if match_result == "win":
            self.points += 1
        elif match_result == "lose":
            self.points += 0
        elif match_result == "draw":
            self.points += 0.5

    def validate_id(self, id):
        """
        Validate the format of the player's identifier.

        :param id: The player's identifier.
        :type id: str
        :return: True if the id format is valid,
         False if the id format is not valid.
        :rtype: bool
        """
        # valide le format de l'identifiant
        id_str = str(id)
        return bool(re.match(r"^[A-Z]{2}\d{5}$", id_str))

    def to_dict(self):
        """
        Convert the player object to a dictionary.

        :return: A dictionary representation of the player.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "firtsname": self.firstname,
            "date_of_birht": self.date_of_birth,
            "points": self.points,
        }


class Tournament:
    """
    Class representing a tournament.

    :param tournament_name: The name of the tournament.
    :type tournament_name: str
    :param place: the place of the tournament.
    :type place: str
    :param start_date: The start date of the tournament.
    :type start_date: datetime
    :param end_date: The end date of the tournament.
    :type end_date: datetime
    :param description: The description of the tournament.
    :type description: str
    :param round_number: The number of the rounds.
    :type round_number: int, optional
    """

    def __init__(
        self, tournament_name, place, start_date,
            end_date, description, round_number=4):
        self.tournament_name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.actual_number_round = 1
        self.rounds = []
        self.registered_players = []
        self.description = description
        self.played_matches = []  # stocke les matchs

    def add_round(self, round_instance):
        """
        Add a round to the tournament.

        :param round_instance: The round instance to add.
        :type round_instance: Round
        """
        self.rounds.append(round_instance)

    def create_match(self, player1, player2):
        """
        Create a match between to players.

        :param player1: The first player.
        :type player1: Player
        :param player2: The second player.
        :type player2: Player
        :return: The created match instance.
        :rtype: Match
        """
        match = Match(player1, player2)
        # Créer un match entre deux joueurs
        print(f"Match is created between {player1.name} and {player2.name}")
        return match

    def record_match_result(self, match, winner=None, loser=None, draw=False):
        """
        Record the result of a match.

        :param match: The match instance.
        :type match: Match
        :param winner: The player who won the match, defaults to None.
        :type winner: Player, optional
        :param loser: The player who lost the match, defaults to None.
        :type loser: Player, optional
        :param draw: Indicates if the match was a draw, defaults to False.
        :type draw: bool, optional
        :return: A list of players with their updated points.
        :rtype: list
        """
        self.played_matches.append(match)
        if draw:
            print("Match nul!")
            players = ([match.player1, 0.5], [match.player2, 0.5])
        else:
            if winner and loser:
                print(f"{winner.name} a gagné!")
                players = ([winner, 1], [loser, 0])
        return players


class Match:
    """
    Class representing a match between two players.

    :param player1: The first player.
    :type player1: Player
    :param player2: The second player.
    :type player2: Player
    """

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.result = None


class Round:
    """
    Class representing a round in a tournament.

    :param round_number: The number of the round.
    :type round_number: int
    """

    def __init__(self, round_number):
        self.name = f"Round {round_number}"
        self.matches = []  # Chaque round a une liste de matchs

    def add_match(self, match):
        """
        Add a match to the round.

        :param match: the match instance to add.
        :type match: Match
        """
        self.matches.append(match)

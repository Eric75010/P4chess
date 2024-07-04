import re
class Player:
    """
    Classe représentant un joueur
    """
    def __init__(self, name, firstname, date_of_birth, id):
        """
        Initialise un joueur.

        :param name: Name of the player.
        :type name: str
        :param firstname:  Firstname of the player.
        :type firstname: str
        :param date_of_birth:  Date of birth of the Player.
        :type date_of_birth: str
        :param id: Unique identifier of the player.
        :type id: str
        """
        if self.validate_id(id):
            self.id = id
        else:
            raise ValueError("Invalid id format, id must contain 2 letters followed by 5 numbers!")
        self.name = name
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.points = 0

    def update_points(self, match_result):
        """
        Update the player's points based on the match result.

        :param match_result: Result of the match ('win', 'draw', 'lose').
        :type match_result: str
        """
        if match_result == "win":
            self.points += 1
        elif match_result == "draw":
            self.points += 0.5

    def validate_id(self, id):
        """
        Validate the format of the identifier.

        :param id: Identifier to validate.
        :type id: str
        :return: True if the identifier is valid, otherwise False.
        :rtype: bool
        """
        id_str = str(id)
        return bool(re.match(r'^[A-Z]{2}\d{5}$', id_str))

    def to_json(self):
        """
        Convert the player object to a JSON dictionary.

        :return: Dictionary representing the player.
        :rtype: dict
        """
        return {
            "id": self.id,
            "name": self.name,
            "firstname": self.firstname,
            "date_of_birth": self.date_of_birth,
            "points": self.points
        }

class Tournament:
    """
    Class representing a tournament.
    """
    def __init__(self, tournament_name, place, start_date, end_date, description, round_number=4):
        """
        Initialize a tournament.

        :param tournament_name: Name of the tournament.
        :type tournament_name: str
        :param place: Place of the tournament.
        :type place: str
        :param start_date: Start date of the tournament.
        :type start_date: datetime
        :param end_date: End date of the tournament.
        :type end_date: datetime
        :param description: Description of the tournament.
        :type description: str
        :param round_number: Number of rounds in the tournament.
        :type round_number: int
        """
        self.tournament_name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.actual_number_round = 1
        self.rounds = []
        self.registered_players = []
        self.description = description
        self.played_matches =[] #store the matchs




    def record_match_result(self, match, winner=None, loser=None, draw=False):
        """
        Record the result of a match.

        :param match: Match to record.
        :type match: Match
        :param winner: Winning player, default is None.
        :type winner: Player, optional
        :param loser: Losing player, default is None.
        :type loser: Player, optional
        :param draw: Indicates if the match is a draw,default is False.
        :type draw: bool, optional
        :return: Result of the players.
        :rtype: list
        """
        self.played_matches.append(match)
        if draw:
            print("Match nul!")
            players = ([match.player1, 0.5], [match.player2, 0.5])
        else:
            if winner and loser:
                print(f"{winner.name} a gagné!")
                players = [(winner, 1), (loser, 0)]
        return match.players

    def classement_joueur(self, point):
        """
        Update the player's rank at the end of a mach.

        :param point: Points to be updated.
        :type point: int
        """
        self.point = point

    def add_round(self, round_instance):
        """
        Add a round to the tournament.

        :param round_instance: The round instance to add.
        :type round_instance: Round
        """
        self.rounds.append(round_instance)


    def to_json(self):
        """
        Concert the Tournament object to a JSON dictionary.

        :return: Dictionary representing the tournament.
        :rtype: dict
        """
        return {
            "tournament_name": self.tournament_name,
            "place": self.place,
            "start_date": self.start_date.isoformat(),
            "end_date": self.end_date.isoformat(),
            "round_number": self.round_number,
            "description": self.description,
            "rounds": [round_instance.to_json() for round_instance in self.rounds],
            "registered_players": [player.to_json() for player in self.registered_players],
            "played_matches": [match.to_json() for match in self.played_matches]
        }

class Match:
    """
    Class representing a match.
    """
    def __init__(self, player1, player2):
        """
        Initialize a match between two players.

        :param player1: First player.
        :type player1: Player
        :param player2: Second player.
        :type player2: Player
        """
        self.point = []
        self.player1 = player1
        self.player2 = player2
        self.players = []



    def to_json(self):
        """
        Convert the Match object to a JSON dictionary.

        :return: Dictionary representing the match.
        :rtype: dict
        """
        return {
            "player1": self.player1.to_json(),
            "player2": self.player2.to_json(),
            "result": [
                {"player": result[0].to_json(), "points": result[1]}
                for result in self.players
            ]

        }

class Round:
    """
    Class representing a round in the tournament.
    """
    def __init__(self, tour_number):
        """
        Initialize a round in the tournamnent.

        :param tour_number: Number of the round.
        :type tour_number: int
        """
        self.name = "Round" + str(tour_number)
        self.matches = []

    def create_match(self, player1, player2):
        """
        Create a match between two players.

        :param player1: First player.
        :type player1: Player
        :param player2: Second player.
        :type player2: Player
        :return: Created match.
        :rtype: Match
        """
        match = Match(player1, player2)
        print(f"Match is created between {player1.name} and {player2.name}")
        return match

    def add_match(self, match):
        """
        Add a match to the round.

        :param match: the match instance to add.
        :type match: Match
        """
        self.matches.append(match)



    def to_json(self):
        """
        Convert the Round object to a JSON dictionary.

        :return: Dictionary representing the round.
        :rtype: dict
        """
        return {
            "name": self.name,
            "matches": [
                match.to_json() for match in self.matches
            ]
        }







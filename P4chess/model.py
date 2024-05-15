import re
class Player:
    #Classe représentant un joueur
    def __init__(self, name, firstname, date_of_birth, id):
        #initialise un joueur
        if self.validate_id(id):
            self.id = id
        else:
            raise ValueError("Invalid id format, id must contain 2 letters followed by 5 numbers!")
        self.name = name
        self.firstname = firstname
        self.date_of_birth = date_of_birth
        self.points = 0
        self.players = []

    def update_points(self, match_result):
        if match_result == "win":
            self.points += 1
        elif match_result == "draw":
            self.points += 0.5

    def validate_id(self, id):
        #valide le format de l'identifiant
        id_str = str(id)
        return bool(re.match(r'^[A-Z]{2}\d{5}$', id_str))


class Tournament:
    #Classe représentant un tournoi
    def __init__(self, tournament_name, place, start_date, end_date, description, round_number=4):
        #Initialise un tournoi
        self.tournament_name = tournament_name
        self.place = place
        self.start_date = start_date
        self.end_date = end_date
        self.round_number = round_number
        self.actual_number_round = 1
        self.rounds = []
        self.registered_players = []
        self.description = description
        self.played_matches =[] #stocke les matchs



    def create_match(self, player1, player2):
        match = Match(player1, player2)
        #Créer un match entre deux joueurs
        print(f"Match is created between {player1.name} and {player2.name}")
        return match

    def record_match_result(self, match, winner=None, loser=None, draw=False):
        self.played_matches.append(match)
        if draw:
            print("Match nul!")
            players = ([match.player1, 0.5], [match.player2, 0.5])
        else:
            if winner and loser:
                print(f"{winner.name} a gagné!")
                players = ([winner, 1], [loser, 0])
        return players


    # points fin de match(+1 ou 0)
    def classement_joueur(self, point):
        self.point = point

class Match:
    def __init__(self, player1, player2):
        # ...tuple

        # ([player, score], [player, score])
        self.players = []
        self.point = []
        self.player1 = player1
        self.player2 = player2



# Un tournoi a un nombre de tours défini.
class tournoi:
    def __init__(self, name, place, begining_date, ending_date, number_of_tour="4"):
        return self

    # màj des points et données
    def archive_tournoi(self):
        return self


# Un tournoi a un nombre de tours défini.
class Round:
    def __init__(self, tour_number):
        self.name = "Round" + str(tour_number)
        self.matches = []

    # association dans l'ordre, eviter les matches identiques
    # def association_paire(self)

    # fonction incrémentation tour(Round1, Round2...)
    # def incrémenter_tour(self, tour_number)


# class match..tuple..







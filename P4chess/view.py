# gestion des utilisateurs
# menu principal
from datetime import datetime


class MainView:
    #Vue du menu principal

    def display_menu(self):
        #Affiche le menu principal
        print("Select the option you want")
        print("1 - run tournament")
        print("2 - User management")
        print("3 - Reports")
        print("4 - Leave the program")



    def get_selected_option(self):
        #Récupère l'option sélctionnée par l'utilisateur
        selected_option = input("select an option : ")
        return selected_option

    def display_leave_program_message(self):
    #Affiche un message de confirmation avant de quitter le programme
        print("Are you sure you want to leave the program? (yes/no)")

    def confirm_leave_the_program(self):
        #Demande une confirmation de l'utilisateur pour quitter le programme
        confirmation = input()
        return confirmation.lower() == "yes"

class RunTournamentView:
    #Vue pour la création d'un tournoi

    def display_create_tournament(self):
        #Affiche le formulaire de création d'un tournoi
        while True:
            try:
                tournament_name = input("Enter the name of the tournament: ")
                place = input("Enter the name of the place: ")
                start_date = datetime.strptime(input("Enter the start of the tournament [DD/MM/YYYY] : "), "%d/%m/%Y")
                end_date = datetime.strptime(input("Enter the end of the tournament [DD/MM/YYYY]: "), "%d/%m/%Y")
                round_number = input("Enter the round number [4]: ")
                if round_number == "":
                    round_number = "4"
                description = input("Enter the description of the tournament: ")

                tournament_details = {
                    "name": tournament_name,
                    "place": place,
                    "start date": start_date,
                    "end date": end_date,
                    "round number": round_number,
                    "description": description
                }

                return tournament_details
            except ValueError:
                print("Invalid date format. Please enter the date in the format DD/MM/YYYY.")
    def add_players_to_tournament(self):
        #Ajoute des joueurs à un tournoi
        ids = []
        while True:
            id = input("Enter the player id[if empty continue]: ")
            ids.append(id)
            if id == "":
                break
        return ids



class UserManagementView:
    #Vue de la gestion des utilisateurs

    def display_menu(self):
        #Affiche le menu de gestion des utilisateurs
        print("""
        1 - create player
        2 - update player
        3 - delete player
        4 - go back to main menu
        5 - display players
        """)
    def update_player(self):
        #Demande l'identifiant du joueur à metter à jour
        player_id = input("Enter the id of the player you want to update: ")
        return player_id

    def delete_player(self):
        #Demande l'indentifiant du joueur à supprimer
        player_id = input("Enter the id of the player you wan to delete: ")
        return player_id


class LeaveTheProgram:

    def display_leave_the_program(self):

        print(""""
        1 - leave tournament
        """)




class ReportView:
    # liste de tous les joueurs par ordre alphabétique,liste de tous les tournois, nom et dates d’un tournoi donné, liste des joueurs du tournoi par ordre alphabétique,
    def __init__(self, tournaments):
        self.tournaments = tournaments

    def display_report_submenu(self):
        #Affiche le menu pour les rapports
        print("""
        1 - List of all players by alphabetical order
        2 - List of all tournaments
        3 - Details of a specific tournament
        4 - List of players in a specific tournament
        5 - List of all rounds and matches in a specific tournament
        """)


    def display_players_by_alphabetical_order(self, tournament_name):
        #TODO lire json plutôt que les joueurs du tournoi
        #tri des joueurs par le nom, ordre alaphabétique
        all_players = [player for tournament in self.tournaments for player in tournament.players]
        sorted_players = sorted(all_players, key=lambda p: p.name)
        print(sorted_players)
        print("List of players by alphabetical order:")
        for player in sorted_players:
            print(f"{player.name}, {player.firstname}, {player.date_of_birth}")

    def display_all_tournaments(self):
        #Afficher la liste des tournois
        print("list of all tournamnents:")
        for tournament in self.tournaments:
            print(f"{tournament.tournament_name} - {tournament.start_date} to {tournament.end_date}")

    def display_tournament_info(self, tournament_name):
        #Recherche du tournoi par le nom
        found_tournament = next((t for t in self.tournaments if t.tournament_name == tournament_name), None)
        print(self.tournaments)
        if found_tournament:
            print(f"Tournament: {found_tournament.tournament_name}")
            print(f"Start Date : {found_tournament.start_date}")
            print(f"End Date: {found_tournament.end_date}")
        else:
            print("Tournament not found!")


    def display_tournament_players_by_alphabetical_order(self, tournament_name):
        #TODO créer sous menu
        #Recherche par nom
        found_tournament = next((t for t in self.tournaments if t.tournament_name == tournament_name), None)
        if found_tournament:
            sorted_players = sorted(found_tournament.registered_players, key=lambda p: p.name)

            print(f"List of players in tournament {tournament_name} by aplphabetical order:")
            for player in sorted_players:
                print(f"{player.name}, {player.firstname}, {player.date_of_birth}")
        else:
            print("Tournament not found!")


    def display_tournament_rounds_and_matches(self, tournament_name):
        #Recherche par nom
        found_tournament = next((t for t in self.tournaments if t.tournament_name == tournament_name), None)
        if found_tournament:
            print(f"Rounds and matches for tournament {tournament_name}:")
            for round_number, matches in enumerate(found_tournament.rounds, start=1):
                print(f"Round {round_number}:")
                for match in matches:
                    print(f" Match: {match['player1'].name} /  {match['player2'].name}")
        else:
            print("Tournament not found!")









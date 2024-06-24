from datetime import datetime


class MainView:
    """
    View for the main menu.
    """

    def display_menu(self):
        """
        Display the menu options.
        """
        print("Select the option you want")
        print("1 - run tournament")
        print("2 - User management")
        print("3 - Reports")
        print("4 - Leave the program")

    def get_selected_option(self):
        """
        Get the option selected by user.

        :return: The selected option.
        :rtype: str
        """
        selected_option = input("select an option : ")
        return selected_option

    def display_leave_program_message(self):
        """
        Display a confirmation message before leaving the program.
        """
        print("Are you sure you want to leave the program? (yes/no)")

    def confirm_leave_the_program(self):
        """
        Ask for user confirmation to leave the program.

        :return: True if the user confirms, False otherwise.
        :rtype: bool
        """
        confirmation = input()
        return confirmation.lower() == "yes"


class RunTournamentView:
    """
    View for creating a tournament.
    """
    def display_create_tournament(self):
        """
        Display the form to create a tournament and add the details.

        :return: A dictionary with the tournament details.
        :rtype: dict
        """
        tournament_name = input("Enter the name of the tournament: ")
        place = input("Enter the name of the place: ")
        start_date = self.display_date_input("start")
        end_date = self.display_date_input("end")

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
            "description": description,
        }

        return tournament_details

    def display_date_input(self, date_text):
        """
        Prompt the user to input a date with a specific format.

        :param date_text: The context of the date
        :type date_text: str
        :return: The date input.
        :rtype: datetime
        """
        while True:
            try:
                date_input = datetime.strptime(
                    input(
                        "Enter the "
                        + date_text
                        + " date of the tournament [DD/MM/YYYY] : "
                    ),
                    "%d/%m/%Y",
                )
                return date_input
            except ValueError:
                print(
                    "Invalid "
                    + date_text
                    + " date format."
                      " Please enter the date in the format DD/MM/YYYY."
                )

    def add_players_to_tournament(self):
        """
        Add players to a tournament by gathering their IDs.

        :return: A list of player IDs.
        :rtype: list
        """
        # Ajoute des joueurs à un tournoi
        ids = []
        while True:
            id = input("Enter the player id[if empty continue]: ")
            if id == "":
                break
            ids.append(id)
        return ids


class UserManagementView:
    """
    View for user management.
    """
    def display_menu(self):
        """
        Display the user management menu options.
        """
        print(
            """
        1 - create player
        2 - update player
        3 - delete player
        4 - go back to main menu
        5 - display players
        """
        )

    def update_player(self):
        """
        Prompt the user to input the ID of the player to update.

        :return: The ID of the player to update.
        :rtype: str
        """
        player_id = input("Enter the id of the player you want to update: ")
        return player_id

    def delete_player(self):
        """
        Prompt the user the ID of the player to delete.

        :return: The ID of the player to delete.
        :rtype: str
        """
        player_id = input("Enter the id of the player you wan to delete: ")
        return player_id


class ReportView:
    """
    View for displaying reports.
    """

    def __init__(self):
        self.tournaments = None

    def display_report_submenu(self):
        """
        Display the submenu for report options.
        """
        print(
            """
        1 - List of all players by alphabetical order
        2 - List of all tournaments
        3 - Details of a specific tournament
        4 - List of players in a specific tournament
        5 - List of all rounds and matches in a specific tournament
        """
        )

    def display_all_players_by_alphabetical_order(self, sorted_players):
        """
        Display all players sorted by alphabetical order.

        :param sorted_players: A list of sorted player objects.
        :rtype sorted_players: list
        """
        print("List of players by alphabetical order:")
        for player in sorted_players:
            print(f"{player.name}, {player.firstname}, {player.date_of_birth}")

    def display_all_tournaments(self, tournaments):
        """
        Display the list of all tournaments.

        :param tournaments: A list of tournament objects.
        :type tournaments: list
        """
        print("list of all tournamnents:")
        for tournament in tournaments:
            print(
                f"Tournament Name: {tournament.tournament_name},"
                f" Place: {tournament.place},"
                f" Start Date: {tournament.start_date},"
                f" End Date: {tournament.end_date},"
                f" Description: {tournament.description}"
            )

    def display_tournament_info(self, tournament_name):
        """
        Display the details of a specific tournament.

        :param tournament_name:
         The name of the tournament.
        :type tournament_name: str
        """
        found_tournament = next(
            (t for t in self.tournaments
             if t.tournament_name == tournament_name), None
        )
        if found_tournament:
            print(f"Tournament: {found_tournament.tournament_name}")
            print(f"Start Date : {found_tournament.start_date}")
            print(f"End Date: {found_tournament.end_date}")
            print(f"Place: {found_tournament.place}")
            print(f"Description: {found_tournament.description}")

    def display_tournament_players_by_alphabetical_order(self, sorted_players):
        """
        Display the players of a specific tournament
         sorted by alphabetical order.

        :param sorted_players: A list of sorted player objects.
        :type sorted_players: list
        """
        print("Liste des joueurs par ordre alphabétique:")
        for player in sorted_players:
            print(f"{player.name}, {player.firstname}, {player.date_of_birth}")

    def display_tournament_rounds_and_matches(self, tournament):
        """
        Display the rounds and matches of a specific tournament

        :param tournament: The tournament object.
        :type tournament: Tournament
        """
        print(f"Rounds and matches for tournament"
              f" {tournament.tournament_name}:")
        for round_instance in tournament.rounds:
            print(f"Round {round_instance.name}:")
            for match in round_instance.matches:
                print(f" Match: {match.player1.name} vs {match.player2.name}")

    def display_tournament_not_found(self):
        """
        Display a message indicating that the tournament was not found.
        """
        print("Tournament not found!")

import json

from PlayerView import PlayerView
from controller import RunTournamentController, Controller
from model import Player
from view import MainView, RunTournamentView


def load_players():
    """
    Load players from a JSON file.

    :return: A list of Player objects.
    :rtype: list
    """
    with open("players.json", "r") as file:
        player_data = json.load(file)
    players = []
    for player in player_data:
        players.append(
            Player(
                player["name"],
                player["firstname"],
                player["date_of_birth"],
                player["id"],
            )
        )
    return players


def main():
    """
    Main function to run the application.

    """
    controller = Controller()
    controller.run()
    main_view = MainView()
    run_tournament_view = RunTournamentView()
    player_view = PlayerView()

    players = load_players()

    tournament_controller = RunTournamentController(
        run_tournament_view, player_view)
    tournament_controller.players = players

    while True:
        main_view.display_menu()
        option = main_view.get_selected_option()

        if option == "1":
            tournament_controller.create_tournament()
        elif option == "2":
            controller.user_management()
        elif option == "3":
            controller.reports()
        elif option == "4":
            main_view.display_leave_program_message()
            if main_view.confirm_leave_the_program():
                break
        else:
            print("Invalid option. Please try again.")


if __name__ == "__main__":
    main()

import datetime


class PlayerView:
    """
    View for player management.
    """

    def ask_id(self):
        """
        Prompt the user to input the player's identifier.

        :return: The player's identifier.
        :rtype: str
        """
        return input("What is your id (AA11111)? : ")

    def ask_name(self):
        """
        Prompt the user to input the player's last name.

        :return: The player's last name.
        :rtype: str
        """
        return input("What is your name ? : ")

    def ask_firstname(self):
        """
        Prompt the user to input the player's first name.

        :return: The player's first name.
        :rtype: str
        """
        return input("What is your firstname ? : ")

    def ask_date_of_birth(self):
        """
        Prompt the user to input his  date of birth with a specific format.

        :param date_text: The date of birth
        :type date_text: str
        :return: The date input.
        :rtype: datetime
        """
        while True:
            date_text = input("Enter player date of birth [DDMMYYYY] : ")
            date_of_birth_checked = self.validate_date_of_birth(date_text)
            if date_of_birth_checked:
                return date_of_birth_checked.strftime("%m/%d/%Y")
            else:
                print("Invalid date."
                      "Please enter a valid date in the format DDMMYYYY.")

    def validate_date_of_birth(self, date_text):
        try:
            return datetime.datetime.strptime(date_text, "%d%m%Y")
        except ValueError:
            return False

    def display_player(self, name, firstname, date_of_birth):
        """
        Display the player's information.

        :param name: The player's last name.
        :type name: str
        :param firstname: the player's first name.
        :type firstname: str
        :param date_of_birth: The player's date of birth.
        :type date_of_birth: datetime
        """
        print(f"The player is {name} {firstname} {date_of_birth}.")

    def display_players(self, players):
        """
        Display the list of available players.

        :param players: A list of player objects.
        :type players: list
        """
        print("Available players:")
        for player in players:
            print(
                f"ID: {player.id},"
                f" Name: {player.name},"
                f" Firstname: {player.firstname},"
                f" Date of birth: {player.date_of_birth}")

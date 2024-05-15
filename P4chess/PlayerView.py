class PlayerView:
    #Vue de la gestion des joueurs
    def ask_id(self):
        #Demande l'identifiant du joueur
        return input("What is your id (AA11111)? : ")
    def ask_name(self):
        #Demande le nom du joueur
        return input("What is your name ? : ")


    def ask_firstname(self):
        #Demande le prénom du joueur
        return input("What is your firstname ? : ")

    def ask_date_of_birth(self):
        #Demande la date de naissance du joueur
        return input("What is your date of birth ? : ")


    def display_player(self,name, firstname, date_of_birth):
        #Affiche un joueur
        print(f"The player is {name} {firstname} {date_of_birth}.")


# Name: David Lee
# Purpose: The purpose of this program is to pull data from sql server and
# store relevant information in specialized class. The information in each
# object is then displayed to the user through an interactive menu.


import pymysql.cursors
from creds import *
from pets import Pet


def menu():
    exit_cond = False
    print("Welcome to the Pet Chooser!")
    while not exit_cond:
        try:
            i = 1
            print("Please choose a pet from the list below:")
            for pet in pets_list:
                print(f"[{i}] {pet.GetPetName()}")
                i += 1
            print("[Q] Quit")

            user_input = input("Choice: ")
            if user_input == "q" or user_input == "Q":
                print("Exiting the Pet Chooser...")
                exit_cond = True
            elif not user_input.isnumeric():
                print("You did not enter in a valid number. Please choose again.")
                input("Press [ENTER] to continue.")
            elif int(user_input) <= 0 or int(user_input) > i-1:
                print(f"Please enter in a number between 1 and {i-1}")
                input("Press [ENTER] to continue.")
            else:
                printPet(pets_list[int(user_input)-1])

        except Exception as e:
            raise e


def printPet(chosen_pet: Pet):
        print(f"You have chosen {chosen_pet.GetPetName()}, the {chosen_pet.GetType()}. "
              f"{chosen_pet.GetPetName()} is {chosen_pet.GetPetAge()} years old. "
              f"{chosen_pet.GetPetName()}'s owner is {chosen_pet.GetOwnerName()}.\n")
        input("Press [ENTER] to continue. ")


# Connect to the database
try:
    myConnection = pymysql.connect(host=hostname,
                                   user=username,
                                   password=password,
                                   db=database,
                                   charset='utf8mb4',
                                   cursorclass=pymysql.cursors.DictCursor)

except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print()
    exit()

# Now that we are connected, execute a query
#  and do something with the result set.
try:
    with myConnection.cursor() as cursor:
        # ==================

        # Create list holding each pet object
        pets_list = []

        sqlSelect = """select pets.id, pets.name, pets.age,
             owners.name, types.animal_type 
            from pets join owners on pets.owner_id=owners.id 
            join types on pets.animal_type_id=types.id;"""

        # Execute select
        cursor.execute(sqlSelect)

        for row in cursor:
            # Create pet object for each returned row from sql server and append it to the list
            pets_list.append(Pet(row['name'], row['age'], row['owners.name'], row['animal_type']))

        menu()
except Exception as e:
    print(f"An error has occurred.  Exiting: {e}")
    print("Thank you for using the Pet Chooser!")
    print()

finally:
    myConnection.close()
    print("Connection closed.")

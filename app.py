from compileall import compile_file
import dbhelpers as db
from random import randint, random, choice

# this function sign in the user
def sign_up():
    print("\n---- SIGN UP ----\n")
    username = input("Username:\n")
    password = input("Password:\n")
    # db connection
    cursor = db.connect_db()
    # getting the result form the db
    result = db.execute_statement(
        cursor, 'CALL add_client(?,?)', [username, password])
    # closing the connection
    db.close_connect(cursor)
    # checking to see if the result is has a length of one
    if (len(result) == 1):
        # return the id
        for id in result:
            return id[0]
    # if it empty, show a message to the user
    else:
        print("Your username or password is incorrect. Try again.")
        return

# funtion that will log in the user
def log_in():
    print("\n---- LOG IN ----\n")
    # getting the username and password's user
    username = input("Username:\n")
    password = input("Password:\n")
    # connecting to the db
    cursor = db.connect_db()
    # getting the result form the db
    result = db.execute_statement(
        cursor, 'CALL select_user(?,?)', [username, password])
    # closing the db connection
    db.close_connect(cursor)
    # checking if the result lenght is equal to one, which it has content inside
    if (len(result) == 1):
        # printing the id by looping the result
        for id in result:
            return id[0]
    # if it empty, show a message to the user
    else:
        print("Your username or password is incorrect. Try again.")
        return

def check_if_is_int(argument):
    try:
        int(argument)
    except ValueError:
        print("\n Choose only numbers between the given options.")
        return False

    return True
        

# this function will pick an existing fighter
def pick_fighter(client_id):
    print("\n---- PICKING A FIGHTER ----\n")
    # connection to the db
    cursor = db.connect_db()
    # getting all fighters back
    all_fighters = db.execute_statement(
        cursor, 'CALL get_fighter_by_id(?)', [client_id])
    # closing the db connection
    db.close_connect(cursor)
    
    # checking to see if the lenght is at least 1
    if (len(all_fighters) >= 1):
        # looping the response to print fighter by fighter
        for fighter in all_fighters:
            print(fighter[0], ".", fighter[6].decode("utf-8"), "")
        # asking which fighter the user will pick
        user_fighter_id = input("\nChoose your fighter by their number.\n")
        
        #Checking to see if the user input is a number
        user_fighter_input = check_if_is_int(user_fighter_id)
        if(user_fighter_input):
            # connecting to the db
            cursor = db.connect_db()
            # getting back only the fighter the user picked    
            fighter_info = db.execute_statement(
            cursor, 'CALL get_fighter_info(?)', [int(user_fighter_id)])
            # closing the connection
            db.close_connect(cursor)
            return fighter_info
        else:
            fighter_info = pick_fighter(client_id)
            return fighter_info

    # if the lenght is not at least 1, print a message and call a function that will create a fighter
    else:
        print("You doesn't have any fighter yet.")
        create_fighter(client_id)

# this function wil create a fighter
def create_fighter(client_id):
    print("\n---- CREATING A FIGHTER ----\n")
    # getting the name of the fighter
    name = input("Name of the fighter:\n")
    # connecting to the db
    cursor = db.connect_db()
    # getting back all moves available to the user to pick
    all_moves = db.execute_statement(cursor, 'CALL get_all_moves()')
    # closing the connection
    db.close_connect(cursor)
    # printing all moves in the terminal
    for move in all_moves:
        print("\n", move[0], ".", "Attack name:", move[1].decode(
            "utf-8"), "Lower Damage:", move[2], "Higher Damage:", move[3])
    # asking the user which 4 moves he will pick
    print("From 1 to 10 select your 4 moves.")
    first_move = input("First move: ")
    second_move = input("Second move: ")
    third_move = input("Third move: ")
    four_move = input("Four move: ")
    
    # closing the connection
    cursor = db.connect_db()
    # adding the fighter in the db
    result = db.execute_statement(cursor, 'CALL add_fighter(?,?,?,?,?,?)', [client_id, int(
        first_move), int(second_move), int(third_move), int(four_move), name])
    db.close_connect(cursor)

    # returning the fighter
    return result

# this function will get the user fighter
def get_user_fighter(client_id, fighter_id):
    # connecting to the db
    cursor = db.connect_db()
    # getting the fighter back
    result = db.execute_statement(
        cursor, 'CALL get_fighter_by_fighter_client(?,?)', [client_id, fighter_id])
    # closing the db
    db.close_connect(cursor)
    # adding into variables all fighter's information
    move_one = result[0][2]
    move_two = result[0][3]
    move_three = result[0][4]
    move_four = result[0][5]
    fighter_name = result[0][6].decode("utf-8")
    fighter_health = result[0][7]
    fighter_points = result[0][8]

    # setting a fighter dictionary with these variables
    fighter = {
        'id': fighter_id,
        'client_id': client_id,
        'move_one': move_one,
        'move_two': move_two,
        'move_three': move_three,
        'move_four': move_four,
        'fighter_name': fighter_name,
        'fighter_health': fighter_health,
        'fighter_points': fighter_points
    }

    # returnig the fighter dictionary
    return fighter

# this function will get the move's information
def get_move_info(move_id):
    # connecting to the db
    cursor = db.connect_db()
    # getting the move back by its id
    result = db.execute_statement(
        cursor, 'CALL get_all_moves_by_id(?)', [move_id])
    # closing the connection
    db.close_connect(cursor)
    # returning the result
    return result

# this function will calculete the damaga by a random number between the lower range and upper range
def calculate_damage(lower_range, upper_range):
    damage = randint(lower_range, upper_range)
    return damage

# this function will attack the computer fighter
def attack_opponent(damage, computer_life):
    computer_fighter_life = computer_life
    # calculating the computer lige after being attacked
    computer_fighter_life = computer_fighter_life - damage
    # checking to see if the computer life is more than 0
    if (computer_fighter_life > 0):
        # if yes return its life
        return computer_fighter_life
    # if not, set to zero and return its life
    else:
        computer_fighter_life = 0
        return computer_fighter_life

# if the user fighter win, add points to the fighter
def add_points(client_id, points):
    # db connection
    cursor = db.connect_db()
    # getting the information sent back
    result = db.execute_statement(
        cursor, 'CALL add_fighter_points(?,?)', [points, client_id])
    # closing the connection
    db.close_connect(cursor)
    # returning the user's points
    return result[0][0]

# this function will get the computer fighter
def get_computer_fighter():
    # db connection
    cursor = db.connect_db()
    # getting back the computer fighter
    result = db.execute_statement(cursor, 'CALL get_computer_fighter_info()')
    # closing db connection
    db.close_connect(cursor)

    # setting variables if the computer fighter information
    computer_fighter_id = result[0][0]
    move_one = result[0][1]
    move_two = result[0][2]
    move_three = result[0][3]
    move_four = result[0][4]
    computer_fighter_name = result[0][5].decode("utf-8")
    computer_fighter_life = result[0][6]

    # setting a dictionary with the computer's fighter information
    computer_fighter = {
        'id': computer_fighter_id,
        'move_one': move_one,
        'move_two': move_two,
        'move_three': move_three,
        'move_four': move_four,
        'computer_fighter_name': computer_fighter_name,
        'computer_fighter_life': computer_fighter_life
    }
    
    # returning the computer fighter
    return computer_fighter

# getting a random move based on a given list and returning this move
def get_random_move(list_of_moves):
    move = choice(list_of_moves)
    return move

# calculating the computer attack based on its number
def calculate_attack(oppononet, damage):
    # if the computer is weak, subtract 2 from their attack
    if (oppononet == 1):
        attack = damage - 2
        return attack
    # if the computer is fair, do nothing with the attack
    elif (oppononet == 2):
        return damage
    # if the computer is strong, add 2 from their attack
    elif (oppononet == 3):
        attack = damage + 2
        return attack

# this function will make the computer attack the user fighter
def computer_attack(computer_fighter, opponent, user_fighter_life):
    # adding all computer moves to a list
    computer_moves = []
    computer_moves.append(computer_fighter['move_one'])
    computer_moves.append(computer_fighter['move_two'])
    computer_moves.append(computer_fighter['move_three'])
    computer_moves.append(computer_fighter['move_four'])

    # calling a function that will return a random move
    random_move = get_random_move(computer_moves)
    # calling a function that will get all move information
    move_info = get_move_info(random_move)
    # setting this variables to has the computer's lower and upper damages
    lower_range = move_info[0][2]
    upper_range = move_info[0][3]
    # calculating the damage
    damage = calculate_damage(lower_range, upper_range)
    # calculating the attack
    attack = calculate_attack(opponent, damage)
    # updating the user fighter life
    user_fighter_life = user_fighter_life - attack

    # if the user life is more than zero return its life
    if(user_fighter_life > 0):
        return user_fighter_life
    # if note, set to zero its life then return its life
    else:
        user_fighter_life = 0
        return user_fighter_life

# this function will get the user fighter move based on the fighter id
def get_user_fighter_moves(fighter_id):
    # db connection
    cursor = db.connect_db()
    # getting back the fighter moves
    result = db.execute_statement(cursor, 'CALL get_user_fighter_by_fighter_id(?)', [fighter_id])
    # closing db connection
    db.close_connect(cursor)
    # returning the result
    return result

# this function will print the user info
def user_move(user_fighter, user_life, computer_life):
    # calling the function that will get the user fighter info to be printed
    user_moves = get_user_fighter_moves(user_fighter['id'])
    print("\n---- YOUR FIGHTER ----")
    print("\nName:", user_fighter['fighter_name'])
    print("Health:", user_life)
    print("Points:", user_fighter['fighter_points'])
    print("--------------------------------------------------")
    print("\nComputer Health:", computer_life,"\n")
    print("\n---- MOVES ----")
    print(user_moves[0][0], user_moves[0][1].decode("utf-8"))
    print(user_moves[1][0], user_moves[1][1].decode("utf-8"))
    print(user_moves[2][0], user_moves[2][1].decode("utf-8"))
    print(user_moves[3][0], user_moves[3][1].decode("utf-8"))
    # asking the user which move he will pick to attack
    move_id = input(
        "\nWhich move do you choose? Choose by their numbers id.\n")

    move_id_input = check_if_is_int(move_id)
    if(move_id_input):
        # returning this move id picked
        return move_id
    else:
        move_id = user_move(user_fighter, user_life, computer_life)
        return move_id

# this function will start the fight
def fight(client_id, user_fighter, opponent, computer_fighter, user_life, computer_life):
    # calling a function that will get the move id
    move_id = user_move(user_fighter, user_life, computer_life)
    # calling a function that will get the move info based on its id
    move_info = get_move_info(move_id)
    # setting these variables to the lower and upper range
    lower_range = move_info[0][2]
    upper_range = move_info[0][3]

    # calculating the damage
    damage = calculate_damage(lower_range, upper_range)
    # calculating the computer life after being attacked
    computer_life = attack_opponent(damage, computer_life)
    # if the computer life is zero print a message to the user that we has won
    if (computer_life == 0):
        print("---- YOU WON ----")
        # calling a function that will add points to the user's fighter
        add_points(client_id, opponent)
        # asking the user if he wanna play again and based on that, initiate the game again or kill the application
        print("\nWanna play again? y/n\n")
        play_again = input("Type y for yes or n to no.\n")
        if (play_again == 'y' or play_again == 'Y'):
            user_selection_fighter(client_id)
        elif (play_again == 'n' or play_again == 'N'):
            print("Bye.")
    # if the user life is more than zero
    else:
        # call a function that will attack the user fighter
        user_fighter_life = computer_attack(computer_fighter, opponent, user_life)
        # if the user life is equal to zero print a message to the user that has lost
        if(user_fighter_life == 0):
            print("\n---- YOU LOST ----\n")
            # asking the user if he wanna play again and based on that, initiate the game again or kill the application
            print("\nWanna play again? y/n\n")
            play_again = input("Type y for yes or n to no.\n")
            if (play_again == 'y' or play_again == 'Y'):
                user_selection_fighter(client_id)
            elif (play_again == 'n' or play_again == 'N'):
                print("Bye.")
        # if the user life is more than zero, call the function that will start the user attack again
        fight(client_id, user_fighter, opponent, computer_fighter, user_fighter_life, computer_life)

# this function will display the user opponents and based on the user selection will return a number that represents the opponent
def choose_opponent():
    print("\n ---- CHOOSE YOUR OPPONENT ---- \n")
    print("1. Weak opponent. If you win will award you 1 point.")
    print("2. Fair opponent. If you win will award you 2 points.")
    print("3. Strong opponent. If you win will award you 4 points.")
    opponent = input("\nWhich one do you choose?\n")
    if (opponent == '1'):
        return 1
    elif (opponent == '2'):
        return 2
    elif (opponent == '3'):
        return 3
    else:
        print("Choose a number between 1, 2 or 3. Try again.")
        choose_opponent()

# this function will ask the user if he wants to create a fighter or pick an existing one
def user_selection_fighter(client_id):
    print("\n1. Create a new fighter?")
    print("2. Pick an existing fighter?\n")
    user_selection = input("Chose 1 or 2.\n")
    # if the user selection is 1, call the function that will create a fighter
    if (user_selection == '1'):
        # creating the user fighter
        user_fighter = create_fighter(client_id)
        # getting the user fighter
        user_fighter = get_user_fighter(client_id, user_fighter[0][0])
        # getting the computer fighter
        computer_fighter = get_computer_fighter()
        # getting the user opponent
        opponent = choose_opponent()
        # calling the function that will start the fight
        fight(client_id, user_fighter, opponent, computer_fighter)
    elif (user_selection == '2'):
        # picking an existing fighter
        user_fighter = pick_fighter(client_id)
        # getting the user fighter
        user_fighter = get_user_fighter(client_id, user_fighter[0][0])
        # getting the computer fighter
        computer_fighter = get_computer_fighter()
        # getting the user opponent
        opponent = choose_opponent()
        # calling the function that will start the fight
        fight(client_id, user_fighter, opponent, computer_fighter, user_fighter['fighter_health'], computer_fighter['computer_fighter_life'])
    # id the user types an different number or caracter, call the function again
    else:
        print("Wrong number. Please type only 1 or 2.")
        user_selection_fighter(client_id)

    # this return will only be attempt if the user wanted to end the application when asked
    return True

# this while true start the application
while (True):
    print("\n1. Sign up?")
    print("2. Log in?\n")
    # getting the user selection after asking him if we wants to sign in or log in
    user_selection = input("Chose 1 or 2.\n")
    # if the user types 1, call the function that will sign in him
    if (user_selection == '1'):
        # calling the sign in function
        client_id = sign_up()
        # getting the result if the user want to end the application and then breaking it
        end_game = user_selection_fighter(client_id)
        if(end_game):
            break
    # if the user types 2, call the function that will log in him
    elif (user_selection == '2'):
        # calling the log in function
        client_id = log_in()
        # getting the result if the user want to end the application and then breaking it
        end_game = user_selection_fighter(client_id)
        if(end_game):
            break
    else:
        print("Chose the number 1 to Sign Up or 2 to Log In.")

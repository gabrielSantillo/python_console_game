import dbhelpers as db
from random import randint, random, choice

def sign_up():
    print("\n---- SIGN UP ----\n")
    username = input("Username:\n")
    password = input("Password:\n")
    cursor = db.connect_db()
    result = db.execute_statement(
        cursor, 'CALL add_client(?,?)', [username, password])
    db.close_connect(cursor)
    if (len(result) == 1):
        # printing the id by looping the result
        for id in result:
            return id[0]
    # if it empty, show a message to the user
    else:
        print("Your username or password is incorrect. Try again.")
        return


def log_in():
    print("\n---- LOG IN ----\n")
    username = input("Username:\n")
    password = input("Password:\n")
    cursor = db.connect_db()
    result = db.execute_statement(
        cursor, 'CALL select_user(?,?)', [username, password])
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


def pick_fighter(client_id):
    print("\n---- PICKING A FIGHTER ----\n")
    cursor = db.connect_db()
    all_fighters = db.execute_statement(
        cursor, 'CALL get_fighter_by_id(?)', [client_id])
    db.close_connect(cursor)
    if (len(all_fighters) >= 1):
        for fighter in all_fighters:
            print(fighter[0], ".", fighter[6].decode("utf-8"), "")
        user_fighter_id = input("\nChoose your fighter by their number.\n")
        for fighter in all_fighters:
            if (str(fighter[0]) == user_fighter_id):
                return fighter
            else:
                print("Choose between the numbers displayed.")
                pick_fighter(client_id)

    else:
        print("You doesn't have any fighter yet.")
        create_fighter(client_id)


def create_fighter(client_id):
    print("\n---- CREATING A FIGHTER ----\n")
    name = input("Name of the fighter:\n")
    cursor = db.connect_db()
    all_moves = db.execute_statement(cursor, 'CALL get_all_moves()')
    db.close_connect(cursor)
    for move in all_moves:
        print("\n", move[0], ".", "Attack name:", move[1].decode(
            "utf-8"), "Lower Damage:", move[2], "Higher Damage:", move[3])

    print("From 1 to 10 select your 4 moves.")
    first_move = input("First move: ")
    second_move = input("Second move: ")
    third_move = input("Third move: ")
    four_move = input("Four move: ")

    cursor = db.connect_db()
    result = db.execute_statement(cursor, 'CALL add_fighter(?,?,?,?,?,?)', [client_id, int(
        first_move), int(second_move), int(third_move), int(four_move), name])
    db.close_connect(cursor)

    return result

def get_user_fighter(fighter_id):
    cursor = db.connect_db()
    result = db.execute_statement(cursor, 'CALL get_user_fighter_by_fighter_id(?)', [fighter_id])
    db.close_connect(cursor)
    return result

def get_move_info(move_id):
    cursor = db.connect_db()
    result = db.execute_statement(cursor, 'CALL get_all_moves_by_id(?)', [move_id])
    db.close_connect(cursor)
    return result

def calculate_damage(lower_range, upper_range):
    damage = randint(lower_range, upper_range)
    return damage


def attack_opponent(damage, computer_fighter):
    computer_fighter_life = computer_fighter[0][4]
    computer_fighter_life = computer_fighter_life - damage
    if(computer_fighter_life > 0):
        return computer_fighter_life
    else:
        computer_fighter_life = 0
        return computer_fighter_life

def add_points(client_id, points):
    cursor = db.connect_db()
    result = db.execute_statement(cursor, 'CALL add_fighter_points(?,?)', [points, client_id])
    db.close_connect(cursor)
    return result[0][0]


def get_computer_fighter():
    cursor = db.connect_db()
    result = db.execute_statement(cursor, 'CALL get_computer_fighter()')
    db.close_connect(cursor)
    return result

def get_random_move(list_of_moves):
    move = choice(list_of_moves)
    return move

def calculate_attack(oppononet, damage):
    if(oppononet == 1):
        attack = damage - 2
        return attack
    elif(oppononet == 2):
        return damage
    elif(oppononet == 3):
        attack = damage + 2
        return attack

def computer_attack(computer_fighter, opponent, user_fighter_life):
    # the order here is
    # get the computer fighter lower and uppr range, call the function calculate_damage to return the value of tha damage
    computer_moves = []
    for move in computer_fighter:
        computer_moves.append(move[2])
    
    random_move = get_random_move(computer_moves)
    move_info = get_move_info(random_move)
    lower_range = move_info[0][2]
    upper_range = move_info[0][3]
    damage = calculate_damage(lower_range, upper_range)
    attack = calculate_attack(opponent, damage)
    user_fighter_life = user_fighter_life - attack
    # create a function that have opponent as argument to check if the user is weak, fair or strong and do something about it (weak subtract 2 to the attack, fair do nothing with the attack, strong add 2 to
    # the attack)
    # create a function that will calculate the damage and update the user health in the db
    # finally return the user current health


def fight(client_id, user_fighter, opponent, computer_fighter):
    fighter = get_user_fighter(user_fighter[0])
    print("\n---- YOUR FIGHTER ----")
    print("\nName:", fighter[0][2].decode("utf-8"))
    print("Health:", fighter[0][5])
    print("Points:", fighter[0][6])
    print("\n---- MOVES ----\n")
    print(fighter[0][3], fighter[0][4].decode("utf-8"))
    print(fighter[1][3], fighter[1][4].decode("utf-8"))
    print(fighter[2][3], fighter[2][4].decode("utf-8"))
    print(fighter[3][3], fighter[3][4].decode("utf-8"))
    move_id = input("\nWhich move do you choose? Choose by their numbers id.\n")

    move_info = get_move_info(move_id)
    lower_range = move_info[0][2]
    upper_range = move_info[0][3]

    damage = calculate_damage(lower_range, upper_range)

    computer_life = attack_opponent(damage, computer_fighter)
    if(computer_life == 0):
        print("---- YOU WON ----")
        add_points(client_id, opponent)
        print("\nWanna play again? y/n\n")
        play_again = input("Type y for yes or n to no.")
        if(play_again == 'y' or play_again == 'Y'):
            user_selection_fighter(client_id)
        elif(play_again == 'n' or play_again == 'N'):
            print("Bye.")
            #write here a code that will end the game
    else:
        damage = computer_attack(computer_fighter, opponent, fighter[0][5])




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


def user_selection_fighter(client_id):
    print("\n1. Create a new fighter?")
    print("2. Pick an existing fighter?\n")
    user_selection = input("Chose 1 or 2.\n")
    if (user_selection == '1'):
        user_fighter = create_fighter(client_id)
        computer_fighter = get_computer_fighter()
        opponent = choose_opponent()
        fight(client_id, user_fighter, opponent, computer_fighter)
    elif (user_selection == '2'):
        user_fighter = pick_fighter(client_id)
        computer_fighter = get_computer_fighter()
        opponent = choose_opponent()
        fight(client_id, user_fighter, opponent, computer_fighter)
    else:
        print("Wrong number. Please type only 1 or 2.")
        user_selection_fighter(client_id)


while (True):
    print("\n1. Sign up?")
    print("2. Log in?\n")
    user_selection = input("Chose 1 or 2.\n")
    if (user_selection == '1'):
        client_id = sign_up()
        user_selection_fighter(client_id)
    elif (user_selection == '2'):
        client_id = log_in()
        user_selection_fighter(client_id)
    else:
        print("Chose the number 1 to Sign Up or 2 to Log In.")

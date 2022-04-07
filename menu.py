import pathlib
import dressphere_execute
import TkinterTemplate
import importlib

class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

seed_path = "Test Files/seed.txt"

def read_seed():
    with open(seed_path, 'r') as seed_file:
        try:
            seed = int(seed_file.read())
        except:
            print("Error reading seed.txt file, please make sure it contains a valid integer.")
            exit()
    seed_file.close()
    return seed

seed = read_seed()

def menu():
    seed = read_seed()

    menu_flag = True

    line_breaker = "-------------------"

    menu_options = {
        1: 'Set Seed',
        2: 'Print current seed',
        3: 'Execute randomizer',
        4: 'Launch dressphere viewer',
        5: 'Exit'
    }

    def print_menu():
        for key in menu_options.keys():
            print (key, '--', menu_options[key] )

    def option1():
        submenu_flag = True
        while(submenu_flag == True):
            submenu_2_flag = False
            try:
                print(line_breaker)
                seed = int(input('Type an integer as the seed: '))
                print(line_breaker)
            except:
                submenu_2_flag = True
                print('Wrong input. Please enter a number ...')
            if submenu_2_flag == False:
                print("The current seed is: " + str(seed))
                print(line_breaker)
                with open(seed_path, 'w') as seed_file:
                    seed_file.write(str(seed))
                    seed_file.close()
                submenu_flag = False
                main_menu()





    def option2():
        seed = read_seed()
        print(line_breaker)
        print("The current seed is: " + str(seed))
        print(line_breaker)
        main_menu()

    def option3():
        importlib.reload(dressphere_execute)
        dressphere_execute.execute_randomizer()
        main_menu()

    def option4():
        importlib.reload(dressphere_execute)
        importlib.reload(TkinterTemplate)
        TkinterTemplate.initialize()
        main_menu()

    def main_menu():
        seed = read_seed()
        while(menu_flag == True):
            seed = read_seed()
            print_menu()
            option = ''
            try:
                option = int(input('Enter your choice: '))
            except:
                print('Wrong input. Please enter a number ...')
            #Check what choice was entered and act accordingly
            if option == 1:
               option1()
            elif option == 2:
                option2()
            elif option == 3:
                option3()
            elif option == 4:
                option4()
            elif option == 5:
                print('Thanks for trying out the FFX-2 Randomizer!')
                exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

    main_menu()

menu()
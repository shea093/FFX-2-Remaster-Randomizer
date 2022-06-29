import pathlib
import dressphere_randomize
import spoiler_tool
import importlib
import sys
import os
import monster_edit

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")

    return os.path.join(base_path, relative_path)

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

seed_path = resource_path(pathlib.PureWindowsPath("Test Files\seed.txt"))
test = ""

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

    line_breaker = "-----------------------"

    menu_options = {
        1: 'Execute Randomizer and Hard Mode (Recommended)',
        2: 'Execute only Dressphere Stat&Ability Randomizer',
        3: 'Execute only Hard Mode',
        4: 'Set Seed',
        5: 'Print current seed',
        6: 'Launch Dressphere Spoiler tool',
        7: 'Get default files (Reset)',
        8: 'Exit'

    }

    def print_menu():
        print(line_breaker)
        for key in menu_options.keys():
            print (key, '--', menu_options[key] )
        print(line_breaker)

    def option4():
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





    def option5():
        seed = read_seed()
        print(line_breaker)
        print("** The current seed is: " + str(seed) + " **")
        print(line_breaker)
        input("Press any key to continue.")
        main_menu()

    def option1():
        importlib.reload(dressphere_randomize)
        dressphere_randomize.change_potencies(dressphere_randomize.global_abilities)
        dressphere_randomize.set_ability_ap_batch()
        dressphere_randomize.replace_ap_with_file_changes()
        dressphere_randomize.batch_AP_multiply()
        dressphere_randomize.write_ap_chunks()

        dressphere_randomize.write_potencies()
        dressphere_randomize.execute_randomizer(reset_bins=False)
        importlib.reload(monster_edit)
        monster_edit.write_bins_new(reset_bins=False)
        main_menu()

    def option2():
        importlib.reload(dressphere_randomize)
        dressphere_randomize.set_ability_ap_batch()
        dressphere_randomize.replace_ap_with_file_changes()
        dressphere_randomize.batch_AP_multiply()
        dressphere_randomize.write_ap_chunks()
        dressphere_randomize.execute_randomizer(reset_bins=False)
        input("Press any key to continue...")
        main_menu()

    def option6():
        importlib.reload(dressphere_randomize)
        importlib.reload(spoiler_tool)
        spoiler_tool.initialize()
        main_menu()

    def option3():
        importlib.reload(dressphere_randomize)
        dressphere_randomize.global_abilities = dressphere_randomize.initiate_abilities()
        dressphere_randomize.dresspheres = dressphere_randomize.initiate_dresspheres_new()
        dressphere_randomize.set_dmg_info_batch()
        dressphere_randomize.set_ability_ap_batch(hard_mode_only=True)
        dressphere_randomize.batch_AP_multiply()
        dressphere_randomize.write_ap_chunks()
        dressphere_randomize.change_potencies(dressphere_randomize.global_abilities)
        dressphere_randomize.write_potencies()
        dressphere_randomize.execute_randomizer(reset_bins=False,hard_mode_only=True)
        importlib.reload(monster_edit)
        monster_edit.write_bins_new(reset_bins=False)
        main_menu()

    def option7():
        importlib.reload(monster_edit)
        importlib.reload(dressphere_randomize)
        dressphere_randomize.execute_randomizer(reset_bins=True)
        monster_edit.write_bins_new(reset_bins=True)
        main_menu()

    def main_menu():
        seed = read_seed()
        while(menu_flag == True):
            seed = read_seed()
            print_menu()
            option = ''
            try:
                option = int(input('Enter your choice then press Enter: '))
                if option < 0 or option > 8:
                    raise ValueError
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
                option5()
            elif option == 6:
                option6()
            elif option == 7:
                option7()
            elif option == 8:
                print(line_breaker)
                print('Thanks for trying out the FFX-2 Randomizer!')
                sys.exit()
        else:
            print('Invalid option. Please enter a number between 1 and 4.')

    main_menu()

menu()
import argparse
import sys
from arg_type import arg_type

def menu_screen():
    menu = {}
    menu['1:'] = 'Option'
    menu['2:'] = 'Option'
    menu['3:'] = 'Option'
    menu['4:'] = 'Option'
    while True:
        options = menu.keys()
        for entry in options:
            print(entry, menu[entry])
        try:
            selection = input("Select An Option: ")
            if selection == '1':
                print('1')
                break
            elif selection == '2':
                print('2')
                break
            elif selection == '3':
                print('3')
                break
            elif selection == '4':
                print('3')
            else:
                print("Unknown Option")
        except KeyboardInterrupt:
            print('\nKeyboard Interrupt Detected')
            print('\nOk byeeeeeeeee')
            sys.exit()


def main():
    menu_screen()

if __name__ == "__main__":
    print('calling as script...')
    parser = argparse.ArgumentParser()
    parser.add_argument("file")
    args = parser.parse_args()
    #Determine arg type and handle it
    arg_type(args.file)
    
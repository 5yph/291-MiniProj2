from usermenu import uMenu

load_json = __import__('load-json')

def main():
    thisCollection = None
    print("-------------")
    print("MONGOLOIDDB DATA STORING PROGRAM")
    print("-------------")

    while(1):
        print("Welcome, Mongoloid. Choose an option:")
        print("1: Build a Collection.")
        print("2: User Menus.")
        print("q: Exit.")
        x = input()
        if (x not in ['1','2','q']):
            print("Please put a valid input !")
            continue
        elif (x == '1'):
            thisCollection = load_json.createCollection()
            continue
        elif (x == '2'):
            if thisCollection is None:
                print("You haven't created a database collection yet!")
                continue
            else:
                uMenu(thisCollection)
                continue
        elif (x == 'q'):
            print("Exiting. Thank you for using the MongoloidDB Data Storing Program! ")
            break


if __name__ == "__main__":
    main()
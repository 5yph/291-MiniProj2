def main():

    print("")
    print("User Menu")
    print("---------")

    print("You've created a MongoloidDB database! What would you like to do now?")
    sno = None
    while (1):
        print("Select an option: ")
        print("1: Search for Articles")
        print("2: Search for Authors")
        print("3: List the Venues")
        print("4: Add an Article")
        print("q: Quit")
        x = input()
        if (x not in ['1','2','3','4','q']):
            print("Please put a valid input !")
            continue
        if (x == '1'):
            continue
        if (x == '2'):
            continue
        if (x == '3'):
            continue

        if (x == '4'):
            continue

        if (x == 'q'):
            print('Thank you for using MongoloidDB Data Storing Program!')
            print("Exiting ...")
            break



if __name__ == "__main__":
    main()
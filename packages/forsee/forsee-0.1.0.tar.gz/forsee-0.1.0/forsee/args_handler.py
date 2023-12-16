import os
script_directory = os.path.dirname(os.path.abspath(__file__))

def set_path(path):
    try:
        with open(script_directory +'/default.txt','w') as file:
            file.write(path)
            print_success("default path changed to:")
            print(path)
    except Exception as e:
        print_error(e)
        


def print_help():
    print(" Forsee Beta:")  
    print(" Author Nikos Tzeka\n")

    print(" Forsee is a program created by Itec-audio and is used to generate a compile database\n specifically from CrossCore Embedded Studio\n")
    print(" In order for the program to work you need to get into CCES project propertied\n and make sure that the run commad is \'make -nw\' instead of \'make\'")
    print(" \n--------------------------------USAGE--------------------------------------\n")
    print(" If the DCT console logs in the default directory, then you only need to type your project name")
    print(" Otherwise you can change this directory with the --default option \n or give as input the whole path to you build.log file")
    print("\n\n")
    print("         OPTIONS")
    print("         ________")
    print("         -h   --help             prints this menu")
    print("         --default=              sets the default searching directory")
    print("         projectname             exports the compile commands in your projects directory")
    print("                                     e.g     c4 projectname1 projectname2 C:/absolute/path/to/the/build.log")
    print("\n\n")
    print(" \n!! Please Note that for now you can you only one type of argument at a time")
    print(" Thats all for now :)")
    print(" !!!!! VERY IMPORTANT !!!!!!!!")
    print(" o valatis einai omofoilofilos")
    exit()


def print_error(error):
    print("\033[31mFAIL:\033[0m")
    print("     error:" + error)

def print_success(msg):
    print("\033[32mSUCCESS:\033[0m")
    print(msg)


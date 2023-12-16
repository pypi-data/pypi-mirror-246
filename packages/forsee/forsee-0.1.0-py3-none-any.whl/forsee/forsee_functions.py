import json
import os
from sre_constants import FAILURE, SUCCESS
from .args_handler import print_error,print_help,print_success,set_path


#comment that in case we mess up and still need to go here
#defaultPath = "C:/Users/Nikolaos/cces/2.12.0/.metadata/.plugins/org.eclipse.cdt.ui/"

script_directory = os.path.dirname(os.path.abspath(__file__))


def set_def_path():
    try:
        with open(script_directory + '/default.txt','r') as file:
            somepaths = file.readlines()
            for line in  somepaths:
                return line.strip()
    except FileNotFoundError as e:
        with open(script_directory +'/default.txt','w') as file:
            relative_path = 'cces/2.12.0/.metadata/.plugins/org.eclipse.cdt.ui/'

            # Expand the user's home directory and join it with the relative path
            full_path = os.path.expanduser(os.path.join('~', relative_path))
            file.write(full_path)
            return full_path
            

def handle_arguments(arguments):
    if(len(arguments) == 0 ):
        print_error("No options presented")
        exit(0)
    if("-h" in arguments or "--help" in arguments):
        print_help()
        exit(0)
    
    for arg in arguments:
        if "--default" in arg:
            path = arg.split('=')
            set_path(path[1])
            exit(0)
    else:
        return arguments


def create_compiledb(output_file_path,jsonformat):
    try:
        with open(output_file_path, 'w') as json_file:
            json.dump(jsonformat, json_file, indent=2)
            return SUCCESS
    except Exception as e:
        print_error("Could not generate the json file")


def get_project_path(project_name,defaultPath):
    if(project_name[0] == 'C'):
        if os.path.exists(project_name):
            return project_name
        return FAILURE
    else:
        for root,dirs,files in os.walk(defaultPath):
            for file in files:
                if project_name in file:
                    path = os.path.join(root,file)
                    print(path)
                    if os.path.exists(path):
                        return path
                    print(path)
    return FAILURE
                
def filter_data(cces_log_file):
    #clean the data
    strings_to_keep = ["lkfn","Finished building"]

    # Open the input file in read mode
    with open(cces_log_file, 'r') as infile:
        # Read all lines from the file      
        lines = infile.readlines()

    # Filter lines that contain the specific string
    return [line for line in lines 
            if (strings_to_keep[0] in line or
                strings_to_keep[1] in line
                ) ]

def get_directory(cces_log_file):
    with open(cces_log_file, 'r') as infile:
        for line in infile:
                if "entering directory" in line.lower():
                    path = line.split('\'')
                    return path[1]
                

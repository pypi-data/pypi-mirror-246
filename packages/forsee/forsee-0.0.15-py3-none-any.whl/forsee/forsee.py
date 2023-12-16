import sys
from .forsee_functions import *
from sre_constants import FAILURE, SUCCESS
from .args_handler import *




def main():

    #cces_log_file = "C:/Users/Nikolaos/cces/2.12.0/.metadata/.plugins/org.eclipse.cdt.ui/testAnalyser_Core0.build.log"

    defaultPath = set_def_path()

    arguments = sys.argv[1:]

    projects = handle_arguments(arguments)

    for i in range(0,len(projects)):


        
        ##get the path from arguments
        print(projects[i])
        cces_log_file = get_project_path(projects[i],defaultPath)
        if(cces_log_file == FAILURE):
            print_error("Path not Found")
            exit(1)


        #file is too populated...here we filter only the lines we need(command and file)
        filtered_lines = filter_data(cces_log_file)


        directory = get_directory(cces_log_file)
        command = ""
        file = ""
        jsonformat = []

        #the flag idea is to basically write to the json every second command

        for line in filtered_lines:
            if "lkfn" in line:
                command = line[:-1]
            if "Finished" in line:
                file = line.split(':')  #the line in the file is in this format  Funished build: ../path/to/the/thing/you.want"\n
                file = file[1]          #now we only keep the second part
                file = file[1:-2]       #and remove the first char (empty space) and the 2 last (\n and ')

                #organise the outputs so they are ready to be dumbed into the json
                jsonformat.append({
                    'directory' : directory,
                    'command': command,
                    'file': file
                })

        #dump data to json file
        output_file_path = directory + '/compile_commands.json'
        if(create_compiledb(output_file_path,jsonformat) == SUCCESS):
            print_success("You can find you compile_commands.json at:")
            print("         "+directory)
        else:
            print_error()

if __name__ == "__main__":

    main()



#!/usr/bin/env python3
# Teaching machine by Holland and Skinner. Behavior analysis self-teaching.
import sys, os, json

def mylistdir(directory):
    """ A specialized version of os.listdir() that ignores files that
    start with a leading period """
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]

def display_welcome():
    """ print welcome line on launch of program """
    print()
    print("Welcome to Holland-Skinner Teaching Machine!\n".center(80))

def display_contents(course_folder, current_set_num):
    """ prints course contents and prompts the user to quit or proceed """
    print("Course contents:")
    for set_filename in mylistdir(course_folder):
        set_path = os.path.join(course_folder, set_filename)
        with open(set_path) as f:
            this_set = json.loads(f.read())
            this_set_name = this_set["set_name"]
            this_set_num = this_set["set_number"]
            print(this_set_num, end = " ")
            if this_set_num == current_set_num:
                print(this_set_name.upper() + \
                      "<-- current set".rjust(65 - len(this_set_name)))
                current_set_path = set_path
            else:
                print(this_set_name)
#    if input("[q]uit or [enter]\n") == 'q':
#        return 'User quit'
#    else:
    return current_set_path

def get_progress(progress_file_path):
    """ returns user progress """
    try:
        with open(progress_file_path, 'x') as f:
            initial = '{"current set": "1.1", "frames complete": []}'
            f.write(initial)
        return json.loads(initial)
    except FileExistsError:
        with open(progress_file_path, 'r') as f:
            return (json.loads(f.read()))

def display_frame(progress, current_set_filename):
    """ displays the frame interface """
    # TODO
    pass

def main():
    """ Main entry point for the script """
    # HSM.py file path:
    hsm_folder_path = (os.path.split(os.path.realpath(__file__))[0])
    # resources folder path:
    resources_path = os.path.join(hsm_folder_path, "resources")
    # course content files folder path:
    course_folder_path = os.path.join(resources_path, "course")
    # user progress file path:
    progress_file_path = os.path.join(resources_path, "progress.json")
    display_welcome()
    progress = get_progress(progress_file_path)
    current_set_path = display_contents(course_folder_path, \
                                            progress["current set"])
    if current_set_path == 'User quit':
        return 'User quit'
    display_frame(progress, current_set_path)
    return "Normal exit"

if __name__ == '__main__':
    sys.exit(print(main()))

#!/usr/bin/env python3
# Teaching machine by Holland and Skinner. Behavior analysis self-teaching.
import sys, os, json, pprint

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

def get_progress(progress_file_path):
    """ returns user progress dictionary """
    try:
        with open(progress_file_path, 'x') as f:
            initial = {"current_set_num": "1.1",
                       "current_frame_num": 0,
                       "frames_complete": []}
            f.write(json.dumps(initial))
    except: pass
    
    with open(progress_file_path, 'r') as f:
        return (json.loads(f.read()))

def display_contents(course_folder, current_set_num):
    """ prints course contents and prompts the user to quit or proceed.
        returns current set path and the curriculum dictionary """
    print("Course contents:\n")
    curriculum = []
    
    # Going over the course files
    for set_filename in mylistdir(course_folder):
        set_path = os.path.join(course_folder, set_filename)
        with open(set_path) as f:
            this_set = json.loads(f.read())
            this_set_name = this_set["set_name"]
            this_set_num = this_set["set_number"]
            print(this_set_num, end = " ")
            # Add path only to non-empty list.
            if curriculum:
                curriculum.append(set_path)
            if this_set_num == current_set_num:
                print(this_set_name.upper() + \
                      "<-- current set".rjust(65 - len(this_set_name)))
                # start compiling curriculum from the current set:
                curriculum.append(set_path)
            else:
                print(this_set_name)
        
##    if input("[q]uit or [enter]\n") == 'q':
##        return 'User quit'
##    else:
    return curriculum

def answers_input(frame_answers):
    for i in range(len(frame_answers)):
        prompt = ""
        user_input = input(str(i + 1) + ': ') # question number as prompt
        if user_input in frame_answers[i]:
            print('  ', user_input, "Correct!")

def frames_loop(progress, curriculum):
    """ frames interface main loop """
    # Load current set into memory
    for set_path in curriculum:
        with open(set_path) as f:
            the_set = json.loads(f.read())
            set_number = the_set["set_number"]
            set_name = the_set["set_name"]
            exhibit, frames = the_set["exhibit"], the_set["frames"]
            current_frame_num = progress["current_frame_num"]
        # Loop frames
            for frame in frames[current_frame_num:]:
                # Display stuff
                # Set title
                print(set_number.ljust(3), set_name.ljust(60), end = "")
                # Progress (Frame 5 / 26)
                print("Frame", current_frame_num, "/", len(frames), "\n")
                # The contents of current frame
                print(frame[0], "\n")
                # Ask for input once.
                print('Please enter your answers. Enter "?" to get a prompt.')
                answers_input(frame[1:])

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
    # progress object
    # {"current_frame_num": ..., "frames_complete": [...] \
    # "current_set_num": ...}:
    progress = get_progress(progress_file_path)
    curriculum = display_contents(course_folder_path, \
                                  progress["current_set_num"])
    if curriculum == 'User quit':
        return 'User quit'
    frames_loop(progress, curriculum)
        
    return "Normal exit"

if __name__ == '__main__':
    sys.exit(print(main()))

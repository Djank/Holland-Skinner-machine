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

def get_prompt(answer, prompt):
    """ Returns next prompt """
    prompt = answer[:len(prompt) + 1]
    print(prompt)
    return prompt

def answers_input(frame_answers, progress):
    message = 'correct'
    # loop through answers
    for i in range(len(frame_answers)):
        prompt = ""
        # loop for the sake of prompting
        while prompt != frame_answers[i][0]:
            # Display question number every time
            user_input = input(str(i + 1) + ': ')
            if user_input in frame_answers[i]:
                print('  ', user_input, "\nCorrect!")
                break
            elif user_input == 'q':
                return 'User quit'
            else: 
                message = 'incorrect'
                if user_input == '?':
                    # prompt is given by the first of alternative correct answers
                    prompt = get_prompt(frame_answers[i][0], prompt)
                else:
                    for answer in frame_answers[i]:
                        print("  ", answer)
                    print("Incorrect")
                    break
    return message

def frames_loop(progress_file_path, curriculum):
    """ frames interface main loop """
    # load progress data
    with open(progress_file_path) as p:
        progress = json.loads(p.read())
    # loop sets
    for set_path in curriculum:
        with open(set_path) as f:
            the_set = json.loads(f.read())
        set_number = the_set["set_number"]
        set_name = the_set["set_name"]
        exhibit = the_set["exhibit"]
        frames = the_set["frames"]
        # Loop frames
        for frame in frames[progress["current_frame_num"]:]:
            # Display stuff
            # Set title
            print(set_number.ljust(3), set_name.ljust(60), end = "")
            # Progress (Frame 5 / 26)
            print("Frame", progress["current_frame_num"] + 1,
                  "/", len(frames), "\n")
            # The contents of current frame
            print(frame[0], "\n")
            # Ask for input once
            print('Please enter your answers. Enter "?" to get a prompt.')
            msg = answers_input(frame[1:], progress)
            if msg == 'correct':
                progress["frames_complete"].append(progress["current_frame_num"])
                progress["current_frame_num"] += 1
            elif msg == 'User quit':
                # record progress to file, quit
                print('Saving progress')
                with open(progress_file_path, 'w') as p:
                    p.write(json.dumps(progress))
                print('Done!')
                return 'User quit'
                    
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
    frames_loop(progress_file_path, curriculum)
        
    return "Normal exit"

if __name__ == '__main__':
    sys.exit(print(main()))

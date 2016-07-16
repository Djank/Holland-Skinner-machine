#!/usr/bin/env python3

import sys, os, json

def mylistdir(directory):
    """ A specialized version of os.listdir() that ignores files that
    start with a leading period """
    filelist = os.listdir(directory)
    return [x for x in filelist if not (x.startswith('.'))]

def display_welcome():
    """ print welcome line on launch of program """
    print()
    print("Welcome to Holland-Skinner Teaching Machine!\n".center(80))

def display_contents(course_folder, current_lesson_num):
    """ prints course contents and prompts the user to quit or proceed.
        returns current lesson path and the curriculum dictionary """
    print("Course contents:\n")
    curriculum = []
    
    # Going over the course files
    for lesson_filename in mylistdir(course_folder):
        lesson_path = os.path.join(course_folder, lesson_filename)
        with open(lesson_path) as f:
            this_lesson = json.loads(f.read())
            this_lesson_name = this_lesson["lesson_name"]
            this_lesson_num = this_lesson["lesson_number"]
            print(this_lesson_num, end = " ")
            # Add path only to non-empty list.
            if curriculum:
                curriculum.append(lesson_path)
            if this_lesson_num == current_lesson_num:
                print(this_lesson_name.upper(),
                      "<-- current lesson".rjust(65 - len(this_lesson_name)))
                # start compiling curriculum from the current lesson:
                curriculum.append(lesson_path)
            else:
                print(this_lesson_name)
    print()
    user_input()
    return curriculum

def teaching_loop(progress, curriculum):
    """ frames interface main loop """
    # loop lessons
    for lesson_path in curriculum:
        current_lesson = Lesson(lesson_path)
        progress.current_lesson_num = current_lesson.number
        progress.save()
        frames_to_do = [x for x in range(current_lesson.number_of_frames)
                        if x not in progress.frames_complete]
        # Loop frames
        for i in frames_to_do:
            progress.current_frame_num = i
            progress.save()
            current_lesson.display_frame(i)
            if answer_loop(current_lesson.answers_to_frame(i)):
                progress.frames_complete.append(i)
            else: frames_to_do.append(i)
        progress.frames_complete = []

def answer_loop(answers):
    all_answers_correct = True
    # Loop through frame questions
    for i in range(len(answers)):
        prompt = ""
        # while incomplete prompt - repeat the same question
        while prompt != answers[i][0]:
            user_answer = user_input(prompt = str(i+1) + ': ',
                                     message = '[q]uit, [h]elp, or '
                                               '[?] to get prompt.')
            if user_answer in answers[i]:
                for answer in answers[i]:
                    print('  ', answer)
                print('Correct!')
                break
            else:
                all_answers_correct = False
                if user_answer == '?':
                    prompt = get_prompt(answers[i][0], prompt)
                    print(prompt)
                else:
                    for answer in answers[i]:
                        print('  ', answer)
                    print('Incorrect!')
                    break
    return all_answers_correct

def get_prompt(answer, prompt):
    """ Returns next prompt """
    return answer[:len(prompt) + 1]

def hsm_help():
    print("Not implemented yet, sorry :)")

class Lesson:
    """ Class for lesson object """
    def __init__(self, lesson_path):
        with open(lesson_path) as f:
            self.lesson = json.loads(f.read())
        self.number = self.lesson["lesson_number"]
        self.name = self.lesson["lesson_name"]
        self.exhibit = self.lesson["exhibit"]
        self.frames = self.lesson["frames"]
        self.number_of_frames = len(self.frames)
    def display_frame(self, frame_num):
        print(self.number.ljust(4), self.name.ljust(60), end = "")
        print("Frame", frame_num + 1, "/", self.number_of_frames, "\n")
        print(self.frames[frame_num][0], "\n")
    def answers_to_frame(self, frame_num):
        return self.frames[frame_num][1:]

class Progress:
    """ Class for progress object """
    def __init__(self, filepath):
        self.filepath = filepath
        with open(filepath) as f:
            self.progress = json.loads(f.read())
        self.current_lesson_num = self.progress["current_lesson_num"]
        self.frames_complete = self.progress["frames_complete"]
        self.current_frame_num = self.progress["current_frame_num"]

    def save(self):
        print('Saving progress')
        self.progress = {"current_lesson_num": self.current_lesson_num,
                         "frames_complete": self.frames_complete,
                         "current_frame_num": self.current_frame_num}
        with open(self.filepath, 'w') as f:
            f.write(json.dumps(self.progress))
        print('Done!')

def user_input(prompt="", message="[q]uit, [h]elp or [Enter] to proceed:"):
    """ user input handler """
    print(message)
    msg = input(prompt)
    if msg == 'q':
        sys.exit(print("User quit"))
    elif msg == 'h':
        hsm_help()
        return user_input(prompt, message)
    else: return msg

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
    progress = Progress(progress_file_path)
    display_welcome()
    # ordered list of lesson file paths, beginning from current lesson:
    curriculum = display_contents(course_folder_path, \
                                  progress.current_lesson_num)
    
    return teaching_loop(progress, curriculum)
    
if __name__ == '__main__':
    sys.exit(print(main()))

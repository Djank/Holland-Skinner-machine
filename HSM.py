#!/usr/bin/env python3
# Teaching machine by Holland and Skinner. Behavior analysis self-teaching.
import sys, os

def mylistdir(directory):
    """A specialized version of os.listdir() that ignores files that
    start with a leading period."""
    filelist = os.listdir(directory)
    return [x for x in filelist
            if not (x.startswith('.'))]


def display_welcome():
    """print welcome line on launch of program"""
    print()
    print("Welcome to Holland-Skinner Teaching Machine!\n".center(80))

def line_by_prefix(filepath, prefix):
    """takes file path and a line prefix
       finds the first occurence of prifix in the file
       returns the rest of the line (omitting the prefix)"""
    with open(filepath) as f:
        for line in f.readlines():
            if line.startswith("#"):        #ignore comments in file
                next
            if line.startswith(prefix):
                return line[len(prefix):-1] #strip off trailing \n

def display_contents(course_folder):
    """Prints course contents"""
    print("Course contents:")
    for setname in mylistdir(course_folder):
        setpath = os.path.join(course_folder, setname)
        print(line_by_prefix(setpath, "!set_number: "), end = ' ')
        print(line_by_prefix(setpath, "!set_name: "), )

def main():
    """Main entry point for the script"""
    # HSM.py file path
    hsm_folder_path = (os.path.split(os.path.realpath(__file__))[0])

    # resources folder path
    resources_path = os.path.join(hsm_folder_path, "resources")

    # course content files folder path
    course_folder_path = os.path.join(resources_path, "course")

    display_welcome()
    display_contents(course_folder_path)

if __name__ == '__main__':
        sys.exit(main())

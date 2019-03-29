# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:24:22 2019
   Vector RPS Module for use as port of larger projects (VecEngine)
@author: Daniel
"""

import time, os, sys, random
import Synonyms
#import speech_recognition as sr
import anki_vector
from anki_vector.util import degrees
try:
    from PIL import Image
except ImportError:
    sys.exit("Cannot import from PIL: Do `pip3 install --user Pillow` to install")
#commented out as Vector's SDK doesn't support mic access yet
#try:
#    from scipy.io import wavfile
#except ImportError as exc:
#    sys.exit("Cannot import scipy: Do `pip3 install scipy` to install")

def get_gesture_text(robot):
    #Keep waiting until you say the right thing
    while True:
        #ask for input
        robot.say_text("Rock, Paper, Scissors, SHOOT! ")
        thrown = input("Rock, Paper, or Scissors? ")
        #preprocess for logic
        thrown = thrown.lower()
        #parse each response and return a standard value
        if thrown == "rock" or thrown == "r":
            return "rock"
        elif thrown == "paper" or thrown == "p":
            return "paper"
        elif thrown == "scissors" or thrown == "s" or thrown == "scissor":
            return "scissors"
        else:
            #invalid input, do it again
            robot.say_text("Didn't catch that;")
            print("type rock, paper, or scissors, please.")
            
def rando_throw(robot):
    #get random value
    r = random
    #list of gestures
    gestures = ["rock", "paper", "scissors"]
    #pick a gesture
    throw = gestures[r.randint(0,2)]
    #report it
    current_directory = os.path.dirname(os.path.realpath(__file__))
    image_path = os.path.join(current_directory, ".", "Pictures\RPS_Images", throw + ".jpg")
	 # Load an image
    image_file = Image.open(image_path)	
    # Convert the image to the format used by the Screen
    screen_data = anki_vector.screen.convert_image_to_screen_data(image_file)
    robot.screen.set_screen_with_image_data(screen_data, 2.0)
    robot.say_text("I choose " + throw)
    print(throw)
    return throw

def decide(pc,vc):
    #you win!
    if (pc == "rock" and vc == "scissors") or (pc == "paper" and vc == "rock") or (pc == "scissors" and vc == "paper"):
        return 1
    
    #draw
    elif pc == vc:
        return 0
    #You lose...
    else:
        return -1

def print_results(robot, result):
    #Interpret results and report
    if(result == 1):
        print("You win!")
        robot.say_text("You win!")
        animation = "anim_blackjack_victorbjacklose_01"
        robot.anim.play_animation(animation)
    elif(result == 0):
        print("It's a draw.")
        robot.say_text("It's a draw.")
        animation = "anim_blackjack_victorlose_01"
        robot.anim.play_animation(animation)
    else:
        print("You lose...")
        robot.say_text("You lose...")
        animation = "anim_blackjack_victorbjackwin_01"
        robot.anim.play_animation(animation)

def greet(robot):
    robot.behavior.set_head_angle(degrees(45.0))
    robot.behavior.set_lift_height(0.0)
    robot.say_text("Let's play rock paper scissors!")
    time.sleep(1)

def another_round_text(robot):
    #Adjust head for easy viewing
    robot.behavior.set_head_angle(degrees(45.0))
    robot.behavior.set_lift_height(0.0)
        #Keep waiting until you say the right thing
    while True:
        #ask for input
        robot.say_text("Play another round?")
        ans = input("Another round? ")
        #preprocess for logic
        ans = ans.lower()
        #parse each response and return a standard value
        if ans in Synonyms.yes:
            return True
        elif ans in Synonyms.no:
            return False
        else:
            #invalid input, do it again
            robot.say_text("Didn't catch that;")
            print("type Yes or No, please.")

def main(robot):
    play = True
    greet(robot)
    while play:
    #get user input (R/P/S)
        player_choice = get_gesture_text(robot)
        #decide what vector should throw
        vector_choice = rando_throw(robot)
        #determine winner
        result = decide(player_choice,vector_choice)
        print_results(robot, result)
        #ask for another round
        play = another_round_text(robot)

if __name__ == '__main__':
    main()
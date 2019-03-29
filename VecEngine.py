# -*- coding: utf-8 -*-
"""
Created on Mon Mar 25 23:51:11 2019
    Wake Word subscription engine to call other vector modules
    Requires some way to loop and catch multiple wake calls
@author: Daniel
"""

import time
import importlib
import functools
import threading
import anki_vector
import Synonyms
from anki_vector.events import Events


wake_word_heard = False

def get_module_text(robot):
    
    #Keep waiting until you say the right thing
    while True:
        #ask for input
        robot.say_text("What module should I load?")
        module = input("Type the name of a module: ")
        
        #parse each response and return a standard value
        if module in Synonyms.wiki:
            module = "VecWiki"
        elif module in Synonyms.test:
            module = "VecTest"
        elif module in Synonyms.rps:
            module = "VecRPS"
        elif module in Synonyms.cancel:
            break
        try:
            mod = importlib.import_module(module)
            mod.main(robot)
            break
        except ModuleNotFoundError:
            #invalid input, do it again
            robot.say_text("I don't know " + module + ", sorry!")
            print("type a valid \".py\" program you wrote, please.")
        

def main():
    evt = threading.Event()
    #Called each time Vector hears "Hey, Vector"
    def on_wake_word(robot, event_type, event):
       
        #Bool to protect code from Vector's extra wake_word_heard events
        global wake_word_heard
        if not wake_word_heard:
            #Grab control from default behavior to query user and perform tasks
            robot.conn.request_control()
            wake_word_heard = True
            get_module_text(robot)
            evt.set()
            robot.conn.release_control()
        else:
            #on second wake_word_event, reset bool and alert cmd that it is ready
            wake_word_heard = False
            print('------ Vector is waiting to hear "Hey Vector!" Press ctrl+c to exit early ------')

    #Setup connection with Vector using default settings 
    #(use 'py -m anki_vector.configure' on windows to setup defaults)
    args = anki_vector.util.parse_command_args()
    with anki_vector.Robot(args.serial, requires_behavior_control=False, cache_animation_list=False) as robot:
        #Set up subscription to wake word events that are fired by Vector automatically
        on_wake_word = functools.partial(on_wake_word, robot)
        robot.events.subscribe(on_wake_word, Events.wake_word)

        print('------ Vector is waiting to hear "Hey Vector!" Press ctrl+c to exit early ------')
        try:
            #wait for wake word to event to occur
            while True:
                time.sleep(1)
        finally:
            robot.events.unsubscribe(on_wake_word, Events.wake_word)
if __name__ == '__main__':
    main()
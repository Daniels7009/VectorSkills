# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 00:40:14 2019
    VecEngine Module to search wikipedia
@author: Daniel
"""
import wikipedia
import re
import time
import Synonyms
from PIL import Image
import PIL
import requests
import random as r
from io import BytesIO
import anki_vector
from anki_vector.util import degrees

def ask_wiki(robot):
    #Keep waiting until you say the right thing
    while True:
        #ask for input
        robot.say_text("What should I look up for you?")
        subject = input("Enter a subject: ")

        #parse each response and return a standard value
        try:
            page = wikipedia.page(subject)
            return page, subject
        except: 
            #invalid input, do it again
            robot.say_text("Didn't catch that;")
            print("Something went wrong, try something else.")

def get_picture(page):
    #create list of valid pictures from the selected Wiki page
    pics = []
    for pic in page.images:
        if ".jpg" in pic or ".png" in pic:
            pics.append(pic)
            #print(pic)
    # and select one to display        
    pic = pics[r.randint(0, len(pics)-1)]
    #get image data from wikipedia
    response = requests.get(pic)
    img = Image.open(BytesIO(response.content))
    #adjust picture size to fit on Vector's screen
    img = img.resize((184, 96), PIL.Image.ANTIALIAS)
            
    return img

def get_summary(subject):
    #Get 2 sentences of summary from wikipedia on the subject
    desc = wikipedia.summary(subject, sentences=2)
    #Get rid of terrible characters that vector can't pronounce
    regex = re.compile('[^a-zA-Z \.,\'"!?()0123456789]')
    #return desc
    return regex.sub('', desc)
  

def main(robot):
    browsing = True
    while browsing:
        #Get page
        page, subject = ask_wiki(robot)
        #get Content
        desc = get_summary(subject)
        #print(desc)
        pic = get_picture(page)
        #display content
        #Adjust head for easy viewing
        robot.behavior.set_head_angle(degrees(45.0))
        robot.behavior.set_lift_height(0.0)
        #variable for length of time in seconds to show image based on 'desc' length
        #Estimating Vector to speak 2.4 words per second
        desc_time = len(desc.split())/2.4 
        #Display image on screen
        screen_data = anki_vector.screen.convert_image_to_screen_data(pic)
        robot.screen.set_screen_with_image_data(screen_data, desc_time)
        
        robot.say_text(desc)
 
        
        
        while True:
            #Wait, then ask if the user has another query
            time.sleep(1)
            robot.say_text("Look up something else?")
            keep_going = input("Look up something else? ")
            if keep_going in Synonyms.yes:
                browsing = True
                break
            elif keep_going in Synonyms.no:
                browsing = False
                break
            else:
                print("Yes or no?")
                robot.say_text("Didn't catch that;")
    
    
if __name__ == '__main__':
    main()
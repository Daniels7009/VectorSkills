# -*- coding: utf-8 -*-
"""
Created on Fri Mar 29 20:03:36 2019
    Module in the Vec- line, this one uses the cube's orientation as a die
@author: Daniel
"""
import time, Synonyms

def cube_setup(robot, max_attempts):
    print("disconnecting from any connected cube...")
    robot.world.disconnect_cube()

    time.sleep(2)
    attempts = 0
    while attempts < max_attempts:
        print("connect to a cube...")
        #animation = "anim_cubeconnection_loop_02"
        #robot.anim.play_animation(animation)
        connectionResult = robot.world.connect_cube()
        attempts = attempts + 1
        print(connectionResult)
        if robot.world.connected_light_cube:
            print("done connecting!")
            break

def get_roll(robot, cube):
    robot.say_text("Roll the cube!")
    while True:
        if cube.is_moving:
            while True:
                time.sleep(1)
                if not cube.is_moving:
                    robot.say_text(f"You rolled a {cube.up_axis}!")
                    break
            break

def another_roll_text(robot):
    while True:
        #Wait, then ask if the user has another query
        time.sleep(1)
        robot.say_text("Want to Roll again?")
        ans = input("Roll again? ").lower()
        if ans in Synonyms.yes:
            return True
        elif ans in Synonyms.no:
            return False
        else:
            print("Yes or no?")
            robot.say_text("Didn't catch that;")

def main(robot):
    cube_setup(robot, 3)
    rolling = True
    while rolling:
        print("start loop")
        connected_cube = robot.world.connected_light_cube
        print(connected_cube)
        if connected_cube:            
            print("Cube connected!")
            get_roll(robot, connected_cube)
            rolling = another_roll_text(robot)
        else:
            print("Lost connection with cube, shutting down...")
            break
            #cube_setup(robot, 3)
        time.sleep(0.5)
    
if __name__ == '__main__':
    main()
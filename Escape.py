##########
# Escape #
##########

# Created by Justin Bauer

from tkinter import *
from tkinter import ttk
import GameObject

NUMBER_OF_OBJECTS = 13

command_widget = None
image_label = None
description_widget = None
inventory_widget = None
north_button = None
south_button = None
east_button = None
west_button = None

root = None
switch = False

refresh_location = True
refresh_objects_visible = True

current_location = 24
end_of_game = False

radio_object_found = False
plans_object_found = False
key_object_found = False
turns_in_room_with_guard = 2
blast_door_openend = False  
arsenal_door_openend = False
armor = False
blaster = False
broken_blaster = False

broken_blaster_object = GameObject.GameObject("old blaster", 19, True, True, False, 'Droid tells you "The blaster appears to be broken."')
blaster_object = GameObject.GameObject("blaster", 25, True, True, False, 'Droid says "This blaster should work."')
radio_object = GameObject.GameObject("radio", 17, True, False, False, 'Droid says "Ooo, a radio. What could we use that for?"')
armor_object = GameObject.GameObject("armor", 10, True, True, False, 'Droid says "You should take this armor."')
switch_object = GameObject.GameObject("switch", 2, False, True, False, 'Droid says "This switch must be useful for something."')
plans_object = GameObject.GameObject("plans", 17, True, False, False, 'Droid says in shock "The death star plans!"')
key_object = GameObject.GameObject("key", 17, True, False, False, 'Droid says "A key!"')
console_object = GameObject.GameObject("console", 17, False, True, False, 'Droid says "There are important things in that console."')
blast_door_object = GameObject.GameObject("blast door", 8, False, True, False, 'Droid says "There must be a key."')
arsenal_door_object = GameObject.GameObject("arsenal door", 5, False, True, False, 'Droid says "There must be something to unlock this door."')
droid_object = GameObject.GameObject("droid", 21, False, True, False, 'Droid says "A droid!"')
old_droid_object = GameObject.GameObject("old droid", 12, False, True, False, 'Droid says "A droid!"')
guard_object = GameObject.GameObject("guard", 15, False, True, False, 'Droid says "A guard!"')

game_objects = [broken_blaster_object, blaster_object, radio_object, armor_object, switch_object, plans_object, key_object, console_object, blast_door_object, arsenal_door_object, droid_object, old_droid_object, guard_object]

def perform_command(verb, noun):
    
    if (verb == "GO"):
        perform_go_command(noun)
    elif ((verb == "N") or (verb == "S") or (verb == "E") or (verb == "W")):
        perform_go_command(verb)        
    elif ((verb == "NORTH") or (verb == "SOUTH") or (verb == "EAST") or (verb == "WEST")):
        perform_go_command(noun)        
    elif (verb == "GET"):
        perform_get_command(noun)
    elif (verb == "DROP"):
        perform_drop_command(noun)
    elif (verb == "LOOK"):
        perform_look_command(noun)        
    elif (verb == "SHOOT"):
        perform_shoot_command(noun)        
    elif (verb == "READ"):
        perform_read_command(noun)        
    elif (verb == "OPEN"):
        perform_open_command(noun)
    elif (verb == 'STATE'):
        set_current_state()
    elif (verb == 'PULL'):
        perform_pull_command(noun)
    elif (verb == "HELP"):
        preform_help_command()
    else:
        import random
        reply_number = random.randrange(1,7)
        if reply_number == 1:
            droid_response = 'Droid yells "YOU STUPID EWOK! THAT MAKES NO SENSE!"'
        elif reply_number == 2:
            droid_response = 'Droid asks "What are you saying?"'
        elif reply_number == 3:
            droid_response = 'Droid says "Are you speaking Wookiee?"'
        elif reply_number == 4:
            droid_response = 'Droid says "We should give up."'
        elif reply_number == 5:
            droid_response = 'Droid says "I should just leave you here."'
        else:
            droid_response = 'Droid says "We should have left you here to die."'
        print_to_description(droid_response)            
        
def perform_go_command(direction):

    global current_location
    global refresh_location
    
    if (direction == "N" or direction == "NORTH"):
        new_location = get_location_to_north()
    elif (direction == "S" or direction == "SOUTH"):
        new_location = get_location_to_south()
    elif (direction == "E" or direction == "EAST"):
        new_location = get_location_to_east()
    elif (direction == "W" or direction == "WEST"):
        new_location = get_location_to_west()
    else:
        new_location = 0
        
    if (new_location == 0):
        print_to_description('Droid says "You cant go that way."')
    else:
        current_location = new_location
        refresh_location = True

def perform_get_command(object_name):
    
    global refresh_objects_visible
    global armor
    global blaster
    global broken_blaster
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.location != current_location):
            print_to_description('Droid says "You do not see one of those here!"')
        elif (game_object.movable == False):
            print_to_description('Droid says "You can not pick it up!"')
        elif (game_object.carried == True):
            print_to_description('Droid says "You are already carrying it"')
        else:
            #handle special conditions
            if (game_object == armor_object):
                armor = True
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
            elif (game_object == blaster_object):
                blaster = True
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
            elif (game_object == broken_blaster_object):
                broken_blaster = True
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
            else:
                #pick up the object
                game_object.carried = True
                game_object.visible = False
                refresh_objects_visible = True
    else:
        print_to_description('Droid says "You do not see one of those here!"')

# 
def perform_drop_command(object_name):

    global refresh_objects_visible
    global blaster
    global broken_blaster
    game_object = get_game_object(object_name)
    
    if not (game_object is None):
        if (game_object.carried == False):
            print_to_description('Droid says "You are not carrying one of those."')
        else:
            if (game_object == blaster_object):
                game_object.location = current_location
                game_object.carried = False
                game_object.visible = True
                refresh_objects_visible = True
                blaster = False
            elif (game_object == broken_blaster_object):
                game_object.location = current_location
                game_object.carried = False
                game_object.visible = True
                refresh_objects_visible = True
                broken_blaster = False
            else:
                #drop down the object
                game_object.location = current_location
                game_object.carried = False
                game_object.visible = True
                refresh_objects_visible = True
    else:
        print_to_description('Droid says "You are not carrying one of those!"')
# 
def perform_look_command(object_name):

    global refresh_location
    global refresh_objects_visible
    global radio_object_found
    global plans_object_found
    global key_object_found
    
    game_object = get_game_object(object_name)
 
    if not (game_object is None):

        if ((game_object.carried == True) or (game_object.visible and game_object.location == current_location)):
            print_to_description(game_object.description)
        else:
            #recognized but not visible
            print_to_description('Droid says "You can not see one of those!"')
        #special cases - when certain objects are looked at, others are revealed!
        if (game_object == console_object):
            radio_object_found = True
            plans_object_found = True
            key_object_found = True
            radio_object.visible = True
            plans_object.visible = True
            key_object.visible = True
            console_object.description = 'Droid says "You have already searched the console."'
            global refresh_objects_visible
            refresh_objects_visible = True

    else:
        if (object_name == ""):
            #generic LOOK
            refresh_location = True
            refresh_objects_visible = True
        else:
            #not visible recognized
            print_to_description('Droid says "You can not see one of those!"')

def perform_shoot_command(object_name):

    game_object = get_game_object(object_name)
    global turns_in_room_with_guard
    global blaster
    global broken_blaster
    
    if (blaster == True):
        if not (game_object is None):
            if (game_object == droid_object):
                print_to_description('Droid says "Do not shoot them! They are friendly!"')
            elif (game_object == old_droid_object):
                print_to_description('Droid says "Do not shoot them! They are friendly!"')
            elif (game_object == guard_object):
                print_to_description('Droid says "Or do that."')
                turns_in_room_with_guard = 1000
            else:
                print_to_description('Droid comments "You can not destroy a '+ object_name +' with that, silly!"')
        else:
            #not visible recognized
            print_to_description('Droid warns "Watch it! That thing makes a lot of noise."')
    else:
        if (broken_blaster == True):
            print_to_description('Droid says "That blaster is broken!"')
        else:
            print_to_description('Droid says "You do not have a blaster, silly!"')


def perform_read_command(object_name):

    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == plans_object):
            print_to_description('Droid says "Those plans are very important to the rebellion. Keep them safe."')
        else:
            print_to_description('Droid says "What are you trying to read?"')
    else:
        print_to_description('Droid says "I am not sure what ' + object_name + 'you are referring to"')
# 
def perform_open_command(object_name):

    global blast_door_openend
    global arsenal_door_openend
    global switch
    game_object = get_game_object(object_name)
 
    if not (game_object is None):
        if (game_object == blast_door_object):
            if (key_object.carried):
                if (blast_door_openend == True):
                    print_to_description('Droid says "It is already open!"')
                else:
                    print_to_description('Droid says "The blast door has now been opened."')
                    blast_door_openend = True
                    blast_door_object.description = ('Droid says "It is open."')
            else:
                print_to_description('Droid says "It is locked."')
        elif (game_object == arsenal_door_object):
            if (switch == True):
                if (arsenal_door_openend == True):
                    print_to_description('Droid says "It is already open Wookie!"')
                else:
                    print_to_description('Droid says "The arsenal door has now been opened."')
                    arsenal_door_openend = True
                    arsenal_door_object.description = ('Droid says "It is open."')
            else:
                print_to_description('Droid says "The door is locked."')
        else:
            print_to_description('Droid says "You can not open that."')
    else:
        print_to_description('Droid says "Um, what?"')

def perform_pull_command(object_name):

    global switch
    game_object = get_game_object(object_name)

    if not (game_object is None):
        if (game_object == switch_object):
            switch = True
            print_to_description('Droid says "The switch has been activated."')
        else:
            print_to_description('Droid says "You can not activate that."')
    else:
        print_to_description('Droid says "Wait. Pull what?"')

def preform_help_command():

    print_to_description('Droid says "Haha, you need help."')
    print_to_description('get ______ to grab an object')
    print_to_description('drop ______ to drop an object')
    print_to_description('look ______ to get a description of an object')
    print_to_description('open ______ to open a door')
    print_to_description('shoot ______ to shoot things')
    print_to_description('pull ______ to pull something such as a switch')
    
def describe_current_location():
    global end_of_game
    if (current_location == 1):
        print_to_description('Droid says "That is a lot of guys"')
    elif (current_location == 2):
        print_to_description('Droid warns "Do not go that way until you have adequete protection"')
    elif (current_location == 3):
        print_to_description('Droid says "That is a nice view."')
    elif (current_location == 4):
        print_to_description('Droid says "So many hallways."')
    elif (current_location == 5):
        print_to_description('Droid says "Hmm, there must be something useful this way."')
    elif (current_location == 6):
        print_to_description('Droid says "Congratulations we have escaped!"')
        end_of_game = True
    elif (current_location == 7):
        print_to_description('Droid says "We need to get out there."')
    elif (current_location == 8):
        print_to_description('Droid tells you "I think this is our way out of here."')
    elif (current_location == 9):
        print_to_description('Droid says "There is no way to open this door."')
    elif (current_location == 10):
        print_to_description('Droid says "This is what you need."')
    elif (current_location == 11):
        print_to_description('Droid squeals "We are doomed!"')
        print_to_description('Darth Vader says "You can not handle the power of the dark side!"')
        print_to_description('Droid tells you "You appear to be choking."')
        end_of_game = True
    elif (current_location == 12):
        print_to_description('Droid says "Hello, old friend."')
    elif (current_location == 13):
        print_to_description('Droid says "Hallways just hallways."')
    elif (current_location == 14):
        print_to_description('Droid tells you "A corridor."')
    elif (current_location == 15):
        ''
    elif (current_location == 16):
        print_to_description('Droid warns "Do not go forward. There is danger ahead."')
    elif (current_location == 17):
        print_to_description('Droid says "There must be something useful here."')
    elif (current_location == 18):
        print_to_description('Droid describes "A corridor."')
    elif (current_location == 19):
        print_to_description('Droid tells you "It is just an empty hallway."')
    elif (current_location == 20):
        print_to_description('Droid says "Just a corridor."')
    elif (current_location == 21):
        print_to_description('Droid says "Ooo! A friend!"')
    elif (current_location == 22):
        print_to_description('Droid tells you "Another hallway."')
    elif (current_location == 23):
        print_to_description('Droid says "A walkway."')
    elif (current_location == 24):
        print_to_description("Escape - Created by Justin Bauer")
        print_to_description("You are a rebel fighter and you were captured by imperial forces.  You are trying to find your way off the ship with the aid of a rebel droid without getting caught or killed. Escape the imperial star destroyer with whatever you can.")
        print_to_description('For a list of commands type "help"')
        print_to_description('Droid says "I am here to help you escape! What are you waiting for, lets go!"')
    elif (current_location == 25):
        print_to_description('Droid says "There must be something useful here."')
    else:
        print_to_description("unknown location:" + str(current_location))

def set_current_image():

    if (current_location == 1):
        image_label.img = PhotoImage(file = 'res/room1_stormtroopers.gif')
    #https://www.google.ca/url?sa=i&rct=j&q=&esrc=s&source=images&cd=&cad=rja&uact=8&ved=0ahUKEwiJzI2EvorYAhUC2WMKHZZ7DVMQjRwIBw&url=http%3A%2F%2Fstarwars.wikia.com%2Fwiki%2FStormtrooper_Corps%2FLegends&psig=AOvVaw1C3BRAYu8Twakm5u7ykosT&ust=1513374394748169
    elif (current_location == 2):
        image_label.img = PhotoImage(file = 'res/room2_bridge.gif')
    #http://www.imperialofficer.com/forum/uploads/monthly_2016_09/imp_stardestroyer_bridge_new_m3_0009.jpg.a6ca3195ecf55451bcffd16adc2a0151.jpg
    elif (current_location == 3):
        image_label.img = PhotoImage(file = 'res/room3_view.gif')
    #https://thumbs.dreamstime.com/t/view-planet-earth-inside-space-station-window-69330337.jpg
    elif (current_location == 4):
        image_label.img = PhotoImage(file = 'res/room4_hallway.gif')
    #https://vignette2.wikia.nocookie.net/starwars/images/e/e4/Executor_commandsalon.jpg/revision/latest?cb=20071031004237
    elif (current_location == 5):
        image_label.img = PhotoImage(file = 'res/room5_hallway.gif')
    #https://s-media-cache-ak0.pinimg.com/originals/0a/80/b4/0a80b4c3c3ab35332a3e2e3b279b128b.png
    elif (current_location == 6):
        image_label.img = PhotoImage(file = 'res/room6_escape.gif')
    #http://starwarsblog.starwars.com/wp-content/uploads/2015/07/a-new-hope-pod-1536x864-738377028005.jpeg
    elif (current_location == 7):
        image_label.img = PhotoImage(file = 'res/room7_viewofdockingbay.gif')
    #https://vignette3.wikia.nocookie.net/playstationallstarsbattleroyale/images/6/65/Docking_Bay.jpg/revision/latest?cb=20120816021225
    elif (current_location == 8):
        image_label.img = PhotoImage(file = 'res/room8_door.gif')
    #https://img1.etsystatic.com/190/1/8818360/il_340x270.1391037219_8sgv.jpg
    elif (current_location == 9):
        image_label.img = PhotoImage(file = 'res/room9_fakedoor.gif')
    #https://static.turbosquid.com/Preview/2015/02/26__08_07_37/0098.jpgcb1282ad-88b9-4644-8aad-1bd9eae062faOriginal.jpg
    elif (current_location == 10):
        image_label.img = PhotoImage(file = 'res/room10_armor.gif')
    #https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSXJwMIprPd3CjmadFGwn0TAI6IsW1D5RR_L5GMTlzuU8I1roI
    elif (current_location == 11):
        image_label.img = PhotoImage(file = 'res/room11_darthvader.gif')
    #https://www.sideshowtoy.com/wp-content/uploads/2014/07/star-wars-darth-vader-life-size-feature-400184.jpg
    elif (current_location == 12):
        image_label.img = PhotoImage(file = 'res/room12_droid.gif')
    #https://vignette.wikia.nocookie.net/es.starwars/images/8/8d/5D6-RA-7.jpg/revision/latest?cb=20081218051445
    elif (current_location == 13):
        image_label.img = PhotoImage(file = 'res/room13_hallway.gif')
    #http://www.foundation3d.com/uploads/studio/2013/01/2-26-219355.jpg
    elif (current_location == 14):
        image_label.img = PhotoImage(file = 'res/room14_hallway.gif')
    #http://orig06.deviantart.net/2176/f/2014/295/1/b/star_destroyer_bridge_by_futuro04-d83q8hy.jpg
    elif (current_location == 15):
        global turns_in_room_with_guard
        if (turns_in_room_with_guard > 1):
            image_label.img = PhotoImage(file = 'res/room15_sleepingguard.gif') 
    #data:image/jpeg;base64,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
        else: 
            image_label.img = PhotoImage(file = 'res/room15_killedbyguard.gif')
    #http://bg0lden.files.wordpress.com/2011/01/stormtrooper-shooting1.jpg       
    elif (current_location == 16):
        image_label.img = PhotoImage(file = 'res/room16_hall.gif')
    #https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRpj2dUlGZALfWYR5mKCQmjrHXrqjwe98ku1d7Jd7Ph2szdGK9z
    elif (current_location == 17):
        image_label.img = PhotoImage(file = 'res/room17_commandcenter.gif')
    #https://img00.deviantart.net/b40e/i/2011/263/4/b/command_center_interior_by_alexdrummo-d4adu58.jpg
    elif (current_location == 18):
        image_label.img = PhotoImage(file = 'res/room18_corridor.gif')
    #https://vignette.wikia.nocookie.net/fantendo/images/9/97/Death_Star_%28PS4-Vita_only%29.jpg/revision/latest?cb=20151209224015
    elif (current_location == 19):
        image_label.img = PhotoImage(file = 'res/room19_hallway.gif')
    #https://i.pinimg.com/236x/94/12/a5/9412a5bbd1d06b632ebfda1d0e9b02f2--star-wars-room-star-wars-art.jpg
    elif (current_location == 20):
        image_label.img = PhotoImage(file = 'res/room20_hallway.gif')
    #http://alienscollection.com/deathstar/deathstarhall1.jpg
    elif (current_location == 21):
        image_label.img = PhotoImage(file = 'res/room21_droid.gif')
    #https://vignette.wikia.nocookie.net/starwars/images/c/c1/R-2Q5.jpg/revision/latest?cb=20160430004853
    elif (current_location == 22):
        image_label.img = PhotoImage(file = 'res/room22_emptyhallway.gif')
    #https://cdnb.artstation.com/p/assets/images/images/001/609/685/large/donny-versiga-dscorridor1.jpg?1449447691
    elif (current_location == 23):
        image_label.img = PhotoImage(file = 'res/room23_hallway.gif')
    #http://www.darth-vader.ch/tswp/previews/pic/imp_stardestroyer_bridge_new_m2_0003.jpg
    elif (current_location == 24):
        image_label.img = PhotoImage(file = 'res/room24_cell.gif')
    #https://i.pinimg.com/736x/0c/15/4b/0c154bfe7aa304b4fcc319bfb13f1c18--asylum-prison.jpg
    else:
        image_label.img = PhotoImage(file = 'res/room25_blasters.gif')
    #https://orig00.deviantart.net/374e/f/2011/237/3/7/armory_by_joker2559-d47miqp.jpg
    
    image_label.config(image = image_label.img)
        

def get_location_to_north():
    
    if (current_location == 8):
        return (3 if blast_door_openend else 0)
    elif (current_location == 10):
        return 5
    elif (current_location == 12):
        return 7
    elif (current_location == 13):
        return 8
    elif (current_location == 16):
        return 11
    elif (current_location == 18):
        return 13
    elif (current_location == 21):
        return 16
    elif (current_location == 23):
        return 18
    elif (current_location == 24):
        return 19
    elif (current_location == 25):
        return 20
    else:
        return 0

def get_location_to_south():
    
    if (current_location == 1):
        return (0 if end_of_game else 6)
    elif (current_location == 5):
        return (10 if arsenal_door_openend else 0)
    elif (current_location == 7):
        return 12
    elif (current_location == 8):
        return 13
    elif (current_location == 13):
        return 18
    elif (current_location == 16):
        return 21
    elif (current_location == 18):
        return 23
    elif (current_location == 20):
        return 25
    else:
        return 0

def get_location_to_east():
    
    if (current_location == 1):
        return (0 if end_of_game else 2)
    elif (current_location == 2):
        return 3
    elif (current_location == 3):
        return 4
    elif (current_location == 4):
        return 5
    elif (current_location == 7):
        return 8
    elif (current_location == 8):
        return 9
    elif (current_location == 12):
        return 13
    elif (current_location == 13):
        return 14
    elif (current_location == 14):
        return 15
    elif (current_location == 16):
        return 17
    elif (current_location == 18):
        return 19
    elif (current_location == 19):
        return 20
    elif (current_location == 21):
        return 22
    elif (current_location == 22):
        return 23
    else:
        return 0

def get_location_to_west():
    
    if (current_location == 2):
        return 1
    elif (current_location == 3):
        return 2
    elif (current_location == 4):
        return 3
    elif (current_location == 5):
        return 4
    elif (current_location == 8):
        return 7
    elif (current_location == 9):
        return 8
    elif (current_location == 13):
        return 12
    elif (current_location == 14):
        return 13
    elif (current_location == 15):
        return (0 if end_of_game else 14)
    elif (current_location == 17):
        return 16
    elif (current_location == 19):
        return 18
    elif (current_location == 20):
        return 19
    elif (current_location == 22):
        return 21
    elif (current_location == 23):
        return 22
    else:
        return 0

def handle_special_condition():
    
    global turns_in_room_with_guard
    global end_of_game
    
    if (current_location == 15):
        turns_in_room_with_guard = turns_in_room_with_guard - 1
        if (turns_in_room_with_guard == 1):
            print_to_description('Droid warns "We got to get out of here, we do not want him waking up."')
        elif (turns_in_room_with_guard == 0):
            print_to_description('Droid says "You have been shot!"')
            print_to_description('GAME OVER')
            end_of_game = True
    if (current_location == 1):
        if armor:
            print_to_description('Droid says "Good thing you have a disguise."')
        else:
            print_to_description('Droid says "You have been shot!"')
            print_to_description('GAME OVER')
            end_of_game = True
            

def print_to_description(output, user_input=False):
    description_widget.config(state = 'normal')
    description_widget.insert(END, output)
    if (user_input):
        description_widget.tag_add("blue_text", CURRENT + " linestart", END + "-1c")
        description_widget.tag_configure("blue_text", foreground = 'blue')
    description_widget.insert(END, '\n')        
    description_widget.config(state = 'disabled')
    description_widget.see(END)
        
def get_game_object(object_name):
    sought_object = None
    for current_object in game_objects:
        if (current_object.name.upper() == object_name):
            sought_object = current_object
            break
    return sought_object

def describe_current_visible_objects():
    
    object_count = 0
    object_list = ""
    global turns_in_room_with_guard
    
    for current_object in game_objects:
        if ((current_object.location  == current_location) and (current_object.visible == True) and (current_object.carried == False)):
            object_list = object_list + (", " if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    if object_count > 0:
        print_to_description('Droid says "There is a ' + object_list + '."')
    elif current_location == 6:
        print_to_description('GAME OVER')
    elif current_location == 11:
        print_to_description('GAME OVER')
    elif current_location == 15 and turns_in_room_with_guard < 2:
        ''
    elif current_location == 24:
        ''
    elif current_location == 1:
        ''
    else:
        print_to_description('Droid says "There is nothing useful here."') 

def describe_current_inventory():
    
    object_count = 0
    object_list = ""

    for current_object in game_objects:
        if (current_object.carried):
            object_list = object_list + (", " if object_count > 0 else "") + current_object.name
            object_count = object_count + 1
    
    inventory = "Inventory: " + (object_list if object_count > 0 else "nothing")
    
    inventory_widget.config(state = "normal")
    inventory_widget.delete(1.0, END)
    inventory_widget.insert(1.0, inventory)
    inventory_widget.config(state = "disabled")
             
def build_interface():
    
    global command_widget
    global image_label
    global description_widget
    global inventory_widget
    global north_button
    global south_button
    global east_button
    global west_button    
    global root

    root = Tk()
    root.resizable(0,0)
    
    style = ttk.Style()
    style.configure("BW.TLabel", foreground="black", background="white")

    image_label = ttk.Label(root)    
    image_label.grid(row=0, column=0, columnspan =3,padx = 2, pady = 2)

    description_widget = Text(root, width =50, height = 10, relief = GROOVE, wrap = 'word')
    description_widget.config(state = "disabled")
    description_widget.grid(row=1, column=0, columnspan =3, sticky=W, padx = 2, pady = 2)

    command_widget = ttk.Entry(root, width = 25, style="BW.TLabel")
    command_widget.bind('<Return>', return_key_enter)
    command_widget.grid(row=2, column=0, padx = 2, pady = 2)
    
    button_frame = ttk.Frame(root)
    button_frame.config(height = 150, width = 150, relief = GROOVE)
    button_frame.grid(row=3, column=0, columnspan =1, padx = 2, pady = 2)

    north_button = ttk.Button(button_frame, text = "N", width = 5)
    north_button.grid(row=0, column=1, padx = 2, pady = 2)
    north_button.config(command = north_button_click)
    
    south_button = ttk.Button(button_frame, text = "S", width = 5)
    south_button.grid(row=2, column=1, padx = 2, pady = 2)
    south_button.config(command = south_button_click)

    east_button = ttk.Button(button_frame, text = "E", width = 5)
    east_button.grid(row=1, column=2, padx = 2, pady = 2)
    east_button.config(command = east_button_click)

    west_button = ttk.Button(button_frame, text = "W", width = 5)
    west_button.grid(row=1, column=0, padx = 2, pady = 2)
    west_button.config(command = west_button_click)
    
    inventory_widget = Text(root, width = 30, height = 8, relief = GROOVE , state=DISABLED )
    inventory_widget.grid(row=2, column=2, rowspan = 2, padx = 2, pady = 2,sticky=W)
    
def set_current_state():

    global refresh_location
    global refresh_objects_visible

    if (refresh_location):
        describe_current_location()
        set_current_image()
    
    if (refresh_location or refresh_objects_visible):
        describe_current_visible_objects()

    handle_special_condition()    
    set_directions_to_move()                
    if (end_of_game == False):
        describe_current_inventory()
    
    refresh_location = False
    refresh_objects_visible = False
    
    command_widget.config(state = ("disabled" if end_of_game else "normal"))


def north_button_click():
    print_to_description("N", True)
    perform_command("N", "")
    set_current_state()

def south_button_click():
    print_to_description("S", True)
    perform_command("S", "")
    set_current_state()

def east_button_click():
    print_to_description("E", True)
    perform_command("E", "")
    set_current_state()

def west_button_click():
    print_to_description("W", True)
    perform_command("W", "")
    set_current_state()

def return_key_enter(event):
    if( event.widget == command_widget):
        command_string = command_widget.get()
        print_to_description(command_string, True)

        command_widget.delete(0, END)
        words = command_string.split(' ', 1)
        verb = words[0]
        noun = (words[1] if (len(words) > 1) else "")
        perform_command(verb.upper(), noun.upper())
        
        set_current_state()

def set_directions_to_move():

    move_to_north = (get_location_to_north() > 0)
    move_to_south = (get_location_to_south() > 0)
    move_to_east = (get_location_to_east() > 0)
    move_to_west = (get_location_to_west() > 0)
    
    north_button.config(state = ("normal" if move_to_north else "disabled"))
    south_button.config(state = ("normal" if move_to_south else "disabled"))
    east_button.config(state = ("normal" if move_to_east else "disabled"))
    west_button.config(state = ("normal" if move_to_west else "disabled"))    

def main():
    
    build_interface()
    set_current_state()
    root.mainloop()
        
main()


# fallout-like terminal password guessing by ThePiroman
# now using pygame
# COPYRIGHT LOLLOLLOL

import pygame
from random import choice
from random import randint
import os

pg = pygame

pg.init()
pg.font.init()
pg.mixer.init()


words_db = ["bake", "word", "kids", "tree", "race",
            "coop", "zero", "game", "hide", "cool",
            "rice", "hope", "from"]
attempts = 5
word = choice(words_db)


bg_color = (0, 0, 0)
text_color = (0, 255, 0)

run = True

w, h = 900, 600
screen = pg.display.set_mode((w, h))

clock = pg.time.Clock()

icon = pg.image.load("icon.png")

pg.display.set_caption("Out Fall Terminal™")
pygame.display.set_icon(icon)

font = pg.font.SysFont("Prototype", size = 24)

text_surface = font.render("Words Database: " + str(words_db[0:9]), False, text_color)
text_surface_1 = font.render(str(words_db[9:]), False, text_color)
block_surface = font.render("--TERMINAL BLOCKED--", False, text_color)

user_text = ""
similarities = len((set(user_text)).intersection(set(word))) # this is a int for how many common letters does user word and password word have

generated_exp = 0

enter = pg.K_RETURN

notify = True
block = False
should_show_exp = False
should_play_block_sound = True
ascii_warn = False
caps_warn = False
unlock = False
exp_sound = True


# sounds database
s_keyboard = ["keyboard_1.wav", "keyboard_2.wav", "keyboard_3.wav", "keyboard_4.wav", "keyboard_5.wav",
              "keyboard_6.wav", "keyboard_7.wav", "keyboard_8.wav", "keyboard_9.wav", "keyboard_10.wav"]
s_mouse = ["mouse_click_1.wav", "mouse_click_2.wav", "mouse_click_3.wav",
           "mouse_click_4.wav", "mouse_click_5.wav", "mouse_click_6.wav"]
s_exp = ["xp_gain_1.wav", "xp_gain_2.wav"]


def create_message(message = "This is a message", x = 0, y = 0):
    if block: return False
    message_surface = font.render(message, False, text_color)
    
    screen.blit(message_surface, (x, y))

# this function is responsible for displaying user input
def user_text_logic():
    if block: return False
    
    user_text_surface = font.render("Enter a word: " + user_text, True, text_color)
    bar = font.render("|", True, text_color)
        
    screen.blit(user_text_surface, (5, 450))
    screen.blit(bar, (user_text_surface.get_width() + 5, 450))

# this function responsible for desplaying attempts left
def attempts_text_logic():
    if block: return False
    
    global attempts
    attempts_surface = font.render(f"Attempts left:  {attempts}", False, text_color)

    screen.blit(attempts_surface, (0, 75))

def create_warning(warning = "This is a warning", should_caps = True, x = 0, y = 0):
    if block: return False
    if should_caps == True:
        warning = warning.upper()
    warning_surface = font.render("WARNING:" + warning, False, text_color)

    screen.blit(warning_surface, (x, y))


def calculate_exp():
    exp_to_give = 1000 * attempts
    return exp_to_give
    

def play_sound(sound_type):
    if type(sound_type) == list:
        sound_name = choice(sound_type)
    else:
        sound_name = sound_type
        
    sound = pg.mixer.Sound(sound_name)
    
    pg.mixer.Sound.play(sound)

    # if debugging: print(sound_name)
    
    
# this function is responsible for playing a sound when user has 1 attempt left
def last_attempt_logic():
    global notify
    if notify:
        play_sound("last_attempt.wav")
        notify = False

# this function is responsible for playing a sound when user has successfuly blocked the terminal
def block_logic():
    global should_play_block_sound
    if should_play_block_sound:
        play_sound("wrong_word.wav")
        should_play_block_sound = False
    
# this function is responsible for playing a sound when exp is given and printing a message
def exp_logic():
    global exp_sound
    if exp_sound:
        play_sound(s_exp)
        exp_sound = False

    create_message("EXP gained: " + str(generated_exp), 0, 410)
    
def char_limit():
    return len(user_text) >= 4

def is_right():
    return user_text == word

# this function initializes words with duplicate letters, which then passes to function that fixes it
def initialize_duplicates():
    words_to_fix = [] # we will put words here
    common_letters = [] # we will put duplicate letters here
    
    for item in words_db:
        
        if len(item) != len(set(item)): # if we have duplicate letters
            words_to_fix.append(item)

    for item in words_to_fix:
        
        for letter in item:
            if item.count(letter) > 1:
                
                common_letters.append(letter)
                
    return words_to_fix, common_letters

# this function fixes similiraties output
def attempt_dumb_letter_duplicate_fix():
    global similarities
    
    if not word in initialize_duplicates()[0]: return False # if the password doesn't need a fix, end the function here
    
    else:
        needed_letter = ""
        for item in initialize_duplicates()[1]:
            
            if word.find(item):
                
                if word.count(item) > 1:
                    needed_letter = item
                    
        if needed_letter in user_text:
            similarities += 1 
    


# due to current pygame having a bad sound loop, i pulled this one from their github reports https://github.com/pygame/pygame/issues/3686
sound_a = pygame.mixer.Sound("terminal_loop.wav")
sound_b = pygame.mixer.Sound("terminal_loop.wav")
playing_sound = sound_a
loop_timer = 33000
loop_acc = 0
playing_sound.set_volume(0.1)
playing_sound.play() 

#print(word)

while run:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            run = False

        if event.type == pg.MOUSEBUTTONDOWN:
            play_sound(s_mouse)


        if event.type == pg.KEYDOWN:

            if block: # this and should_show_exp will close the program when an input from user is given
                run = False

            if should_show_exp:
                run = False

            if event.key == enter:

                if unlock: # if we guessed the word, show exp
                    should_show_exp = True
                    
                play_sound("enter.wav")
            
                # overriding the initial variable for similar letters
                similarities = len((set(user_text)).intersection(set(word)))

                # attempt a duplicate fix
                attempt_dumb_letter_duplicate_fix()
                
                if not block and is_right() == False and not unlock: # if terminal isn't blocked or unlocked and the word is wrong
                    attempts -= 1
                    user_text = "" # empty the user text

                if is_right() and not unlock: # if the word is right
                    play_sound("unlock.wav")
                    generated_exp = calculate_exp()
                    
                    unlock = True

                    
                
            if event.key == pg.K_BACKSPACE:
                
                # delete a letter
                if not block and not unlock:
                    
                    user_text = user_text[:-1]
                play_sound(s_keyboard)
  
            else:
                if char_limit() and event.key != enter: # if we hit a 4 letter limit
                    
                    if not block and not unlock:
                        play_sound("limit.wav")
                        
                    else:
                        play_sound(s_keyboard)
                
                if not char_limit() and event.key != enter and event.key != pg.K_KP_ENTER: # if we aren't at the limit, and the key isn't enter
                    
                    if not block and not unlock:

                        if not event.unicode.isascii(): # if user is  using diffrent language
                            ascii_warn = True
                            
                        elif event.unicode.isupper(): # if user is writting with caps (did this because it conflicts with word recognition)
                            caps_warn = True
                            
                        else:
                            
                            ascii_warn = False
                            caps_warn = False
                            user_text += event.unicode
                        
                    play_sound(s_keyboard)


    # sound loop fix   
    time_delta_ms = clock.tick()
    loop_acc += time_delta_ms
    
    if loop_acc >= loop_timer:
        loop_acc = loop_acc - loop_timer
        playing_sound.fadeout(250-loop_acc)
        if playing_sound == sound_a:
            playing_sound = sound_b
        if playing_sound == sound_b:
            playing_sound = sound_a
            
        playing_sound.play(fade_ms=250-loop_acc)
    
    screen.fill(bg_color)
    
    create_message(str(similarities) + " out of 4", 0, 100)
    
    if block:
        
        screen.blit(block_surface, (w / 3, h / 2))
        block_logic()

    else:
        
        screen.blit(text_surface, (0, 0))
        screen.blit(text_surface_1, (0, 30))

    if unlock:
        
        create_message("Terminal unlocked!", 0, 380)

    if attempts == 1:
        
        create_warning("Terminal Shutdown Risk!", True, 0, 200)
        last_attempt_logic()
        
    if attempts < 1:
        block = True

    if ascii_warn:
        
        create_warning("Trying to input non-ASCII characters!", False, 0, 400)
        
    elif caps_warn:
        
        create_warning("Trying to input characters with CAPS-LOCK on!", False, 0, 400)

    user_text_logic()
    attempts_text_logic()
    if should_show_exp:
        exp_logic()
      
    pygame.display.flip()

quit()

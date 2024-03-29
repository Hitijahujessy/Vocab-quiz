import os
import sys

from kivy.clock import Clock

# os.environ['KIVY_GL_BACKEND'] = 'angle_sdl2'

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import NumericProperty, ObjectProperty
from kivy.uix.dropdown import DropDown
from kivy.uix.popup import Popup

from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import ScreenManager, Screen
import pandas as pd
import random
from gtts import gTTS
from kivy.core.audio import SoundLoader

# Import Kivy Layout
root_widget = Builder.load_file('app.kv')

# Create class for main widget
class ExampleWidget(Screen):
    # Import the wordlists contained in the .csv file
    df = pd.read_csv('translations.csv')

    word_order = []  # Will be used to prevent duplicate words and to randomize the order of words
    i = 0  # Used for proceeding to next word
    maincolor = ObjectProperty((.25, .6, 1, 1))
    time = NumericProperty(0)
    start_game = ObjectProperty()

    origin_language = 'English'
    origin_flag = ObjectProperty()
    origin_flag = '120x90/gb.png'
    origin_sound = 'en'

    input_language = 'Dutch'
    input_flag = ObjectProperty()
    input_flag = '120x90/nl.png'



    def __init__(self, **kwargs):

        super(ExampleWidget, self).__init__(**kwargs)

        # Wordlist must be set before app is started
        self.set_wordlist()

    # Function for randomizing the word order for the list
    def set_wordlist(self):

        # For-loop to set word order
        for x in range(len(self.df[self.origin_language])):

            # While-loop to prevent duplicates in word_order list
            while True:
                number = random.randint(0, (
                            len(self.df[self.origin_language]) - 1))  # Random number between 0 and length of wordlist is chosen

                if number in self.word_order:
                    continue  # If chosen number already exists in word_order list, continue the loop
                else:
                    self.word_order.append(
                        number)  # If chosen number does not exist in word_order list, append it to the list.
                    # print(self.word_order)  # Print the word_order list to check if everything works
                    break

        # Keeping time
    def increment_time(self, interval):

        self.time += .1
        print(self.time)  # To check if stopwatch is running or not

    # Stop should mean that the stopwatch must reset when it starts again.
    # When paused it should resume when it starts again

    def start(self):

        # Keeping time
        self.time = 0
        Clock.schedule_interval(self.increment_time, .1)

        self.ids.origin_word.text = self.df[self.origin_language][(self.word_order[self.i])]

        self.ids.origin_icon.source = self.origin_flag
        self.ids.origin_icon.color = (1, 1, 1, 1)

        self.ids.input_icon.source = self.input_flag
        self.ids.input_icon.color = (1, 1, 1, 1)

        self.ids.sound_button.disabled = False

        self.ids.start_game.disabled = True


    def stop(self):

        Clock.unschedule(self.increment_time)
        print('Stopped')

    def pause(self):

        # Pause stopwatch
        if self.paused:
            Clock.unschedule(self.increment_time)
            print("!!", self.time)  # To make it easier to see if stopwatch actually resumes where it left off
            print('unscheduled')  # Just to confirm and to make it a bit easier to see

        # resume stopwatch
        elif not self.paused:
            Clock.schedule_interval(self.increment_time, .1)

    # Function for checking if typed word is correct when pressed enter
    def on_enter(self):

        # This is to prevent the app from telling the answer is wrong before anything is typed
        if self.ids.input.text == '':
            pass
        # If answer is correct
        elif self.ids.input.text.capitalize() == self.df[self.input_language][(self.word_order[self.i])]:
            #print('correct')  # Feedback in console to check if it works, can be removed when it's no longer needed
            self.ids.origin_word.color = (0, 1, 0)  # Set textlabel color to green (RGB)
            self.ids.next.disabled = False  # Button for proceeding to next word will be enabled
            self.i += 1  # Proceed to next word
        else:
            #print('incorrect')  # Feedback in console to check if it works, can be removed when it's no longer needed
            self.ids.origin_word.color = (1, 0, 0)  # Set textlabel color to red (RGB)

    # Function for proceeding to next word
    def next_word(self):
        self.ids.next.disabled = True  # Button for proceeding to next word will be disabled
        self.ids.input.text = ''  # Clear text input widget
        self.ids.origin_word.color = (1, 1, 1)  # Set textlabel color to white (RGB)
        self.ids.origin_word.text = self.df[self.origin_language][(self.word_order[self.i])]  # Set textlabel text to new word

    def play_sound(self):
        myobj = gTTS(text=self.ids.origin_word.text, lang=self.origin_language, slow=False)
        myobj.save("word.mp3")
        sound = SoundLoader.load('word.mp3')
        sound.play()

    def ColorChange(self):
        self.maincolor = (random.uniform(0, 1), random.uniform(0, 1), random.uniform(0, 1), 1)
        print(self.maincolor)

    def reload(self):
        self.stop()


        self.ids.sound_button.disabled = True

        self.ids.next.disabled = True  # Button for proceeding to next word will be disabled
        self.ids.input.text = ''  # Clear text input widget
        self.ids.origin_word.text = ''
        self.ids.origin_word.color = (1, 1, 1)  # Set textlabel color to white (RGB)

        self.word_order = []  # Will be used to prevent duplicate words and to randomize the order of words
        self.i = 0  # Used for proceeding to next word
        self.time = 0

        self.ids.start_game.disabled = False

        self.ids.origin_icon.source = self.origin_flag
        self.ids.origin_icon.color = (0, 0, 0, 0)

        self.ids.input_icon.source = self.input_flag
        self.ids.input_icon.color = (0, 0, 0, 0)

        self.set_wordlist()



# Menu screen class
class Menu(Screen, BoxLayout):
    pass


# Widget class for using multiple screens
class WindowManager(ScreenManager):
    pass


# App class for running the app
class QuizApp(App):
    WindowManager = WindowManager()

    def build(self):
        return self.WindowManager

# Run the app
QuizApp().run()

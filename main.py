# manipulate the python terminal window for funny

# get packages
import time
import math
import random

# for window manipulation
import pyautogui
import pywinauto
import tkinter as tk


class WindowManipulation:

    def fail_safe(self):
        """if mouse is in top left corner, exit the program"""
        if pyautogui.position() == (0, 0):
            raise Exception("Fail safe executed, mouse in top left corner")
        
    def attach_window(self):
        """attach the window to the python script"""
        # in order of preference
        # 1 - python terminal
        # 2 - windows powershell
        # 3 - windows command prompt
        # thats it for now

        # get the terminal window
        try:
            self.app = pyautogui.getWindowsWithTitle("Python")[0]
        except IndexError:
            try:
                self.app = pyautogui.getWindowsWithTitle("Windows PowerShell")[0]
            except IndexError:
                try:
                    self.app = pyautogui.getWindowsWithTitle("Command Prompt")[0]
                except IndexError:
                    print("No terminal window found")
                    raise Exception("No terminal window found")
                
        print("Window found: ", self.app.title)

        return self.app

    def __init__(self):
        # get terminal window, or windows powershell
        #self.app = pyautogui.getActiveWindow()
        self.app = self.attach_window()
        self.screen_size = pyautogui.size()

    def center_window(self):
        window_width = int(self.screen_size.width/4)
        window_height = int(self.screen_size.height/4)

        self.app.moveTo(window_width, window_height)
    
    def shake_window(self, intensity = 150, intensity_drop = 0.96, ilterations = 100):
        """shake the window by a certain intensity for a certain number of ilterations"""
    
        # intensity = the intensity of the shake by pixel movement
        # intensity_drop = the amount the intensity drops each ilteration in percentage
        # ilterations = the number of ilterations the shake will last

        x_current, y_current = self.app.left, self.app.top

        for i in range(ilterations):
            int_intensity = int(intensity)
            x_offset = random.randint(-int_intensity, int_intensity)
            y_offset = random.randint(-int_intensity, int_intensity)

            self.app.moveTo(x_current + x_offset, y_current + y_offset)

            time.sleep(0.01)
            intensity = intensity * intensity_drop

    def sine_wave(self, amplitude = 100, frequency = 10, ilterations = 100):
        """create a sine wave effect on the window"""

        x_current, y_current = self.app.left, self.app.top

        for i in range(ilterations):
            x_offset = int((frequency * i))
            y_offset = int(amplitude * math.cos(frequency * i))

            self.app.moveTo(x_current + x_offset, y_current + y_offset)

            time.sleep(0.01)

    def dvd_bounce(self):
        """simulate the dvd screensaver"""

        # set window to random position
        self.app.moveTo(random.randint(0, int(self.screen_size.width/2)), random.randint(0, int(self.screen_size.height/2)))

        x_current, y_current = self.app.left, self.app.top
        x_offset = 1
        y_offset = 1
        speed_multiplier = 5

        # loop until the window is closed
        while True:
            window_size = self.app.size # hitbox of the window
            window_width = window_size.width
            window_height = window_size.height

            # move the window by the offset  
            x_current += x_offset * speed_multiplier
            y_current += y_offset * speed_multiplier

            # check if the window is at the edge of the screen
            if x_current + window_width >= self.screen_size.width or x_current <= 0:
                x_offset *= -1
                x_current += x_offset

            if y_current + window_height >= self.screen_size.height or y_current <= 0:
                y_offset *= -1
                y_current += y_offset

            # move the window
            self.app.moveTo(x_current, y_current)
            time.sleep(0.01)
            self.fail_safe()

    def tween_to_mouse(self):
        """tween the window to the mouse, like a dog following a treat"""
            
        while True:
            mouse_position = pyautogui.position()
            window_x, window_y = self.app.left, self.app.top

            x_diff = mouse_position[0] - window_x
            y_diff = mouse_position[1] - window_y

            x_new = window_x + x_diff/10
            y_new = window_y + y_diff/10

            x_new = int(x_new)
            y_new = int(y_new)

            self.app.moveTo(x_new, y_new)
            time.sleep(0.01)
            self.fail_safe()


# menu for the window manipulation
def window_menu():
    root = tk.Tk()
    root.title("Window Manipulation")
    root.geometry("600x300")
    window_manipulation = WindowManipulation()

    # functions

    def center_window():
        window_manipulation.center_window()

    def shake_window():
        window_manipulation.shake_window()

    def sine_wave():
        window_manipulation.sine_wave()
    
    def dvd_bounce():
        window_manipulation.dvd_bounce()

    def tween_to_mouse():
        window_manipulation.tween_to_mouse()

    # buttons

    center_button = tk.Button(root, text="Center Window", command=center_window)
    center_button.pack()
    
    shake_button = tk.Button(root, text="Shake Window", command=shake_window)
    shake_button.pack()

    sine_wave_button = tk.Button(root, text="Sine Wave", command=sine_wave)
    sine_wave_button.pack()

    dvd_bounce_button = tk.Button(root, text="DVD Bounce", command=dvd_bounce)
    dvd_bounce_button.pack()

    tween_to_mouse_button = tk.Button(root, text="Terminal follows Mouse", command=tween_to_mouse)
    tween_to_mouse_button.pack()

    # text
    text = tk.Label(root, text="Select a function to run")
    text.pack()
    text2 = tk.Label(root, text="move the mouse to the top left corner to exit in case of emergency")
    text2.pack()

    root.mainloop()

if __name__ == "__main__":
    window_menu()
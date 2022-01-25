from tkinter import *
from tkinter import ttk
import json
import os


def start_game():
    # writes settings in json for future using
    if os.path.exists('settings.json'):
        with open('settings.json', 'r') as file:
            data = json.load(file)
            fps = int(fps_choice.get())
            sounds = True if enabled_sounds.get() == 1 else False
            current_data = {'fps': fps, 'sounds': sounds}

        if data != current_data:
            with open('settings.json', 'w') as file:
                json.dump(current_data, file)

    else:
        with open('settings.json', 'w') as file:
            fps = int(fps_choice.get())
            sounds = True if enabled_sounds.get() == 1 else False
            data = {'fps': fps, 'sounds': sounds}
            json.dump(data, file)

    os.startfile('game.py')
    root.destroy()


root = Tk()
root.geometry('300x250')
root.resizable(0, 0)
root.title('Space Adventures')

enabled_sounds = IntVar()

FPS_LIST = [144, 60]

button_play = Button(root, text='Play', font=('Arial Bold', 20),
                     command=start_game)
fps_choice = ttk.Combobox(root, values=FPS_LIST, width=10)
fps_choice.current(0)
text_fps = Label(root, text='FPS', font=('Arial Bold', 15))
enable_sounds_button = Checkbutton(root, text='Enable Sounds',
                                   font=('Arial Bold', 10),
                                   variable=enabled_sounds, onvalue=1, offvalue=0)
enable_sounds_button.select()

button_play.place(x=150, y=200, anchor='center')
fps_choice.place(x=80, y=100, anchor='center')
text_fps.place(x=80, y=50, anchor='center')
enable_sounds_button.place(x=200, y=100, anchor='center')

root.mainloop()

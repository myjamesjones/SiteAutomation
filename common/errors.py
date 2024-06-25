
from sys import path
from sys import exit

path.append('..\\common')

def StandardErrorPopup(strHeading, strErrorMsg):
    sg.change_look_and_feel('Dark Blue 3')
    layout = [[sg.Text(strHeading)],
          [sg.Text(strErrorMsg,auto_size_text=any)],
          [sg.Button('Exit')]]


    window = sg.Window(strHeading, layout)
    event, values = window.read(close=True)
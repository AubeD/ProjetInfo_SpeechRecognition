import speech_recognition as sr
from pywinauto.application import Application

# obtain audio from the microphone
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# recognize speech using Sphinx
try:
    parole=r.recognize_sphinx(audio)
    print(parole)
    app = Application(backend="uia").start('notepad.exe')
    # describe the window inside Notepad.exe process
    dlg_spec = app.SansTitreBlocNotes
    # wait till the window is really open
    actionable_dlg = dlg_spec.wait('visible')
    if parole=="browse":
        app.SansTitreBlocNotes.menu_select("File->EnregistrerSous")
    
except sr.UnknownValueError:
    print("Sphinx could not understand audio")
except sr.RequestError as e:
    print("Sphinx error; {0}".format(e))

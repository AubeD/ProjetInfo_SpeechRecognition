import speech_recognition as sr
from pywinauto.application import Application

# obtain audio from the microphone

app = Application(backend="uia").connect(title="mainForm")
commandes = {'connect':app.mainForm.ConnectNao,'rest':app.mainform.MakeNaoRest,'start':app.mainform.StartRealtimeControl}
# recognize speech using Sphinx

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Say something!")
        audio = r.listen(source)

    try:
        parole=r.recognize_sphinx(audio,"EN-Nao")
        print(parole)
        # describe the window inside Notepad.exe process
        dlg_spec = app.mainForm
        # wait till the window is really open
        actionable_dlg = dlg_spec.wait('visible')
        for key in commandes:
            if key in parole:
                commandes[key].click()
        
    except sr.UnknownValueError:
        print("Sphinx could not understand audio")
    except sr.RequestError as e:
        print("Sphinx error; {0}".format(e))
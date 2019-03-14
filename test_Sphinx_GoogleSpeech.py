# -*- coding: utf-8 -*-

# Importation des modules
import speech_recognition as sr
import os

# quiet the endless 'insecurerequest' warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Paramétrage
recognizer = 'sphinx'
sphinx_use_hotwords = False


# Configuration de Sphinx
if recognizer == 'sphinx':
    model_path = 'D:/3A_Centrale/Projet Info/ProjetInfo_SpeechRecognition/EN-NAO/'
    config = {
        'hmm': os.path.join(model_path, 'acoustic-model'),
        'lm': os.path.join(model_path, 'language-model.lm.bin'),
        'dict': os.path.join(model_path, 'pronounciation-dictionary.dict'),
        'grammar':os.path.join(model_path, 'GrammarNAO.jsgf')
    }
    config_sphinx = (config['hmm'], config['lm'], config['dict'])
    
    if sphinx_use_hotwords:
        keyword_entries = [
                            'connect nao',
                            'make nao rest',
                            'start real-time telecontrol',
                            'stop real-time telecontrol',
                            'mirror on',
                            'mirror off',
                            'connect kinect',
                            'close kinect',
                            'save movement',
                            'stop movement'
                           ]
        for i in range(len(keyword_entries)):
            keyword_entries[i] = (keyword_entries[i], 0.9)
    else:    
        grammar = config['grammar']

# Reconnaissance
with sr.Microphone(sample_rate=44100) as source:
    r = sr.Recognizer()
    print("Please wait. Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=1)
    print('Microphone calibred')
    while True:
        audio = r.listen(source,phrase_time_limit=5)
        print('Speech recognized')
        try:
            if recognizer == 'google':
                response = r.recognize_google(audio, show_all=True)
                print(response)
            else:
                if sphinx_use_hotwords:
                    response = r.recognize_sphinx(audio, language=config_sphinx, keyword_entries=keyword_entries, show_all=True)
                    if response.hyp():
                        print(response.hyp().hypstr)
                        print(response.hyp().best_score)
                else:
                    response = r.recognize_sphinx(audio, language=config_sphinx, grammar=grammar, show_all=True)
                    hypothese = response.hyp()
                    if hypothese:
                        print(hypothese.hypstr)
                        print(hypothese.best_score)
                    #print("I think you said " + response + "'")
        except sr.UnknownValueError:
            print("Sphinx could not understand audio")
        except sr.RequestError as e:
             print("Sphinx error; {0}".format(e))
        except:
            if recognizer == 'google':
                print('Request timed out !')
            else:
                print('Unknown error type')
                raise
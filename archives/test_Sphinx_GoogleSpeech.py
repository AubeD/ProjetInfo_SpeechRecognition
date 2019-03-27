# -*- coding: utf-8 -*-

################################################################################################
# La première version de la reconaissance vocale mise en oeuvre. Ce fichier permet d'évaluer   #
# 3 solutions différentes:                                                                     #
#     - Reconnaissance vocale avec Sphinx + une grammaire                                      #
#     - Utilisation de Sphinx en tant que détecteur de mots-clés (hotwords)                    #
#     - Utilisation de l'API gratuite de Google, SpeechRecognition                             #
# Les hotwords fonctionnent extrêmement mal, on les a écartés tout de suite. SpeechRecognition #
# donne les meilleurs résultats, mais la réponse de l'API peut être lente à venir/ne pas venir #
# du tout. On a donc gardé Sphinx+grammaire+système de rejet de faux-positifs à seuil          #
################################################################################################



###########################################################################################
# Importation des modules                                                                 #
###########################################################################################
import speech_recognition as sr
import os

# quiet the endless 'insecurerequest' warning
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

###########################################################################################
# Paramétrage                                                                             #
###########################################################################################
recognizer = 'sphinx'        # 'sphinx' pour utiliser pocketSphinx, 'google' pour SpeechRecognition API
sphinx_use_hotwords = False  # Si (recognizer, sphinx_use_hotwords) = ('sphinx', True) on utilise
                             # Sphinx en mode détection de Hotwords. Sous Linux Snowboy existe et est censé
                             # fonctionner correctement voire très bien. Il est gratuit.

###########################################################################################
# Configuration de Sphinx (manuelle)                                                      #
###########################################################################################
if recognizer == 'sphinx':
    model_path = '../EN-NAO/'
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
                            'stop movement',
                            'start listening',
                            'stop listening',
                            'yes nao',
                            'no nao'
                           ]
        for i in range(len(keyword_entries)):
            keyword_entries[i] = (keyword_entries[i], 0.9)
    else:    
        grammar = config['grammar']

###########################################################################################
# Reconnaissance                                                                          #
###########################################################################################
with sr.Microphone(sample_rate=44100) as source: # Changer le numéro de device et le sample_rate au besoin (utiliser ../scripts_utilitaires/listage_micros pour trouver les bons paramètres)
    r = sr.Recognizer()
    # Adaptation de la reconnaissance au niveau de bruit ambiant
    print("Please wait. Calibrating microphone...")
    r.adjust_for_ambient_noise(source, duration=1)
    print('Microphone calibred')
    # Reconnaissance en continu (arrêter Python avec Ctrl+C pour terminer)
    while True:
        audio = r.listen(source,phrase_time_limit=5)
        print('Speech recognized')
        try:
            # Reconnaissance vocale avec Google SpeechRecognition API
            if recognizer == 'google':
                response = r.recognize_google(audio, show_all=True)
                print(response)
            else:
                # Attente de phrases-clés avec Sphinx (préférer Snowboy sous Linux/OSX)
                if sphinx_use_hotwords:
                    response = r.recognize_sphinx(audio, language=config_sphinx, keyword_entries=keyword_entries, show_all=True)
                    if response.hyp():
                        print(response.hyp().hypstr)
                        print(response.hyp().best_score)
                # Reconnaissance vocale avec Sphinx, un dictionnaire custom et une grammaire custom
                # NE PAS UTILISER LE DICTIONNAIRE COMPLET / NE PAS SE PASSER DE GRAMMAIRE, le résultat sera n'importe quoi
                else:
                    response = r.recognize_sphinx(audio, language=config_sphinx, grammar=grammar, show_all=True)
                    hypothese = response.hyp()
                    if hypothese:
                        print('+{}+'.format(hypothese.hypstr))
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
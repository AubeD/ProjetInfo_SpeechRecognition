# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 10:22:26 2019

@author: natan
"""

#########################################################################################
# Importation des modules                                                               #
#########################################################################################
import speech_recognition as sr
import config

#########################################################################################
# Fonctions auxiliaires                                                                 #
#########################################################################################
def instruction_plus_proche(instruction):
    """
    Post-traitement: reconnaît une instruction connue à partir d'une instruction
    reconnue par Sphinx
    """
    for instr in config.instructions:
        if (instruction == instr) or (instr in instruction):
            return instruction
        elif instr == 'make nao rest' and instruction == 'make nao':
            return instr
    return 'RIEN'

def print_fichier(chemin, texte, clean=False):
    """
    Écrit le texte "texte" dans le fichier de chemin "chemin", sans retour à la ligne.
    Si clean=True, on vide au préalable le fichier (ou on le crée s'il n'existe pas)
    """
    if clean:
        with open(chemin, 'w') as fo:
            fo.write(texte)
    else:
        with open(chemin, 'a+') as fo:
            fo.write(texte)

def init_log():
    """ Crée/vide le fichier de log Python au chemin précisé dans config.py """
    print_fichier(config.chemin_pylog, '', True)

def write_log(texte):
    """ Écrit texte dans le fichier de log Python puis retourne à la ligne"""
    print_fichier(config.chemin_pylog, texte+'\n', False)
    
def read_stopfile():
    """
    Lit le buffer de communication C++ -> Python. Si ce dernier contient "stop",
    on arrêtera la reconnaissance vocale.
    """
    with open(config.chemin_stopfile, 'r') as foo:
        return foo.readline() == 'stop'

def init_buffer(buffer):
    """
    Crée/vide le fichier de communication Python -> C++ au chemin précisé dans
    config.py
    """
    if buffer == 'entendu par nao':
        print_fichier(config.chemin_buffer_entendu, '', True)
    elif buffer=='compris par nao':
        print_fichier(config.chemin_buffer_compris, '', True)
        
def write_buffer(buffer, texte):
    """
    Écrit texte dans le fichier de communication Python -> C++ puis retourne
    à la ligne
    """
    if buffer == 'entendu par nao':
        print_fichier(config.chemin_buffer_entendu, texte+'\n', False)
    elif buffer=='compris par nao':
        print_fichier(config.chemin_buffer_compris, texte+'\n', False)
        
    
#########################################################################################
# Script lancé en parallèle du code C++                                                 #
#########################################################################################

# Chargement de la configuration de PocketSphinx depuis config.py
config_sphinx = (config.config_sphinx['hmm'], config.config_sphinx['lm'], config.config_sphinx['dict'])
grammaire = config.config_sphinx['grammar']

# Vidage des fichiers de communiction Python -> utilisateur et Python -> C++
# (bonne pratique: le fichier de communication C++ -> Python doit être vidé par C++)
init_log()
init_buffer('entendu par nao')
init_buffer('compris par nao')

# Initialisation de l'écoute et de l'objet de reconnaissance vocale
with sr.Microphone(sample_rate=44100) as source: # Changer le numéro de device et le sample_rate au besoin (utiliser scripts_utilitaires/listage_micros pour trouver les bons paramètres)
    r = sr.Recognizer()
    r = sr.Recognizer()
    # Début de la reconnaissance vocale
    while not(read_stopfile()):
        # Segmentation et enregistrement d'une phrase
        audio = r.listen(source,phrase_time_limit=5)
        try:
            # On soumet la phrase à Sphinx et on récupère son objet-hypothèse
            response = r.recognize_sphinx(audio, language=config_sphinx, grammar=grammaire, show_all=True)
            hypothese = response.hyp()
            if hypothese:
                # Si du texte intelligible a été reconnu, et que c'est une instruction connue
                instruction = instruction_plus_proche(hypothese.hypstr)
                write_buffer('entendu par nao', hypothese.hypstr)
                write_log('Speech recognized: {}'.format(instruction))
                if instruction != 'RIEN':
                    # On récupère le couple (instruction, score). Si score > seuil(instruction) on la transmet
                    # au programme C++ via le buffer Python->C++
                    score = hypothese.best_score
                    if score > config.instructions[instruction]:
                        write_buffer('compris par nao', instruction)
                    else:
                        write_log('{}: Rejet comme Faux Positif'.format(instruction))
            else:
                write_buffer('entendu par nao', '')
        # Si Sphinx renvoie une erreur, on continue la reconnaissance en modifiant le fichier de logs
        except sr.UnknownValueError:
            write_log("Sphinx could not understand audio")
        except sr.RequestError as e:
             write_log("Sphinx error; {0}".format(e))
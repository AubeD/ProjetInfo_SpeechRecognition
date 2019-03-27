# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 10:16:42 2019

@author: natan
"""

###########################################################################################
# Fichier de configuration des chemins Python et des instructions à reconnaître. À        #
# modifier si:                                                                            #
# - des fichiers sont déplacés (chemins relatifs depuis le répertoire courant)            #
# - la liste des instructions à reconnaître change (la grammaire sera également à refaire #
#   et à recompiler dans ce cas; le dictionnaire de phonèmes devra être modifié)          #
###########################################################################################


###########################################################################################
# Chemins d'accès                                                                         #
###########################################################################################

# Module os, ici pour la gestion des chemins de fichiers
import os

# Dossier contenant l'instance de reconnaissance vocale de Sphinx
model_path = 'EN-NAO/'
# Buffers de communication Python -> C++
chemin_buffer_entendu = 'communication/buffer_entendu.txt'
chemin_buffer_compris = 'communication/buffer_compris.txt'
# Buffer de communication C++ -> Python
chemin_buffer_C = 'communication/buffer_C.txt'
# Logs écrits par le fichier programme_python_nao.py
chemin_pylog = 'logs/log_Python.log'

# Éléments constituant l'instance de reconnaissance vocale par Sphinx
config_sphinx = {
    'hmm': os.path.join(model_path, 'acoustic-model'),                 # Hidden Markov Model / Phonèmes + enchaînement
    'lm': os.path.join(model_path, 'language-model.lm.bin'),           # Modèle de langage / enchaînement + contexte des mots
    'dict': os.path.join(model_path, 'pronounciation-dictionary.dict'),# Dictionnaire phonétiques pour les mots reconnus
    'grammar':os.path.join(model_path, 'GrammarNAO.jsgf')              # Fichier de grammaire utilisée
}

########################################################################################################################
# Instructions à reconnaître et seuils de confiance nécessaires à leur conservation                                    #
# (ces seuils sont déterminés par "clustering visuel" à l'aide de sphinx_reglage_seuils_anti_surdetection.py)          #
# Pour chaque instruction: seuils=  [s1, s2] => score <= s1: rejet, score >=s2: acceptation, s1<score<s2: acceptation  #
# Si s1=s2=s: pas de domaine de doute, score <= s: rejet et score > s: acceptation                                     #
########################################################################################################################
instructions =  {
        'connect nao':                  [-6800, -6800],
        'make nao rest':                [-8000, -8000],
        'start real-time telecontrol':  [-10000, -10000],
        'stop real-time telecontrol':   [-9500, -7000],
        'mirror on':                    [-8000, -8000],
        'mirror off':                   [-8000, -8000],
        'connect kinect':               [-6000, -6000],
        'close kinect':                 [-5000, -4500],
        'save movement':                [-8000, -4000],
        'stop movement':                [-7000, -5500],
        'start listening':              [-100000, -100000],
        'stop listening':               [-100000, -100000],
        'yes nao':                      [-100000, -100000],
        'no nao':                       [-100000, -100000],
        'RIEN':                         [0, 0]  # 'RIEN' désigne une absence d'instruction reconnue.
        }

###########################################################################################
# Graphe d'états de la reconnaissance vocale.                                             #
###########################################################################################

# Noeuds/états du graphe
etats_possible_reconnaissance = ['stop', 'pause', 'doute', 'attente_instruction']

# Instructions comprises par NAO lorsqu'on se trouve dans chaque noeud du graphe
instructions_comprises = {
        'arret': [],
        'pause':['start listening'],
        'doute':['yes nao', 'no nao'],
        'attente_instruction': [instr for instr in instructions if not(instr in ['start listening', 'yes nao', 'no nao', 'RIEN'])]
        }

# Pour chaque état, liste des instructions causant le passage à un autre état
transitions_vocales = {
        'arret': {},
        'pause': {'start listening': 'attente_instruction'},
        'doute': {'yes nao': 'attente_instruction', 'no nao': 'attente_instruction'},
        'attente_instruction': {'stop listening': 'pause'}
        }

# Pour chaque message envoyé par le code C++, transition d'un état à un autre induite
transitions_provoquees = {
        'stop':'arret',
        'pause':'pause',
        'reprise':'attente_instruction'
        }

#############################################################################################################
# Microphone à utiliser et son paramétrage (utiliser scripts_utilitaires/listage_micros.py pour le trouver) #
#############################################################################################################
id_micro = None # None pour utiliser le périphérique par défaut
sample_rate = 44100

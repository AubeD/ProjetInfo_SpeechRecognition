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


# Module os, ici pour la gestion des chemins de fichiers
import os

# Dossier contenant l'instance de reconnaissance vocale de Sphinx
model_path = 'EN-NAO/'
# Buffers de communication Python -> C++
chemin_buffer_entendu = 'communication/buffer_entendu.txt'
chemin_buffer_compris = 'communication/buffer_compris.txt'
# Buffer de communication C++ -> Python
chemin_stopfile = 'communication/stop_Python.txt'
# Logs écrits par le fichier programme_python_nao.py
chemin_pylog = 'logs/log_Python.log'

# Éléments constituant l'instance de reconnaissance vocale par Sphinx
config_sphinx = {
    'hmm': os.path.join(model_path, 'acoustic-model'),                 # Hidden Markov Model / Phonèmes + enchaînement
    'lm': os.path.join(model_path, 'language-model.lm.bin'),           # Modèle de langage / enchaînement + contexte des mots
    'dict': os.path.join(model_path, 'pronounciation-dictionary.dict'),# Dictionnaire phonétiques pour les mots reconnus
    'grammar':os.path.join(model_path, 'GrammarNAO.jsgf')              # Fichier de grammaire utilisée
}

# Instructions à reconnaître et seuils de confiance nécessaires à leur conservation
# (ces seuils sont déterminés par "clustering visuel" à l'aide de sphinx_reglage_seuils_anti_surdetection.py)
instructions =  {
                'connect nao':-6800,
                'make nao rest':-9000,
                'start real-time telecontrol':-11000,
                'stop real-time telecontrol':-7500,
                'mirror on':-4500,
                'mirror off':-7500,
                'connect kinect':-6500,
                'close kinect':-4500,
                'save movement':-6000,
                'stop movement':-5500,
                'RIEN':0 # 'RIEN' désigne une absence d'instruction reconnue.
                }

# Microphone à utiliser et son paramétrage (utiliser scripts_utilitaires/listage_micros.py pour le trouver)
id_micro = None # None pour utiliser le périphérique par défaut
sample_rate = 44100

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 11:31:00 2019

@author: natan
"""

# Importation des modules
import speech_recognition as sr
import matplotlib.pyplot as plt
import winsound
import os
import numpy as np


def instruction_plus_proche(instruction):
    instructions = [ # Instructions possibles pour le projet
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
                'RIEN'
               ]
    for instr in instructions:
        if (instruction == instr) or (instr in instruction):
            return instruction
        elif instr == 'make nao rest' and instruction == 'make nao':
            return instr
    return 'RIEN'

def enregistrer_phrase(duree=5):
    """Enregistre et labellise une séquence audio"""
    instructions = {
                    '0': 'connect nao',
                    '1': 'make nao rest',
                    '2': 'start real-time telecontrol',
                    '3': 'stop real-time telecontrol',
                    '4': 'mirror on',
                    '5': 'mirror off',
                    '6': 'connect kinect',
                    '7': 'close kinect',
                    '8': 'save movement',
                    '9': 'stop movement',
                    '10': 'RIEN'
                   }
    print(instructions)
    choix = input("Entrer le numéro de l'instruction: ")
    instruction = instructions[choix]
    print('Instruction choisie: {}'.format(instruction))
    with sr.Microphone(sample_rate=44100) as source:
        r = sr.Recognizer()
        print('Parlez')
        audio = r.listen(source,phrase_time_limit=duree)
        print('Enregistrement terminé')
        fichier_wav = audio.get_wav_data()
        
    chemin = 'records/'+instruction
    if not(os.path.exists(chemin)):
        os.makedirs(chemin)
    nb_fichiers = len(os.listdir(chemin))
    chemin_nouveau_fichier = '{}/{}_{}.wav'.format(chemin, instruction, nb_fichiers+1)
    
    with open(chemin_nouveau_fichier, 'wb') as fo:
        fo.write(fichier_wav)
        
    winsound.PlaySound(chemin_nouveau_fichier, winsound.SND_FILENAME)
    condition=False
    while not(condition):
        garder_fichier = input('Garder le fichier ? (y/n): ')
        if garder_fichier == 'n':
            os.remove(chemin_nouveau_fichier)
            print('fichier effacé !')
            condition = True
        elif garder_fichier == 'y':
            print('fichier conservé !')
            condition = True
        
def analyser_son(chemin, config_sphinx, grammar):
    """
    Pour une séquence audio, la soumet à Sphinx et retourne l'hypothèse et le
    score obtenus, en plus de l'instruction attendue
    """
    instruction = os.path.split(chemin)[1].split('_')[0]
    with sr.AudioFile(chemin) as source:
        r = sr.Recognizer()
        audio = r.record(source)
        reponse = r.recognize_sphinx(audio, language=config_sphinx, grammar=grammar, show_all=True)
    hypothese = reponse.hyp()
    if hypothese:
        instruction_sphinx = hypothese.hypstr
        score_sphinx = hypothese.best_score
    else:
        instruction_sphinx = 'RIEN'
        score_sphinx = None
    
    instruction_reconnue = instruction_plus_proche(instruction_sphinx)
    return instruction, instruction_reconnue, score_sphinx

def analyser_banque_sonore(model_path):
    """
    Applique systématiquement analyser_son à tous les enregistrements de la bdd,
    et retourne la liste de (instruction attendue, instruction reconnue, score)
    """
    # Configuration de Sphinx
    config = {
        'hmm': os.path.join(model_path, 'acoustic-model'),
        'lm': os.path.join(model_path, 'language-model.lm.bin'),
        'dict': os.path.join(model_path, 'pronounciation-dictionary.dict'),
        'grammar':os.path.join(model_path, 'GrammarNAO.jsgf')
    }
    config_sphinx = (config['hmm'], config['lm'], config['dict'])
    grammar = config['grammar']
    
    resultats_analyses_sons = []
    for instruction in os.listdir('records'):
        for son in os.listdir('records/{}'.format(instruction)):
            chemin = 'records/{}/{}'.format(instruction, son)
            resultats_analyses_sons.append(analyser_son(chemin, config_sphinx, grammar))
    return resultats_analyses_sons
            
def visualiser_TP_FP():
    """
    Pour une base de données de fichiers .wav annotés par nomenclature:
    - Détermine pour chaque fichier l'instruction attendue (annotation),
    l'instruction reconnue par Sphinx et le score de la reconnaissance
    - Pour chaque instruction possible, trace le score renvoyé par Sphinx pour
    les Vrais Positifs (TP, instruction reconnue à raison) et les Faux Positifs
    (FP, instruction reconnue à tort)
    - Renvoie les données ayant servi aux graphes pour d'éventuelles analyses
    statistiques
    """
    model_path = 'EN-NAO'
    resultats_analyse = analyser_banque_sonore(model_path)
    instructions = [
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
                'RIEN'
               ]
    TP_FP = {i:{'TP':[], 'FP':[]} for i in instructions if i!= 'RIEN'}
    for instr, instr_sphinx, score in resultats_analyse:
        if instr == instr_sphinx:
            if instr != 'RIEN':
                TP_FP[instr]['TP'].append(score)
        else:
            TP_FP[instr_sphinx]['FP'].append(score)
    
    for instr in TP_FP:
        data_TP = TP_FP[instr]['TP']
        data_FP = TP_FP[instr]['FP']
        plt.figure(instr)
        plt.title('Répartition TP/FP en fonction du score - {}'.format(instr))
        plt.xlabel('Score')
        plt.scatter(data_TP, np.random.rand(len(data_TP)), c='blue', label='TP')
        plt.scatter(data_FP, np.random.rand(len(data_FP)), c='red', label='FP')
        plt.ylim([-5, 5])
        plt.legend()
    
    return TP_FP

def enregistrer_FP_en_continu(nb_extraits, duree_enregistrement=5):
    with sr.Microphone(sample_rate=44100) as source:
        r = sr.Recognizer()
        for i in range(nb_extraits):
            print('Enregistrement {}/{} commencé'.format(i+1, nb_extraits))
            audio = r.listen(source,phrase_time_limit=duree_enregistrement)
            print('Enregistrement {}/{} terminé'.format(i+1, nb_extraits))
            fichier_wav = audio.get_wav_data()     
            chemin = 'records/RIEN'
            if not(os.path.exists(chemin)):
                os.makedirs(chemin)
            nb_fichiers = len(os.listdir(chemin))
            chemin_nouveau_fichier = '{}/{}_{}.wav'.format(chemin, 'RIEN_cours_enregistre', nb_fichiers+1)
            with open(chemin_nouveau_fichier, 'wb') as fo:
                fo.write(fichier_wav)
                
def supprimer_enregistrements_RIEN_sans_FP():
    # Configuration de Sphinx
    model_path = 'EN-NAO'
    config = {
        'hmm': os.path.join(model_path, 'acoustic-model'),
        'lm': os.path.join(model_path, 'language-model.lm.bin'),
        'dict': os.path.join(model_path, 'pronounciation-dictionary.dict'),
        'grammar':os.path.join(model_path, 'GrammarNAO.jsgf')
    }
    config_sphinx = (config['hmm'], config['lm'], config['dict'])
    grammar = config['grammar']
    chemin = 'records/RIEN/'
    fichiers_conserves = []
    fichiers_supprimes = []
    print('Début du nettoyage des fichiers inutiles...')
    for fichier in os.listdir(chemin):
        if analyser_son(chemin+fichier, config_sphinx, grammar)[1] == 'RIEN':
            fichiers_supprimes.append(chemin+fichier)
            print('Fichier {} supprimé !'.format(chemin+fichier))
        else:
            print('Fichier {} conservé !'.format(chemin+fichier))
            fichiers_conserves.append(chemin+fichier)
    for chemin_fichier in fichiers_supprimes:
        os.remove(chemin_fichier)
    for i in range(len(fichiers_conserves)):
        os.rename(fichiers_conserves[i], '{}RIEN_FP_confirme_attente_{}'.format(chemin, i+1))
    for i in range(len(fichiers_conserves)):
        chemin_fichier = '{}RIEN_FP_confirme_attente_{}'.format(chemin, i+1)
        chemin_slice = chemin_fichier.split('attente_')
        os.rename(chemin_fichier, chemin_slice[0] + chemin_slice[1])
    print('Nettoyage terminé !')
            
        
#while True:
#    enregistrer_phrase()

#enregistrer_FP_en_continu(50, 5)
#supprimer_enregistrements_RIEN_sans_FP()

#visualiser_TP_FP()

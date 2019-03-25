# -*- coding: utf-8 -*-
"""
Created on Thu Mar 14 11:31:00 2019

@author: natan
"""

#########################################################################################
# Importation des modules                                                               #
#########################################################################################
import speech_recognition as sr
import matplotlib.pyplot as plt
import winsound
import os
import numpy as np
import config

#########################################################################################
# Fonctions utilisées pour l'enregistrement/l'analyse/le nettoyage de la bdd sonore     #
#########################################################################################
def instruction_plus_proche(instruction):
    """
    Post-traitement: reconnaît une instruction connue à partir d'une instruction
    reconnue par Sphinx
    """
    instructions = config.instructions
    for instr in instructions:
        if (instruction == instr) or (instr in instruction):
            return instruction
        elif instr == 'make nao rest' and instruction == 'make nao':
            return instr
    return 'RIEN'

def enregistrer_phrase(duree=5):
    """Enregistre et labellise une séquence audio"""
    # Chargement de la liste des instructions possibles depuis config.py
    liste_instructions = list(config.instructions.keys())
    instructions = {str(i):liste_instructions[i] for i in range(len(liste_instructions))}
    # On demande à l'utilisateur le label de la phrase à prononcer, parmi les instructions possibles
    print(instructions)
    choix = input("Entrer le numéro de l'instruction: ")
    instruction = instructions[choix]
    print('Instruction choisie: {}'.format(instruction))
    # On enregistre la phrase sous la forme d'un fichier audio (objet wav sous Python)
    with sr.Microphone(device_index=config.id_micro, sample_rate=config.sample_rate) as source:
        r = sr.Recognizer()
        print('Parlez')
        audio = r.listen(source,phrase_time_limit=duree)
        print('Enregistrement terminé')
        fichier_wav = audio.get_wav_data()
    
    # On écrit cet objet wav dans un fichier .wav au sein du dossier records
    # (système de sous-dossiers classant les fichiers en fonction de l'instruction/label)
    chemin = 'records/'+instruction
    if not(os.path.exists(chemin)):
        os.makedirs(chemin)
    nb_fichiers = len(os.listdir(chemin))
    chemin_nouveau_fichier = '{}/{}_{}.wav'.format(chemin, instruction, nb_fichiers+1)
    
    with open(chemin_nouveau_fichier, 'wb') as fo:
        fo.write(fichier_wav)
    
    # On rejoue le son et on demande à l'utilisateur de valider l'enregistrement
    # (en boucle jusqu'à que la réponse soit clairement oui ou non).
    # Si c'est non on eface l'enregistrement.
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
    # On extrait l'instruction/label du fichier grâce au système de nomenclature
    instruction = os.path.split(chemin)[1].split('_')[0]
    # On soumet le fichier audio à Sphinx, et on note l'hypothèse et le score de
    # confiance obtenus
    with sr.AudioFile(chemin) as source:
        r = sr.Recognizer()
        audio = r.record(source)
        reponse = r.recognize_sphinx(audio, language=config_sphinx, grammar=grammar, show_all=True)
    hypothese = reponse.hyp()
    if hypothese:
        instruction_sphinx = hypothese.hypstr
        score_sphinx = hypothese.best_score
    else:
        # S'il n'y a pas d'hypothèse (son non reconnu) l'instruction reconnue par
        # Sphinx est prise comme 'RIEN'
        instruction_sphinx = 'RIEN'
        score_sphinx = None
    
    # On identifie l'instruction à une instruction connue ou à RIEN
    instruction_reconnue = instruction_plus_proche(instruction_sphinx)
    # On renvoie le triplet (label_manuel, label_sphinx, confiance_sphinx)
    return instruction, instruction_reconnue, score_sphinx

def analyser_banque_sonore(model_path):
    """
    Applique systématiquement analyser_son à tous les enregistrements de la bdd,
    et retourne la liste de (instruction attendue, instruction reconnue, score)
    pour chaque enregistrement (l'ordre de la liste n'importe pas)
    """
    # Configuration de Sphinx
    conf = config.config_sphinx
    config_sphinx = (conf['hmm'], conf['lm'], conf['dict'])
    grammar = conf['grammar']
    
    # Analyse de tous les fichiers du dossier 'records'
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
    (FP, instruction reconnue à tort). Utiliser ces courbes pour déterminer visuellement
    les seuils de confiance en-dessous desquels une instruction reconnue doit être ignorée.
    - Renvoie les données ayant servi aux graphes pour d'éventuelles analyses
    statistiques
    """
    # On analyse le dossier records pour obtenir la liste de (label_manuel, label_sphinx, confiance_sphinx)
    # pour chaque fichier audio
    resultats_analyse = analyser_banque_sonore(config.model_path)
    # On charge l'ensemble des instructions possibles depuis config.py
    instructions = list(config.instructions.keys())
    # Pour chaque instruction possible, on crée une liste TP contenant les scores
    # de confiance des enregistrements pour lesquels label_manuel = label_sphinx = instruction
    # et une liste FP pour laquelle label_sphinx = instruction != label_manuel
    TP_FP = {i:{'TP':[], 'FP':[]} for i in instructions}
    for instr, instr_sphinx, score in resultats_analyse:
        if instr == instr_sphinx:
            if instr != 'RIEN':
                TP_FP[instr]['TP'].append(score)
        else:
            TP_FP[instr_sphinx]['FP'].append(score)
    
    # Pour chaque instruction possible, on trace la position des TP (en bleu) et
    # des FP (en rouge) sur la droite des scores de confiances (on fait du jittering
    # selon l'axe y pour pouvoir distinguer des points proches)
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
    
    # On retourne le dictionnaire (scores_TP, scores_FP = f(instruction))
    return TP_FP

def enregistrer_FP_en_continu(nb_extraits, duree_enregistrement=5):
    """
    Enregistre nb_fois d'affilée des extraits sonores avec le label "RIEN" (voir
    nomenclature de enregistrer_phrases). À utiliser en tâche de fond, dans un
    contexte n'ayant rien à voir avec NAO afin de se constituer une base 
    de données de faux positifs pour la détermination des seuils de rejet.
    """
    with sr.Microphone(device_index=config.id_micro, sample_rate=config.sample_rate) as source:
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
    """
    Explore l'ensemble des fichiers audio labellisés "RIEN", et les soumet à
    Sphinx. Supprime les enregistrements qui n'ont pas été reconnus à tort comme
    des instructions valides (inutiles à la recherche de seuils de rejet de faux
    positifs). Renomme les fichiers restants ('consolidés') afin qu'ils soient bien
    identifiés
    """
    # Configuration de Sphinx
    conf = config.config_sphinx
    config_sphinx = (conf['hmm'], conf['lm'], conf['dict'])
    grammar = conf['grammar']
    chemin = 'records/RIEN/'
    # Identification des fichiers à supprimer (en les soumettant à Sphinx)
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
    # Suppression des fichiers inutiles (non-FP)
    for chemin_fichier in fichiers_supprimes:
        os.remove(chemin_fichier)
    # Renommage des fichiers en 2 étapes afin d'éviter des conflits avec la nomenclature
    # des fichiers déjà consolidés
    for i in range(len(fichiers_conserves)):
        os.rename(fichiers_conserves[i], '{}RIEN_FP_confirme_attente_{}'.format(chemin, i+1))
    for i in range(len(fichiers_conserves)):
        chemin_fichier = '{}RIEN_FP_confirme_attente_{}'.format(chemin, i+1)
        chemin_slice = chemin_fichier.split('attente_')
        os.rename(chemin_fichier, chemin_slice[0] + chemin_slice[1])
    print('Nettoyage terminé !')
            
#########################################################################################
# Programme principal                                                                   #
#########################################################################################

if __name__ == '__main__':
#    # Décommenter ce bloc pour enregistrer manuellement des instructions en continu
#    while True:
#        enregistrer_phrase()
    
#    # Décommenter ce bloc pour enregistrer des faux positifs en continu
#    enregistrer_FP_en_continu(150, 5)
#    supprimer_enregistrements_RIEN_sans_FP()
    
    # Décommenter ce bloc pour visualiser les TP et FP parmi les enregistrements existants
    visualiser_TP_FP()

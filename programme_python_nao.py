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
    
def read_buffer_C():
    """
    Lit le buffer de communication C++ -> Python. Si ce dernier contient "stop",
    on arrêtera la reconnaissance vocale.
    """
    with open(config.chemin_buffer_C, 'r') as foo:
        return foo.readline()

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
        
 
    
def reconnaissance_vocale(mode_reconnaissance, r, source, config_sphinx, grammaire):
    """
    Effectue la reconnaissance vocale de la prochaine phrase à venir. Prend en paramètres:
        - le mode de reconnaissance actuel
        - l'objet sr.Recorder r permettant de segmenter et d'analyser un extrait audio avec Sphinx
        - une source audio source (fichier .wav ou stream en sortie du micro de l'appareil)
        - config_sphinx et grammaire, la configuration de la reconnaissance Sphinx
    Filtre les instructions reconnues en fonction du mode de reconnaissance actuel.
    Communique le cas échéant l'instruction qui a été reconnue au code C++, via les différents buffers.    
    Retourne le mode de reconnaissance à la fin de la reconnaissance vocale (il diffère du mode de 
    départ si l'instruction reconnue implique un changement de mode).
    """    
    
    # Si C++ s'est arrêté, on ne cherche pas à reconnaître quoi que ce soit et on laisse Python
    # s'arrêter.
    if mode_reconnaissance == 'arret':
        return 'arret'
    
    # Segmentation et enregistrement d'une phrase
    audio = r.listen(source,phrase_time_limit=5)
    try:
        # On soumet la phrase à Sphinx et on récupère son objet-hypothèse
        response = r.recognize_sphinx(audio, language=config_sphinx, grammar=grammaire, show_all=True)
        hypothese = response.hyp()
        if hypothese:
            # Si du texte intelligible a été reconnu, et que c'est une instruction attendue
            # dans le mode d'écoute actuel...
            instruction = instruction_plus_proche(hypothese.hypstr)
            write_buffer('entendu par nao', hypothese.hypstr)
            if instruction in config.instructions_comprises[mode_reconnaissance]:
                # On extrait le score de confiance associé à l'instruction
                score = hypothese.best_score
                # En fonction de ce dernier, on accepte ou non l'instruction, ou on
                # se place en état de doute
                score_rejet, score_acceptance = config.instructions[instruction]
                write_log('{} vs [{}  {}]'.format(score, score_rejet, score_acceptance))
                
                if score <= score_rejet: # rejet comme FP
                    write_log('{}: {} vs [{}  {}] =>Rejet comme Faux Positif'.format(instruction, score, score_rejet, score_acceptance))
                    return mode_reconnaissance
                
                elif score >= score_acceptance: # acceptation comme TP
                    write_buffer('compris par nao', '{}:{}'.format(instruction, 'OK'))
                    write_log('{}: {} vs [{}  {}] =>Instruction transmise'.format(instruction, score, score_rejet, score_acceptance))
                    # Si l'instruction reconnue correpond à une transition d'un état de la
                    # reconnaissance vocale à un autre, on effectue cette transition
                    if instruction in config.transitions_vocales[mode_reconnaissance]:
                        return config.transitions_vocales[mode_reconnaissance][instruction]
                    else:
                        return mode_reconnaissance
                    
                else: # On se place en état de doute et on va demander à l'utilisateur son avis
                    write_buffer('compris par nao', '{}:{}'.format(instruction, 'doute'))
                    write_log('{}: {} vs [{}  {}] =>Doute de NAO'.format(instruction, score, score_rejet, score_acceptance))
                    return 'doute'
            else:
                write_log('{}: instruction inconnue dans le mode {}'.format(instruction, mode_reconnaissance))
                return mode_reconnaissance
                    
        else: # Si aucun texte n'a été reconnu on ne fait rien
            write_buffer('entendu par nao', '')
            return mode_reconnaissance
        
    # Si Sphinx renvoie une erreur, on continue la reconnaissance en modifiant le fichier de logs
    # et on continue en conservant l'état actuel
    except sr.UnknownValueError:
        write_log("Sphinx could not understand audio")
        return mode_reconnaissance        
    except sr.RequestError as e:
         write_log("Sphinx error; {0}".format(e))
         return mode_reconnaissance
         
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

# Initialisation du mode de reconnaissance: on commence par écouter les instructions possibles
mode_reconnaissance = 'attente_instruction' # modes possibles: 'attente_instruction', 'doute', 'pause', 'arret'

# Initialisation de l'écoute et de l'objet de reconnaissance vocale
with sr.Microphone(device_index=config.id_micro, sample_rate=config.sample_rate) as source:
    r = sr.Recognizer()
    r = sr.Recognizer()
    # Début de la reconnaissance vocale
    while not(mode_reconnaissance == 'arret'):
        # Si le code C envoie une instruction, on outrepasse le fonctionnement normal de la reconnaissance
        # vocale et on se place à l'état indiqué (par exemple 'arret' pour mettre fin à la reconnaissance)
        message_code_C = read_buffer_C()
        if message_code_C:
            mode_reconnaissance = config.transitions_provoquees[message_code_C]
        # On reconnaît une phrase. Si elle correspond à une instruction possible dans le contexte du mode de
        # reconnaissance actuel, on la transmet à C++ et on met à jour le mode de reconnaissance au besoin.
        mode_reconnaissance = reconnaissance_vocale(mode_reconnaissance, r, source, config_sphinx, grammaire)
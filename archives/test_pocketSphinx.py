# -*- coding: utf-8 -*-

##############################################################################################
# Ce fichier (pompé sur Internet !) illustre les possibilités de Sphinx dans le cas où on ne #
# passerait pas par la surcouche SpeechRecognition:                                          #
#     - Score de détection de chaque phonème du mot                                          #
#     - Ensemble des hypothèses émises par Sphinx                                            #
#     - Score de chaque hypothèse                                                            #
# Dans les faits, on a plus été confrontés au problème de la surdétection qu'au problème de  #
# la sous-détection, et on n'a pas eu à se servir de tout cela                               #
##############################################################################################

from __future__ import print_function
import os
from pocketsphinx import Pocketsphinx, get_data_path

# Accès aux fichiers d'exemples fournis/ayant servi à entraîner Sphinx
data_path = get_data_path()

# Entrer le chemin vers le modèle de reconnaissance vocale Sphinx à utiliser
model_path = 'D:/3A_Centrale/Projet Info/ProjetInfo_SpeechRecognition/EN-NAO/'
config = {
    'hmm': os.path.join(model_path, 'acoustic-model'),
    'lm': os.path.join(model_path, 'language-model.lm.bin'),
    'dict': os.path.join(model_path, 'pronounciation-dictionary.dict')
}

ps = Pocketsphinx(**config)
ps.decode(
    audio_file=os.path.join(data_path, 'goforward.raw'),
    buffer_size=2048,
    no_search=False,
    full_utt=False
)

print(ps.segments()) # => ['<s>', '<sil>', 'go', 'forward', 'ten', 'meters', '</s>']
print('Detailed segments:', *ps.segments(detailed=True), sep='\n') # => [
#     word, prob, start_frame, end_frame
#     ('<s>', 0, 0, 24)
#     ('<sil>', -3778, 25, 45)
#     ('go', -27, 46, 63)
#     ('forward', -38, 64, 116)
#     ('ten', -14105, 117, 152)
#     ('meters', -2152, 153, 211)
#     ('</s>', 0, 212, 260)
# ]

print(ps.hypothesis())  # => go forward ten meters
print(ps.probability()) # => -32079
print(ps.score())       # => -7066
print(ps.confidence())  # => 0.04042641466841839

print(*ps.best(count=10), sep='\n') # => [
#     ('go forward ten meters', -28034)
#     ('go for word ten meters', -28570)
#     ('go forward and majors', -28670)
#     ('go forward and meters', -28681)
#     ('go forward and readers', -28685)
#     ('go forward ten readers', -28688)
#     ('go forward ten leaders', -28695)
#     ('go forward can meters', -28695)
#     ('go forward and leaders', -28706)
#     ('go for work ten meters', -28722)
# ]
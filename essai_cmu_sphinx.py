# -*- coding: utf-8 -*-
"""
Created on Thu Jan 24 10:34:12 2019

@author: natan
"""

from __future__ import print_function
import os
from pocketsphinx import Pocketsphinx, get_model_path, get_data_path

current_path = 'C:\\Users\\natan\\Desktop\\3A_Centrale\\Projet Info'
model_path = get_model_path()
data_path = get_data_path()

config = {
'hmm': current_path + '\\langage\\fr',
'lm': current_path + 'langage\\fr-small.lm.bin',
'dict': current_path + 'langage\\fr.dict'
}

ps = Pocketsphinx(**config)
ps.decode(
audio_file=os.path.join(os.getcwd(), 'essai.wav'), # add your audio file here
buffer_size=2048,
no_search=False,
full_utt=False
)

print(ps.hypothesis())
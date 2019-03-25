# -*- coding: utf-8 -*-


#########################################################################################
# Fichier (pompé sur Internet !) permettant de compiler un fichier de grammaire .jsgf   #
# en un fichier .fsg utilisable par Sphinx. À noter que:                                #
# - Les chemins sont à renseigner (on n'utilise pas config.py ici, ce script étant      #
#   fortement susceptible d'être déplacé                                                #
# - Si la grammaire s'appelle 'nom_grammaire.jsgf', la règle qui sera lue sera celle qui#
#   se nomme nom_grammaire, et seulement elle. Attention lors de la construction de la  #
#   grammaire, donc (-> faire une arborescence dont la base est nom_grammaire)          #
#########################################################################################

# Dependencies
import os
import pocketsphinx as ps

# Fichier à convertir et paramètres de la reconnaissance vocale
model_path = './'
log_path = 'log_jsgf_to_fsg.log'
config = {
    'hmm': os.path.join(model_path, 'acoustic-model'),
    'lm': os.path.join(model_path, 'language-model.lm.bin'),
    'dict': os.path.join(model_path, 'pronounciation-dictionary.dict'),
    'grammar':os.path.join(model_path, 'GrammarNAO.jsgf')
}
grammar = config['grammar']

try:
    # Point to the model files
    acoustic_parameters_directory = config['hmm']
    language_model_file = config['lm']
    phoneme_dictionary_file = config['dict']

    # Create a decoder object with our custom parameters
    config = ps.Decoder.default_config()
    config.set_string("-hmm", acoustic_parameters_directory)  # set the path of the hidden Markov model (HMM) parameter files
    config.set_string("-lm", language_model_file)
    config.set_string("-dict", phoneme_dictionary_file)
    config.set_string("-logfn", log_path) # Voir le log en cas d'erreur
    decoder = ps.Decoder(config)

    # Convert grammar
    grammar_path = os.path.abspath(os.path.dirname(grammar))
    grammar_name = os.path.splitext(os.path.basename(grammar))[0]
    fsg_path = "{0}/{1}.fsg".format(grammar_path, grammar_name)
    if not os.path.exists(fsg_path):  # create FSG grammar if not available
        jsgf = ps.Jsgf(grammar)
        rule = jsgf.get_rule("{0}.{0}".format(grammar_name))
        fsg = jsgf.build_fsg(rule, decoder.get_logmath(), 7.5)
        fsg.writefile(fsg_path)
        print('Successful JSFG to FSG conversion!!!')

    # Pass the fsg file into the decoder
    decoder.set_fsg(grammar_name, fsg)  # <--- BUG IS HERE!!!

except Exception as e:
    print('Ach no! {0}'.format(e))
finally:
    os.remove(grammar.split('.jsgf')[0] + '.fsg')  # Remove again to help prove that the grammar to fsg conversion isn't at fault


# ProjetInfo_SpeechRecognition
## Projet Option Info 2019 - Centrale Lyon
## Contrôle du robot NAO par la parole

### Fichiers Python:
* essai_cmu_sphinx.py.py* et *test_pocketSphinx.py*: Tests (non-concluants) de la librairie PocketSphinx sans la surcouche SpeechRecognition. Visaient à afficher en temps réel les hypothèses de Sphinx.

* *listage_micros.py*: liste les périphériques audios disponibles sur un PC. Permet de déterminer le numéro de device correspondant au micro à utiliser dans les programmes d'enregistrement/de Speech Recognition. À lancer en premier.

* *jsgf_to_fsg.py*: Convertit un fichier de grammaire Java Speech Grammar File en fichier fsg utilisable par Sphinx, et prenant en compte le modèle utilisé. Pour modifier la grammaire, modifier le fichier *EN-NAO/GrammarNAO.jsgf* puis lui appliquer *jsgf_to_fsg.py*.

* *test_Sphinx_GoogleSpeech.py*: Test du module SpeechRecognition de Python avec la bibliothèque PocketSphinx et l'API gratuite de Speech Recognition de Google. On peut utiliser Sphinx en mode 'Hotwords' ou en mode 'Fonctionnement avec grammaire'.

* *essai_SpeechRecognition.py*: Test de l'API Google Cloud Speech. Ca marche très bien, en temps réel (-> pas de délai sur les instructions), mais il faut s'inscrire à Google Cloud et entrer sa carte bleue. C'est payant au bout de 30min de requêtes par mois.

### Dossier EN-NAO:
Ce dossier contient le modèle utilisé par Sphinx pour la reconnaissance vocale. Il comprend:
* Un modèle acoustique (reconnaissance des phonèmes): *acoustic-model*.
* Un modèle de langage: *language-model.lm.bin*
* Un dictionnaire de prononciation: *pronounciation-dictionary.dict*
* Une grammaire: *GrammarNAO.jsgf*, à laquelle correspond le fichier utilisé par Sphinx *GrammarNAO.fsg*

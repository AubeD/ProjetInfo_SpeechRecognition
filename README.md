# ProjetInfo_SpeechRecognition
## Projet Option Info 2019 - Centrale Lyon
## Contrôle du robot NAO par la parole

### Environnement de développement
* **OS**: Windows 10
* **Python**: 3.6.5, distribution Anaconda

### Prérequis
**Obligatoires** (faire fonctionner le code):
* Numpy, Matplotlib
* **Speechrecognition**: `pip install SpeechRecognition`, https://pypi.org/project/SpeechRecognition/
* **PocketSphinx**: `python -m pip install --upgrade pip setuptools`;  `wheelpip install --upgrade pocketsphinx`, https://github.com/bambocher/pocketsphinx-python
* **pyAudio**: `pip install pyaudio`
* **winsound**: `pip install winsound`

**Optionnels** (faire fonctionner les archive Python):
* **Google Cloud API**: https://cloud.google.com/speech-to-text/?hl=fr
* **urllib3**: `pip install urllib3`

### Description du projet
Ce projet vise à contrôler le robot NAO grâce à la reconnaissance vocale. Pour cela, on utilise la bibliothèque *offline* CMU Sphinx de C++, à laquelle Python accède grâce au module PocketSphinx et à une surcouche SpeechRecognition.

Il existe un certain nombre d'instructions qui peuvent être reconnues par le code Python. Ce dernier les reconnaît puis les envoie à l'algorithme qui contrôle NAO, afin qu'elles soient effectuées.

### Fonctionnement du projet
Schéma à ajouter

### Structure du projet - code Python
Le projet comprend:
* *config.py*: Fichier contenant les chemins Python, les instructions à reconnaître et les seuils de détection. À modifier en cas de changement de structure du code Python ou de changement des instructions à reconnaître.

* *programme_python_nao.py*: Le programme qui effectue la reconnaissance vocale, traite les résultats obtenus et en déduit les instructions que NAO devra effectuer. Il transmet ensuite ces instructions à l'algorithme contrôlant NAO, qui travaille en parallèle.

* *sphinx_reglage_seuils_anti_surdetection.py*: Le problème avec Sphinx, lorsqu'il écoute du langage avec une grammaire réduite, est qu'il a tendance à assimiler n'importe quelle phrase prononcée à l'une des instructions de NAO. Pour corriger cela, on analyse le niveau de confiance que Sphinx donne aux phrases qu'il reconnaît: si ce dernier est trop faible on rejette l'instruction reconnue come un "faux positif". Ce fichier contient des instruments permettant de déterminer les seuils de confiance en-dessous desquels on rejettera des instructions.

* **archives**: Comprend diverses autres solutions qui ont été envisagées pour le projet mais non retenues. À regarder si l'on souhaite aller plus loin.

* **communication**: Pour l'instant, la communication entre Python et l'algorithme de contrôle de NAO est rudimentaire: Python écrit dans un fichier (buffer) qui est lu de manière asynchrone par l'algorithme, et vice-versa.



* *essai_cmu_sphinx.py.py* et *test_pocketSphinx.py*: Tests (non-concluants) de la librairie PocketSphinx sans la surcouche SpeechRecognition. Visaient à afficher en temps réel les hypothèses de Sphinx.



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

# ProjetInfo_SpeechRecognition
## Projet Option Info 2019 - Centrale Lyon
## Contrôle du robot NAO par la parole

### Environnement de développement
* **OS**: Windows 10, 8
* **Python**: 3.6.5, distribution Anaconda

### Prérequis
**Obligatoires** (faire fonctionner le code):
* Numpy, Matplotlib
* **Speechrecognition**: `pip install SpeechRecognition`, https://pypi.org/project/SpeechRecognition/
* **PocketSphinx**: `python -m pip install --upgrade pip setuptools`;  `wheelpip install --upgrade pocketsphinx`, https://github.com/bambocher/pocketsphinx-python
* **pyAudio**: `pip install pyaudio`. Peut nécessiter d'installer MS VisualStudio au préalable.
* **winsound**: `pip install winsound`

**Optionnels** (faire fonctionner les archive Python):
* **Google Cloud API**: https://cloud.google.com/speech-to-text/?hl=fr
* **urllib3**: `pip install urllib3`

### Description du projet
Ce projet vise à contrôler le robot NAO grâce à la reconnaissance vocale. Pour cela, on utilise la bibliothèque *offline* CMU Sphinx de C++, à laquelle Python accède grâce au module PocketSphinx et à une surcouche SpeechRecognition.

Il existe un certain nombre d'instructions qui peuvent être reconnues par le code Python. Ce dernier les reconnaît puis les envoie à l'algorithme qui contrôle NAO, afin qu'elles soient effectuées.

### Fonctionnement du projet
![Schema du fonctionnement](https://github.com/AubeD/ProjetInfo_SpeechRecognition/blob/master/schema/schema.PNG)

### Structure du projet - code Python
Le projet comprend :
* *config.py*: Fichier contenant les chemins Python, les instructions à reconnaître et les seuils de détection. À modifier en cas de changement de structure du code Python ou de changement des instructions à reconnaître.

* *programme_python_nao.py*: Le programme qui effectue la reconnaissance vocale, traite les résultats obtenus et en déduit les instructions que NAO devra effectuer. Il transmet ensuite ces instructions à l'algorithme contrôlant NAO, qui travaille en parallèle.

* *sphinx_reglage_seuils_anti_surdetection.py*: Le problème avec Sphinx, lorsqu'il écoute du langage avec une grammaire réduite, est qu'il a tendance à assimiler n'importe quelle phrase prononcée à l'une des instructions de NAO. Pour corriger cela, on analyse le niveau de confiance que Sphinx donne aux phrases qu'il reconnaît : si ce dernier est trop faible, on rejette l'instruction reconnue comme un "faux positif". Ce fichier contient des instruments permettant de déterminer les seuils de confiance en dessous desquels on rejettera des instructions.

* **EN-NAO**: Contient le modèle de langage Sphinx utilisé pour la reconnaissance vocale.

* **records**: Comprend l'ensemble des extraits sonores enregistrés afin de déterminer les seuils de rejets des différentes instructions. Voir *sphinx_reglage_seuils_anti_surdetection.py*.

* **scripts_utilitaires**: Comprend divers scripts à utiliser en cas de problème lors de l'exécution du code Python.

* **archives**: Comprend diverses autres solutions qui ont été envisagées pour le projet mais non retenues. À regarder si l'on souhaite aller plus loin.

* **communication**: Pour l'instant, la communication entre Python et l'algorithme de contrôle de NAO est rudimentaire: Python écrit dans un fichier (buffer) qui est lu de manière asynchrone par l'algorithme, et vice-versa.

* **logs**: Contient les fichiers de logs permettant de débugger/d'analyser le fonctionnement des différents programmes, et un outil (*mtail.exe*, disponible sur http://ophilipp.free.fr/op_tail.htm, développé par Olivier Philippe) permettant de les lire au fur et à mesure de leur écriture.

### Guide d'utilisation

#### Faire fonctionner le programme Python

1. Cloner ce répertoire et adapter si nécessaire les chemins dans le fichier *config.py*

2. Lancer le fichier *programme_python_nao.py* et lire (avec *mtail.exe* ou son propre programme):
    * Les informations remontées par le programme dans *logs/log_Python.py*
    * Les informations transmises au programme contrôlant NAO dans *communication/buffer_entendu.txt* (texte entendu par NAO) et *communication/buffer_compris.txt* (instructions à transmettre au robot).

**En cas de problème avec le micro...**

De base, SpeechRecognition utilise le micro "Par défaut" de l'ordinateur considéré, avec un Sample Rate (fréquence d'échantillonnage) de 16000 Hz. Le périphérique utilisé peut ne pas être celui voulu, ou ne pas fonctionner ave le Sample Rate par défaut. Pour régler ce problème :

1. Lancer le programme *scripts_utilitaires/listage_micros.py* pour afficher l'ensemble des périphériques disponibles et leurs paramétrages.

2. Entrer le couple (périphérique à utiliser, sample rate) dans le fichier *config.py*.

#### Modifier les seuils de rejet des différentes instructions
1. Enregistrer des extraits sonores correspondants aux différentes instructions que NAO devra comprendre à l'aide du fichier *sphinx_reglage_seuils_anti_surdetection.py* (à la fin, décommenter la boucle *while(1)...* et commenter le reste).

2. Enregister des extraits sonores correspondant à des identifications erronées (FP) par Sphinx des différentes instructions à comprendre. Pour cela, il faut placer un micro dans une salle où ont lieu des conversations sans rapport avec les instructions du robot, et enregistrer en continu à l'aide de la fonction *enregistrer_FP_en_continu* du programme précédent (encore une fois, décommenter le bloc correspondant dans le programme Python).

3. Visualiser les scores obtenus par les hypothèses de Sphinx lorsqu'il identifie à raison des instructions (TP) et lorsqu'il les identifie à tort (FP). Déterminer ainsi, visuellement, en dessous de quel score on va rejeter les hypothèses de Sphinx. Pour cela, décommenter le bloc correspondant à *visualiser_TP_FP* dans le fichier Python précédent.

4. Modifier les seuils dans le dictionnaire *instructions* du fichier *config.py*

#### Modifier le vocabulaire et la grammaire compris par NAO

*Modification du dictionnaire*
1. Lister TOUS les mots que NAO devra pouvoir comprendre. Ils devront être présents dans *EN-NAO/pronounciation-dictionary.dict*.

2. Les copier-coller depuis *EN-NAO/pronounciation-dictionary-original.dict* vers *EN-NAO/pronounciation-dictionary.dict* (ou trouver leur phonétique s'ils n'y sont pas, et les entrer dans notre dictionnaire).

*Modification de la grammaire*
1. Lister les instructions que NAO devra pouvoir comprendre. En déduire un ensemble de structures de phrases possibles, en gardant à l'esprit qu'il faut que certaines ne correspondent pas à des instructions (dans le cas contraire, Sphinx considérera n'importe quoi comme une instruction...).

2. Modifier le fichier de grammaire *EN-NAO/GrammarNAO.jsgf* en s'appuyant:
    * Sur le fichier pré-existant pour garder la même structure en ajoutant par exemple de nouveaux sujets, noms, verbes possibles.
    * Sur les guides de syntaxe suivants : https://www.w3.org/TR/jsgf/ , http://www.gavo.t.u-tokyo.ac.jp/~kuenishi/java/sphinx4/edu/cmu/sphinx/jsapi/JSGFGrammar.html , https://developer.syn.co.in/tutorial/speech/jsgf-grammar.html

3. Parser la grammaire en utilisant le fichier *EN-NAO/jsgf_to_fsg.py* (adapter les chemins).

À noter : Si la grammaire s'appelle 'nom_grammaire.jsgf', la règle qui sera lue sera celle qui se nomme nom_grammaire, et seulement elle. Attention lors de la construction de la grammaire, donc (-> faire une arborescence dont la base est nom_grammaire).

#### Procédure pour modifier ce que NAO comprend

1. Établir sur papier la liste de mots et les enchaînements possibles correspondants aux différentes instructions.

2. Modifier le dictionnaire phonétique.

3. Modifier et parser la grammaire utilisée.

4. Refaire le système de seuils : supprimer dans *records* les dossiers correspondant aux instructions que l'on utilisera plus (si on veut les réutiliser plus tard on pourra les retrouver avec le système de versionnement de Github :-) ), et appliquer "Modifier les seuils de rejet des différentes instructions" (de nouveaux dossiers seront créés automatiquement si besoin).

5. Tester si le tout fonctionne, éventuellement modifier la grammaire ou les seuils, etc...

#### Utiliser les programmes archivés

1. Télécharger les dépendances optionnelles si ce n'est pas déjà fait.

2. Régler les chemins et paramétrages à la main (le fichier *config.py* n'est pas utilisé).

3. Pour utiliser *archives/essai_google_cloud_speech.py*, créer un compte Google Cloud et entrer une carte bleue.

4. Se connecter à Internet pour pouvoir se servir des APIs en ligne !

5. Lancer le programme à utiliser.

### Reste à faire :

* Intégrer la partie du projet rédigée en code C++

* Intégrer un système permettant d'interrompre l'écoute ("bouton on/off"), et une "zone de doute" dans laquelle NAO nous demande si on a effectivement prononcé certaines instructions (pour adoucir le rejet de faux positifs en mode "tout ou rien").

Ce dossier comprend les fichiers nécessaires pour la compréhension du langage par sphinx:

* Le fichier *pronunciation-dictionary.dict* contient les mots qui pourront être reconnu par sphinx avec leur prononciation (liste des phonèmes). Nous n'y avons mis que les mots nécessaires à notre application. C'est donc un dictionnaire très léger. Il est possible de rajouter des mots si besoin est.
* Le dictionnaire anglais complet est également présent : *pronunciation-dictionary-original.dict*, il est présent pour permettre de rajouter de nouveau mots plus facilement. En effet, il suffit de chercher dans ce dictionnaire le mot à ajouter puis de copier-coller la ligne correspondante dans le dictionnaire *pronunciation-ditionary.dict*. Cela permet d'avoir la liste des phonèmes du mots sous le bon format.
* *language-model.lm.bin* est le modèle de language, il permet une mise en contexte des mots et une analyse des phrases selon la langue, c'est la sémantique.
* La grammaire représentent tous les enchaînements de mots possibles, il y a deux fichiers de grammaire :
	* *GrammarNAO.jsgf* est le fichier dans lequel nous avons rentré notre grammaire (voir le format utilisé : https://en.wikipedia.org/wiki/JSGF)
	* *GrammarNAO.fsg* est le fichier précédent, compilé à l'aide de Sphinx afin que ce dernier puisse s'en servir.

Il comprend de plus le fichier *jsgf_to_fsg.py*, qui permet de compiler *GrammarNAO.jsgf* à l'aide du modèle Sphinx pour obtenir *GrammarNAO.fsg*.

Les fichiers C++ sont présents sur l'ordinateur de la salle Amigo de l'école Centrale de Lyon.

naoKinect3 - Voix est le projet final. Il faut ouvrir naoKinectVoix(Type: Microsoft Visual Studio Solution) dans C:\Users\wang\Desktop\song\myProject\naoKinect3 - Voix\naoKinectVoix de l'ordinateur de la salle Amigo.

Cela fonctionne avec Visual studio 2010 mais il faut ajouter deux fichiers head de Visual Studio 2013 (sal.h, ConcurrencySal.h) dans C:\Program Files\Microsoft SDKs\Kinect\v2.0_1409\inc
En effet, par défaut, Kinect v2.0 SDK fonctionne au moins avec vs2013 alors que nao C++ SDK marche seulement vs2010.

Cette étape a été effectuée sur l'ordinateur de la salle Amigo mais il faudra la faire si on veut implémenter le projet sur un autre ordinateur, sinon le build ne fonctionnera pas.

Kinect v2 SDK est installé dans C:\Program Files\Microsoft SDKs\Kinect\v2.0_1409
Nao C++ SDK est installé dans C:\Users\wang\NAO\naoqi-sdk-2.1.4.13-win32-vs2010
Le projet vs a été créé par cmake qui est installé dans C:\Program Files (x86)\CMake

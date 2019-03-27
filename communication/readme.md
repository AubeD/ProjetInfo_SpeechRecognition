Ce dossier comprend les buffers de communication *Python -> C++* et *C++ -> Python*. Il comporte:

**Python -> C++**:
* *buffer_entendu.txt*: Lorsque Sphinx comprend une instruction, le code Python l'écrit dans ce fichier afin que le code C++ l'affiche dans une boîte de dialogur. Cela permet à l'utilisateur d'avoir une idée de ce que Sphinx entend, au cas où la reconnaissance vocale ne fonctionnerait pas parfaitement.

* *buffer_compris.txt*: Lorsque Python confirme une instruction comprise par Sphinx, il l'écrit dans ce fichier pour que le programme C++ la fasse exécuter par NAO.

**C++ -> Python**
* *buffer_C.txt*: Permet l'envoi d'instruction de la part du programme C++ vers le programme Python. Par exemple lorsque le programme C++ s'arrête, il écrit "stop" dans ce fichier. Python s'arrête lorsqu'il le lit. Les autres instructions possibles sont "pause" et "reprise".

# definisce una funzione che restituisce tutti i file di una directory corrente
# in formato di stringa
# ogni modulo dovrebbe avere questa funziona per standrdizzare il caricamento dei moduli
#

import os

def run(**args):
    print "[*] In dirlist module."
    files = os.listdir(".")

    return str(files)





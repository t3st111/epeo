# modulo che recupera le variabili d'ambiente del ristema su cui gira


import os

def run(**args):
    print "[*] In enviroment module."
    return str(os.environ)




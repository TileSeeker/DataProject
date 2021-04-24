# -*- coding: utf-8 -*-
"""
@author: Sveien (emism)

Oppsett av Signal class for henting og skriving av data 
fra og til Circus of Things.
"""
import requests
import json

class Signal:
    """
    setter opp en self/__init__ som vil kjøre da funksjonen kalles,
    denne vil lagre key og token i variablen som funksjonen kalles i.
    (dette må gjøres for å kunne benytte andre de andre kommandoene til Signal)
    """
    def __init__(self, key, token):
        self.key = key
        self.token = token
    
    """
    .get har ingen variabelinputt. .get benytter requests.get for å lese av
    data fra CoT. deretter henter data ved bruk av json.loads og til slutt 
    returnerer delve verdien til signalet "Value".
    """
    def get(self):
        response = requests.get('https://circusofthings.com/ReadValue',
                                params = {'Key':self.key,
                                          'Token':self.token})
        response = json.loads(response.content)
        
        return response["Value"]
    
    """
    .write her en variabelinput, altså verien som ønsker å skrives til signalet.
    her benyttes requests.put, sammenslått med json.dumps for å dumpe/overskrive
    data. Deretter en simpel if/else logikk som sier ifra hvis en feil oppstår.
    """
    def write(self, value):
        response = requests.put('https://circusofthings.com/WriteValue',
                                data = json.dumps({'Key':self.key,
                                                   'Value':value,
                                                   'Token':self.token}),
                                headers ={"Content-Type":"application/json"})
        
        if (response.status_code == 200):
            return "Success"
        else:
            return "error %d" % (response.status_code)

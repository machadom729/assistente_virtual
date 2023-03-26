from vosk import Model, KaldiRecognizer
import pyaudio
import pyttsx3
import json
import os
import core
from nlu.classificador import classifica

# síntese de fala

texto_fala = pyttsx3.init()

voices = texto_fala.getProperty('voices')
texto_fala.setProperty('voice', voices[-2].id)


def falar(texto):
    texto_fala.say(texto)
    texto_fala.runAndWait()


def avaliar(text):
    entidade = classifica(text)
    if entidade == 'time|getTime':
        falar(core.SystemInfo.get_time())
    elif entidade == 'time|getDate':
        falar(core.SystemInfo.get_date())
    # Abrir programas
    elif entidade == 'open|notepad':
        falar('Abrindo o bloco de notas')
        os.system('notepad.exe')
    elif entidade == 'open|chrome':
        falar('Abrindo o google chrome')
        os.system('"C:/Program Files/Google/Chrome/Application/chrome.exe"')
    elif entidade == "open|calc":
        falar("Abrindo a calculadora")
        os.system('"calc.exe')
    elif entidade == "open|email":
        falar("Abrindo a calculadora")
        os.system('"outlook.exe')

    print('Text: {}  Entity: {}'.format(text, entidade))

# reconhecendo a voz


model = Model("model")
rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000,
                input=True, frames_per_buffer=2048)
stream.start_stream()

while True:
    data = stream.read(2048)
    if len(data) == 0:
        break

    if rec.AcceptWaveform(data):
        result = rec.Result()
        result = json.loads(result)

        if result is not None:
            texto = result['texto']
            avaliar(texto)

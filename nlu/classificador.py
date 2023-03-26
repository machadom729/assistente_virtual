from tensorflow.keras.models import load_model
import numpy as np


modelo = load_model("model.h5")

rotulos = open("rotulos.txt", "r", encoding="utf-8").read().split("\n")

rotulo2idx = {}
idx2rotulo = {}

for k, rotulo in enumerate(rotulos):
    rotulo2idx[rotulo] = k
    idx2rotulo[k] = rotulo


def classifica(texto):
    x = np.zeros((1, 24, 256), dtype="float32")

    for k, ch in enumerate(bytes(texto.encode("utf-8"))):
        x[0, k, int(ch)] = 1.0

    saida = modelo.predict(x)
    idx = saida.argmax()
    return idx2rotulo[idx]


while True:
    texto = input("dasd: ")
    print(classifica(texto))

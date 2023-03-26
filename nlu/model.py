import yaml
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical


data = yaml.safe_load(open("nlu/train.yml", "r", encoding="utf-8").read())

entradas, saidas = [], []

for comando in data["comandos"]:
    entradas.append(comando["entrada"])
    saidas.append(f"{comando['entidade']}\{comando['acao']}")

chars = set()

for entrada in entradas + saidas:
    for ch in entrada:
        if ch not in chars:
            chars.add(ch)

chr2idx = {}
idx2chr = {}

for i, ch in enumerate(chars):
    chr2idx[ch] = i
    idx2chr[i] = ch

maior_seq = max([len(bytes(x.encode("utf-8"))) for x in entradas])

dados_entrada = np.zeros((len(entradas), maior_seq, 256), dtype="float32")

for i, entrada in enumerate(entradas):
    for k, ch in enumerate(bytes(entrada.encode("utf-8"))):
        dados_entrada[i, k, int(ch)] = 1.0

rotulos = set(saidas)
dados_saida = []

salva = open("rotulos.txt", "w", encoding="utf-8")

rotulo2idx = {}
idx2rotulo = {}

for k, rotulo in enumerate(rotulos):
    rotulo2idx[rotulo] = k
    idx2rotulo[k] = rotulo
    salva.write(rotulo + "\n")

salva.close()

for saida in saidas:
    dados_saida.append(rotulo2idx[saida])

dados_saida = to_categorical(dados_saida, len(dados_saida))


modelo = Sequential()
modelo.add(LSTM(128))
modelo.add(Dense(len(dados_saida), activation="softmax"))

modelo.compile(optimizer="adam",
               loss="categorical_crossentropy",
               metrics=["categorical_accuracy"])

# modelo.summary()

modelo.fit(dados_entrada, dados_saida, epochs=120)

modelo.save("model.h5")


def classifica(texto):
    x = np.zeros((1, 48, 256), dtype="float32")

    for k, ch in enumerate(bytes(texto.encode("utf-8"))):
        x[0, k, int(ch)] = 1.0

    saida = modelo.predict(x)
    idx = saida.argmax()
    print(idx2rotulo[idx])

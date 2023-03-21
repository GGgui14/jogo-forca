from termcolor import colored
from nltk.corpus import wordnet
from random import choice
from translate import Translator
from requests import get
from requests import ConnectionError
from platform import system
from texttable import Texttable
from time import sleep
import os


def clear():
    if system() == "Windows":
        os.system('cls')
    else:
        os.system('clear')


def is_connected():
    try:
        # Tentando conectar a um site conhecido
        response = get("http://www.google.com")
        return response.status_code == 200
    except ConnectionError:
        pass
    return False


# baixa a lista de palavras caso o usuario não tenha.
if not os.path.exists("7776palavras.txt"):
    url = "https://raw.githubusercontent.com/thoughtworks/dadoware/master/7776palavras.txt"
    response = get(url)

    with open("7776palavras.txt", "wb") as f:
        f.write(response.content)


# lendo a lista de palavras
def palavra_secreta():
    with open("7776palavras.txt", 'r') as worlist:
        secret_word = choice(worlist.readlines())
        while len(secret_word) < 4:
            secret_word = choice(worlist.readlines())

        return secret_word


palavra = palavra_secreta()

word = palavra.lower()

# traduz a palavra de pt-br para inglês
translator = Translator(from_lang="pt-br", to_lang="en")
palavra_en = translator.translate(word)


def busca_definicao(palavra1):
    # busca a definição de uma palavra
    for syn in wordnet.synsets(palavra1):
        word_definition = syn.definition()

    try:
        translator = Translator(from_lang="en", to_lang="pt-br")
        translation_def = translator.translate(word_definition)
        return translation_def
    except NameError:
        print(colored("Definição não encontrada", "red"))


def busca_sinonimo(palavra1):
    synonyms = list()
    # busca sinônimos de uma palavra
    for syn in wordnet.synsets(palavra1):
        for lemma in syn.lemmas():
            synonyms.append(lemma.name())

    try:
        sinonym = choice(synonyms)

        translator = Translator(from_lang="en", to_lang="pt-br")
        translation_sin = translator.translate(sinonym)
        return translation_sin
    except IndexError:
        print(colored("Sem definições encontradas", "red"))


""" print(palavra)
print(busca_definicao(palavra_en))
print(busca_sinonimo(palavra_en)) """

# transforma a palavra de  letras(abcd) para underline(_ _ _ _ )


def palavra_codificada(word):
    l = list()
    for c in range(len(word) - 1):
        l.append("_" if word[c] != " " else " ")

    return l


def verifica_letra(letter):
    if letter in word:
        if word.count(letter) == 1:
            return word.index(letter)
        else:
            positions = list()

            index = word.find(letter)

            while index >= 0:
                positions.append(index)
                index = word.find(letter, index + 1)

            return positions
    else:
        return False


##################################################################################
def verifica_palavra(palavra_tentativa, palavra_original):
    p = len(palavra_original) - 1
    for c in range(len(palavra_original) - 1):
        if palavra_tentativa[c] == palavra_original[c]:
            p -= 1

    if p == 0:
        return True
    else:
        return False


tentativas = 5
palavra_cod = palavra_codificada(word)


def menu():
    tab = Texttable(max_width=1000)

    def show_attempts():
        cor = ""

        if tentativas >= 4:
            cor = 'green'
        elif tentativas >= 2:
            cor = 'yellow'
        else:
            cor = 'red'

        print(f"Tentativas: {colored(tentativas, cor)}")

    def show_secret_word():
        mostrar_palavra_cod = "".join([str(i) for i in palavra_cod])
        tab.add_rows([mostrar_palavra_cod])
        print(tab.draw())

    while True:
        show_secret_word()
        print('\n\n')
        if is_connected() == False:
            print(
                "Sem conexão com a internet, as opções [1] e [2] não estão disponíveis.")
        print(
            colored("Digite uma das opções abaixo se tiver em duvida da palavra", "yellow"))
        print(
            f"[1] Sinonimo [{colored('ON', 'green') if is_connected() else colored('OFF', 'red')}]")
        print(
            f"[2] Definição [{colored('ON', 'green') if is_connected() else colored('OFF', 'red')}]")
        print("\n\n")
        show_attempts()
        print(colored("[!] Digite uma letra ou a palavra toda!", "yellow"))

        tentativa = str(input(">")).lower()

        if tentativa.isnumeric():
            if int(tentativa) == 1:
                print(colored(busca_sinonimo(palavra_en),
                      "red", "on_yellow", ['bold']))
            elif int(tentativa) == 2:
                print(colored(busca_definicao(palavra_en),
                      "red", "on_yellow", ['bold']))
        else:
            break

    return tentativa


while tentativas > 0:
    clear()
    print(word)  # ////

    tentativa = str(menu())

    if len(tentativa) == 1:
        if type(verifica_letra(tentativa)) == int:
            palavra_cod[verifica_letra(tentativa)] = tentativa
        elif type(verifica_letra(tentativa)) == list:
            for p in verifica_letra(tentativa):
                palavra_cod[p] = tentativa
        else:
            print(colored("Letra não encontrada", "red"))
            tentativas -= 1

        if palavra_cod.count("_") == 0:
            mostrar_palavra_cod = " ".join([str(i) for i in palavra_cod])
            print(mostrar_palavra_cod)
            print(colored("Você acertou todas as letras", "green"))
            break

    elif len(tentativa) > 1:
        if len(tentativa) == len(word) - 1:
            if verifica_palavra(tentativa, word):
                print(colored("Você acertou", "green"))
                break
            else:
                print(colored("Você errou", "red"))
                tentativas -= 1
        else:
            print(colored("Você errou", "red"))
            tentativas -= 1

    sleep(3)
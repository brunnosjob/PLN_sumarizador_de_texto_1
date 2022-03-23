#!/usr/bin/env python
# coding: utf-8

# In[217]:


#Importando as bibliotecas de base
import nltk #Tratamento dos textos
import spacy #Tratamento dos textos
import string #Tratamento de strings
import re #Tratamento de caracteres
import numpy #Tratamento numérico-matemático-científico
import pandas #Criação e manipulação de tabelas e series
import heapq #Selecionar melhores sentenças

#Importando módulos
from IPython.core.display import HTML #Gerar de textos por HTML
from goose3 import Goose #Extrair de textos html

#Aplicando url em variável
url = ''

#Criando função (algoritmo) de geração de resumo
def sumarizador(url, n_sentencas):
    
    #Criando objeto Goose, extraindo dados HTML e armazenando dados
    g = Goose()
    documento = g.extract(url)

    #Armazenando informações
    titulo = documento.title
    texto_original = documento.cleaned_text
    dominio = documento.domain
    
    #Armazenando stopwords e pontuações
    stpwrds = nltk.corpus.stopwords.words("portuguese")
    pontuacoes = string.punctuation
    
    tokens = [] #Recebe texto tokenizado
    texto_limpo = [] #Recebe texto pré-processado
    
    
    #Remoção de espaços, quebras de linha e convertendo maiúsculas em minúsculas
    texto = re.sub("\n+", "", texto_original)
    texto = re.sub(" +", " ", texto)
    texto = texto.replace("R$", "*RS")
    texto = texto.lower()
    
    #Tokenizando o texto
    for token in nltk.word_tokenize(texto):
        tokens.append(token)
        
    #Eliminando stopwords
    texto_limpo = [elemento for elemento in tokens if elemento not in stpwrds and elemento not in pontuacoes]
    
    #Unificando texto limpo
    texto_limpo = ' '.join(texto_limpo)
    
    #Gerando frequência de palavras
    freq_palavras = nltk.FreqDist(nltk.word_tokenize(texto_limpo))
    freq_max = max(freq_palavras.values())
    
    #Geração dos pesos
    for palavra in freq_palavras.keys():
        freq_palavras[palavra] = (freq_palavras[palavra]/freq_max)
        
    #Gerando as notas das sentenças
    sentencas_tokenizadas = nltk.sent_tokenize(texto)
    notas_sentencas = {}
    for sentenca in sentencas_tokenizadas:
        for palavra in nltk.word_tokenize(sentenca):
            if palavra in freq_palavras.keys():
                if sentenca not in notas_sentencas.keys():
                    notas_sentencas[sentenca] = freq_palavras[palavra]
                else:
                    notas_sentencas[sentenca] += freq_palavras[palavra]
                    
    #Selecionando as melhores sentenças
    melhores_sentencas = heapq.nlargest(n_sentencas, notas_sentencas, key=notas_sentencas.get)
    
    #Gerando resumo
    resumo = ' '.join(melhores_sentencas)
    
    #Gerando interface HTML
    texto_html = ''
    display(HTML(f"<h1>Resumo</h1>"))
    display(HTML(f"""<footer>Domínio: {dominio}</footer>"""))
    display(HTML(f"<footer>*OBS: R$ é substituído por rs</footer>"))
    display(HTML(f"""<h2>{titulo}<h/>"""))
    for sentenca in sentencas_tokenizadas:
        if sentenca in melhores_sentencas:
            texto_html += str(sentenca).replace(sentenca, f"<mark style='background-color: yellow'>{sentenca}</mark>")
        else:
            texto_html += sentenca
            
    return display(HTML(f"""{texto_html}"""))

#Testando algoritmo
sumarizador(url, 2)


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
import streamlit as st

#Importando módulos
from nltk import word_tokenize
from IPython.core.display import HTML #Gerar de textos por HTML
from goose3 import Goose #Extrair de textos html

#Aplicando url em variável
st.markdown('*__Observação: para mais informações acerca do projeto, clique na seta no canto esquerdo superior da tela__*')
st.markdown(' ')

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
    stpwrds = ['de', 'a', 'o', 'que', 'e', 'é', 'do', 'da', 'em', 'um', 'para', 'com', 'não', 'uma', 'os', 'no', 'se', 'na', 'por', 'mais', 'as', 'dos', 'como', 'mas', 'ao', 'ele', 'das', 'à', 'seu', 'sua', 'ou', 'quando', 'muito', 'nos', 'já', 'eu', 'também', 'só', 'pelo', 'pela', 'até', 'isso', 'ela', 'entre', 'depois', 'sem', 'mesmo', 'aos', 'seus', 'quem', 'nas', 'me', 'esse', 'eles', 'você', 'essa', 'num', 'nem', 'suas', 'meu', 'às', 'minha', 'numa', 'pelos', 'elas', 'qual', 'nós', 'lhe', 'deles', 'essas', 'esses', 'pelas', 'este', 'dele', 'tu', 'te', 'vocês', 'vos', 'lhes', 'meus', 'minhas', 'teu', 'tua', 'teus', 'tuas', 'nosso', 'nossa', 'nossos', 'nossas', 'dela', 'delas', 'esta', 'estes', 'estas', 'aquele', 'aquela', 'aqueles', 'aquelas', 'isto', 'aquilo', 'estou', 'está', 'estamos', 'estão', 'estive', 'esteve', 'estivemos', 'estiveram', 'estava', 'estávamos', 'estavam', 'estivera', 'estivéramos', 'esteja', 'estejamos', 'estejam', 'estivesse', 'estivéssemos', 'estivessem', 'estiver', 'estivermos', 'estiverem', 'hei', 'há', 'havemos', 'hão', 'houve', 'houvemos', 'houveram', 'houvera', 'houvéramos', 'haja', 'hajamos', 'hajam', 'houvesse', 'houvéssemos', 'houvessem', 'houver', 'houvermos', 'houverem', 'houverei', 'houverá', 'houveremos', 'houverão', 'houveria', 'houveríamos', 'houveriam', 'sou', 'somos', 'são', 'era', 'éramos', 'eram', 'fui', 'foi', 'fomos', 'foram', 'fora', 'fôramos', 'seja', 'sejamos', 'sejam', 'fosse', 'fôssemos', 'fossem', 'for', 'formos', 'forem', 'serei', 'será', 'seremos', 'serão', 'seria', 'seríamos', 'seriam', 'tenho', 'tem', 'temos', 'tém', 'tinha', 'tínhamos', 'tinham', 'tive', 'teve', 'tivemos', 'tiveram', 'tivera', 'tivéramos', 'tenha', 'tenhamos', 'tenham', 'tivesse', 'tivéssemos', 'tivessem', 'tiver', 'tivermos', 'tiverem', 'terei', 'terá', 'teremos', 'terão', 'teria', 'teríamos', 'teriam']
    pontuacoes = string.punctuation
    
    tokens = [] #Recebe texto tokenizado
    texto_limpo = [] #Recebe texto pré-processado
    
    
    #Remoção de espaços, quebras de linha e convertendo maiúsculas em minúsculas
    texto = re.sub("\n+", "", texto_original)
    texto = re.sub(" +", " ", texto)
    texto = texto.replace("R$", "*RS")
    texto = texto.lower()
    
    #Tokenizando o texto
    for token in texto.split():
        tokens.append(token)
        
    #Eliminando stopwords
    texto_limpo = [elemento for elemento in tokens if elemento not in stpwrds and elemento not in pontuacoes]
    
    #Unificando texto limpo
    texto_limpo = ' '.join(texto_limpo)
    
    #Gerando frequência de palavras
    freq_palavras = nltk.FreqDist([word for word in texto_limpo.split()])
    freq_max = max(freq_palavras.values())
    
    #Geração dos pesos
    for palavra in freq_palavras.keys():
        freq_palavras[palavra] = (freq_palavras[palavra]/freq_max)
        
    #Gerando as notas das sentenças
    sentencas_tokenizadas = []
    for sent in texto_original.split('.'):
        sentencas_tokenizadas.append(sent)
    notas_sentencas = {}
    for sentenca in sentencas_tokenizadas:
        for palavra in sentenca.split():
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
url = st.text_input('Cole/digite o link da página do site de onde você gostaria de obter o resumo ou fichamento das melhores partes do texto')
if st.button('Gerar resumo'):
    sumarizador(url, 2)


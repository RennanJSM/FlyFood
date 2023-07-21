import numpy as np
import random
import operator 
import pandas as pd
with open('input.txt', 'r') as readfile:
    file = open('input.txt', 'r')

coordenadas = {}
largura, altura = (file.readline().split())
linhas = file.read().splitlines()
lista_pontos = list()
for locais in range(int(largura)):
    linha = linhas[locais].split()
    for pontos in linha:
        if pontos != '0':
            coordenadas[pontos] = (locais, linha.index(pontos))
            lista_pontos.append(pontos)

class Ponto:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distancia(self, proximo_ponto):
        return ((self.x - proximo_ponto.x) + (self.y - proximo_ponto.y))

    def __repr__(self):
        return '(' + str(self.x) + ',' + str(self.y) + ')'

def CriarRota(lista_pontos):
    rota = random.sample(lista_pontos, len(lista_pontos))
    return rota

def PopulacaoInicial(tam_populacao, lista_pontos):
    populacao = []
    for i in range(0, tam_populacao):
        populacao.append(CriarRota(lista_pontos))
    return populacao

class Aptidao:
    def __init__(self, rota):
        self.rota = rota
        self.distancia = 0
        self.aptidao = 0.0

    def tamanho_rota(self):
        if self.distancia ==0:
            custo = 0
            for i in range(0, len(self.rota)):
                ponto_atual = self.rota[i]
                proximo_ponto = None

                if (i + 1) < len(self.rota):
                    proximo_ponto = self.rota[i +1]
                else:
                    proximo_ponto = self.rota[0] 
                custo += ponto_atual.distancia(proximo_ponto)

            self.distancia = custo
        return self.distancia
    
    def aptidao_rota(self):
        if self.aptidao == 0:
            self.aptidao = 1 / float(self.tamanho_rota())
        return self.aptidao

def ranking(populacao):
    res_aptidoes = {}
    for i in range(0, len(populacao)):
        res_aptidoes[i] = Aptidao(populacao[i]).aptidao_rota()
    return sorted(res_aptidoes.items(), key = operator.itemgetter(1), reverse = True)

def selecao(ranking_populacao, tam_elite):
    res_selecao = list()
    df = pd.DataFrame(np.array(ranking_populacao), columns=["índice","Aptidão"])
    df['cum_sum'] = df.Aptidao.cumsum()
    df['cum_perc'] = 100*df.cum_sum/df.Aptidao.sum()
    for i in range(0, tam_elite):
        res_selecao.append(ranking_populacao[i][0])
    for i in range(0, len(ranking_populacao) - tam_elite):
        escolher = 100*random.random()
        for i in range(0, len(ranking_populacao)):
            if escolher <= df.iat[i,3]:
                res_selecao.append(ranking_populacao[i][0])
                break
    return res_selecao

def buscar_individuo(populacao, res_selecao):
    buscar_individuo = list()
    for i in range(0, len(res_selecao)):
        j = res_selecao[i]
        buscar_individuo.append(populacao[j])
    return buscar_individuo

def cruzamento(pai1, pai2):
    filhos = list()
    filhop1 = list()
    filhop2 = list()
    cromossomo1 = int(random.random()*len(pai1))
    cromossomo2 = int(random.random()*len(pai2))
    primeiro_gene = min(cromossomo1, cromossomo2)
    segundo_gene = max(cromossomo1, cromossomo2)
    for i in range(primeiro_gene, segundo_gene):
        filhop1.append(pai1[i])
    filhop2 = [i for i in pai2 if i not in filhop1]
    filhos = filhop1 + filhop2
    return filhos

def produzir_geracao(buscar_individuo, tam_elite):
    nova_geracao = list()
    num_individuos = len(buscar_individuo) - tam_elite
    geracao = random.sample(buscar_individuo, len(buscar_individuo))
    for i in range(0, tam_elite):
        nova_geracao.append(buscar_individuo[i])
    for i in range(0, num_individuos):
        filhos = cruzamento(geracao[i], geracao[len(buscar_individuo)-i-1]) 
        nova_geracao.append(filhos)
    return nova_geracao

def mutacao(individuo, nivel_mutacao):
    for i in range(len(individuo)):
        if (random.random() < nivel_mutacao):
            trocar = int(random.random()*len(individuo))
            cidade1 = individuo[i]
            cidade2 = individuo[trocar]
            individuo[i] = cidade2
            individuo[trocar] = cidade1
    return individuo

def mutacao_populacao(populacao, nivel_mutacao):
    populacao_mut = list()
    for j in range(0, len(populacao)):
        mutantes = mutacao(populacao[j], nivel_mutacao)
        populacao_mut.append(mutantes)
    return populacao_mut

def proxima_geracao(geracao_atual, tam_elite, nivel_mutacao):
    ranking_populacao = ranking(geracao_atual)
    res_selecao = selecao(ranking_populacao, tam_elite)
    buscar_individuo = buscar_individuo(geracao_atual, res_selecao)
    nova_geracao = produzir_geracao(buscar_individuo, tam_elite)
    proxima_geracao = mutacao_populacao(nova_geracao, nivel_mutacao)
    return proxima_geracao

def resultado(populacao_, tamPopulacao, tam_elite, nivel_mutacao, geracoes):
    population = PopulacaoInicial(tamPopulacao, populacao_)
    print('Distância inicial: ' + str(1 / ranking(population)[0][1]))
    for i in range(0, geracoes):
        population = proxima_geracao(population, tam_elite, nivel_mutacao)
    print('Distância final: ' + str(1 / ranking(population)[0][1]))
    indice_melhor_rota = ranking(population)[0][0]
    melhor_rota = population[indice_melhor_rota]
    return melhor_rota

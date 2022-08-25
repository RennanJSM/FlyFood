with open('input.txt', 'r') as readfile:
    file = open('input.txt', 'r')

coordenadas = {}
largura, altura = (file.readline().split())
linhas = file.read().splitlines()
pontos_de_entrega = list()
for locais in range(int(largura)):
    linha = linhas[locais].split()
    for pontos in linha:
        if pontos != '0':
            coordenadas[pontos] = (locais, linha.index(pontos))
            pontos_de_entrega.append(pontos)

def permutar(lista):
    if len(lista) == 0:
        return list()
    if len(lista) == 1:
        return [lista]
    lista_auxiliar = []
    for indice in range(len(lista)):
        termo = lista[indice]
        termos_restantes = lista[:indice] + lista[indice+1:]
        for i in permutar(termos_restantes):
            lista_auxiliar.append([termo] + i)
    return lista_auxiliar
    
custo_otimo = float('inf')
rota_otima = str('inf')
pontos_de_entrega.remove('R')
for rotas in (permutar(pontos_de_entrega)):
    custo_atual = 0
    rotas = list(rotas)
    rotas.insert(0, 'R')
    rotas.append('R')
    for rota_atual in range(len(rotas)-1):
        linha_x = abs(coordenadas[rotas[rota_atual]][1] - coordenadas[rotas[rota_atual+1]][1])
        linha_y = abs(coordenadas[rotas[rota_atual]][0] - coordenadas[rotas[rota_atual+1]][0])
        custo_atual += linha_x + linha_y
    if custo_atual < custo_otimo:
        custo_otimo = custo_atual
        rota_otima = rotas
print(rota_otima, custo_otimo)

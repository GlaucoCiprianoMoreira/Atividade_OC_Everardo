def ler_circuito(arquivo_entrada):
    with open(arquivo_entrada, 'r') as f:
        return eval(f.read())

def calcular_saida(gate, entradas):
    if gate == "and":
        return int(all(entradas))
    elif gate == "nand":
        return int(not all(entradas))
    elif gate == "or":
        return int(any(entradas))
    elif gate == "nor":
        return int(not any(entradas))
    elif gate == "not":
        return int(not entradas[0])
    elif gate == "xor":
        return int(entradas[0] ^ entradas[1])
    elif gate == "nxor":
        return int(not (entradas[0] ^ entradas[1]))
    else:
        raise ValueError(f"Porta lógica desconhecida: {gate}")

def avaliar_circuito(circuito, combinacao):
    entradas = circuito['entradas']
    valores = {var: val for var, val in zip(entradas, combinacao)}

    for gate in circuito['gates']:
        detalhes = circuito[gate]
        tipo = detalhes[0]
        saida = detalhes[1]
        entradas_gate = [valores[entrada] for entrada in detalhes[2:]]
        valores[saida] = calcular_saida(tipo, entradas_gate)

    saidas = [valores[saida] for saida in circuito['saidas']]
    return saidas

def gerar_tabela_verdade(circuito):
    entradas = circuito['entradas']
    num_entradas = len(entradas)
    combinacoes = [[(i >> bit) & 1 for bit in range(num_entradas - 1, -1, -1)] for i in range(2 ** num_entradas)]

    tabela = []
    for combinacao in combinacoes:
        saidas = avaliar_circuito(circuito, combinacao)
        tabela.append(combinacao + saidas)
    return tabela

def escrever_saida(arquivo_saida, circuito, tabela_verdade):
    with open(arquivo_saida, 'w') as f:
        f.write(f"Circuito: {circuito['name']}\n")
        f.write("Tabela Verdade:\n")
        f.write(' '.join(circuito['entradas'] + circuito['saidas']).upper() + '\n')
        for linha in tabela_verdade:
            f.write(" ".join(map(str, linha)) + "\n")

def main(arquivo_entrada, arquivo_saida):
    circuito = ler_circuito(arquivo_entrada)
    tabela_verdade = gerar_tabela_verdade(circuito)
    escrever_saida(arquivo_saida, circuito, tabela_verdade)

entrada = input("Digite o nome do arquivo de entrada (com extensão .txt): ")
saida = input("Digite o nome do arquivo de saída (com extensão .txt): ")
main(entrada, saida)

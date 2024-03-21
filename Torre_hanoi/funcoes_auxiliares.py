import sys
import random

sys.setrecursionlimit(1000000)


#Coleta dos parametros 

def coletar_numero_discos():
    while True:
        try:
            numero_discos = int(input("Digite o número de discos (Numero inteiro): "))
            lista_numero_discos = list(range(1, numero_discos + 1))
            return lista_numero_discos
        except ValueError:
            print("Isso não é um número inteiro.")
            tentar_novamente = input("Deseja tentar novamente? (sim/não): ").lower()
            if tentar_novamente != "sim":
                print("Operação encerrada pelo usuário.")
                sys.exit()

def escolher_metodo_pinos(lista_disco):
    modo = input("Deseja escolher a posição de cada pino?(sim/nao): ").lower()
    if modo =="sim":
        pinos,quantidade_pinos = solicitar_configuracao_pinos(lista_disco)
    
    else:
        pinos,quantidade_pinos =  solicitar_quantidade_pinos_e_configuracao(lista_disco)
        
    return pinos,quantidade_pinos

def solicitar_configuracao_pinos(lista_disco):
    while True:
        quantidade_pinos = int(input("Digite a quantidade de pinos: "))
        valor_original = lista_disco
        pinos = [[] for _ in range(quantidade_pinos)]
        
        for i in range(quantidade_pinos):
            lista_atual = []
            while True:
                if len(lista_disco)==0:
                    break
                print("Valores disponiveis: ",lista_disco)
                discos = int(input(f"Digite um discos no pino {i+1}: "))
                if discos:
                    if discos in lista_disco:
                        lista_disco.remove(discos)
                        lista_atual.append(discos)
                        if len(lista_disco)==0:
                            pinos[i] = lista_atual
                            pinos[i].sort(reverse=True)
                            lista_atual = []
                            break
                            
                    else:
                        print("Esse valor nao esta disponivel")
                confirmacao = input("Quer inserir outro disco ? (sim/nao): ").lower()
                if confirmacao == "sim":
                    pinos[i].sort(reverse=True)
                    
                    
                elif confirmacao == "nao":
                    pinos[i] = lista_atual
                    pinos[i].sort(reverse=True)
                    lista_atual = []
                    break
                    

        print("Configuração atual dos pinos:")
        for i, pino in enumerate(pinos):
            print(f"Pino {i+1}: {pino}")
        
        confirmacao = input("A configuração está correta? (sim/nao): ").lower()
        if confirmacao == "sim":
            break
        elif confirmacao == "nao":
            lista_disco = valor_original
            print("Vamos tentar novamente.")

    return pinos,quantidade_pinos

def solicitar_quantidade_pinos_e_configuracao(lista_discos):
    quantidade_pinos = int(input("Digite a quantidade de pinos: "))
    modo = input("Deseja a configuração padrão do Hanoi (padrao) ou aleatória (aleatorio)? ").lower()
    pinos = [[] for _ in range(quantidade_pinos)]

    if modo == "padrao":
        pino_escolhido = int(input(f"Escolha o pino onde os discos serão inseridos (1-{quantidade_pinos}): ")) - 1
        pinos[pino_escolhido] = sorted(lista_discos, reverse=True)
    
    elif modo == "aleatorio":
        for disco in lista_discos:
            pino_aleatorio = random.randint(0, quantidade_pinos-1)
            pinos[pino_aleatorio].append(disco)
        for pino in pinos:
            pino.sort(reverse=True)

    
    while True:
        print("Configuração atual dos pinos:")
        for i, pino in enumerate(pinos):
            print(f"Pino {i+1}: {pino}")
        
        confirmacao = input("Esta configuração está correta? (sim/nao): ").lower()
        if confirmacao == "sim":
            return pinos, quantidade_pinos
        elif confirmacao == "nao" and modo == "aleatorio":
            pinos = [[] for _ in range(quantidade_pinos)] 
            for disco in lista_discos:
                pino_aleatorio = random.randint(0, quantidade_pinos-1)
                pinos[pino_aleatorio].append(disco)
            for pino in pinos:
                pino.sort(reverse=True) 
        elif confirmacao == "nao" and modo == "padrao":
            print("Reiniciando o processo.")
            return solicitar_quantidade_pinos_e_configuracao(lista_discos)

def coletar_pino_destino(quantidade_pinos):
    
    while True:
        try:
            pino_escolhido = int(input(f"Escolha o pino para onde os discos irão  (1-{quantidade_pinos}): ")) - 1
            return pino_escolhido
        except ValueError:
            print("Isso não é um número inteiro.")
            tentar_novamente = input("Deseja tentar novamente? (sim/não): ").lower()
            if tentar_novamente != "sim":
                print("Operação encerrada pelo usuário.")
                sys.exit()



#Funções para a orientação e escolhas de movimentos


def print_pinos(pinos):
    for i, pino in enumerate(pinos):
        print(f"Pino {i+1}: {pino}")
    print("-" * 20)

def encontrar_maior_disco(pinos,destino):
    maior_disco = -1
    pino_maior_disco = None
    for i, pino in enumerate(pinos):
        if i != destino and pino:  # Ignora o pino de destino
            maior_disco_no_pino = max(pino)
            if maior_disco == -1 or maior_disco_no_pino > maior_disco:
                maior_disco = maior_disco_no_pino
                pino_maior_disco = i
    return pino_maior_disco, maior_disco

def escolher_pino_auxiliar(pinos, excluidos):
    for i, pino in enumerate(pinos):
        if i not in excluidos and (not pino or (pino[-1] > pinos[excluidos[0]][-1])):
            return i
    return None

def mover_disco(pinos, origem, destino):
    if not pinos[origem]:
        return False
    if pinos[destino] and pinos[destino][-1] < pinos[origem][-1]:
        return False
    disco = pinos[origem].pop()
    pinos[destino].append(disco)
    print(f"Movendo disco {disco} de Pino {origem+1} para Pino {destino+1}")
    print_pinos(pinos)
    return True

def mover_discos(pinos, n, origem, destino, aux):
    if n == 0:
        return
    mover_discos(pinos, n - 1, origem, aux, destino)
    mover_disco(pinos, origem, destino)
    mover_discos(pinos, n - 1, aux, destino, origem)

def reorganizar_para_mover_maior_disco(pinos, destino):
    pino_maior_disco, maior_disco = encontrar_maior_disco(pinos,destino)
    if pino_maior_disco == destino or pino_maior_disco is None:
        return
    excluidos = [pino_maior_disco, destino]
    aux = escolher_pino_auxiliar(pinos, excluidos)
   
    # Caso o pino com o maior disco disponível tenha apenas um disco
    if len(pinos[pino_maior_disco]) == 1:
        if pinos[destino] and pinos[destino][-1] > maior_disco:
            # Se o disco no destino for maior que o disco a ser movido, move diretamente
            mover_disco(pinos, pino_maior_disco, destino)
        elif not pinos[destino]:
            # Se o destino estiver vazio, move o disco diretamente
            mover_disco(pinos, pino_maior_disco, destino)
    else:
        if aux is None:
            print("Não foi possível encontrar um pino auxiliar adequado.")
            return
        # Caso haja mais de um disco no pino, utiliza a lógica padrão de movimentação
        mover_discos(pinos, len(pinos[pino_maior_disco]), pino_maior_disco, destino, aux)

    mover_discos(pinos, len(pinos[pino_maior_disco]), pino_maior_disco, destino, aux)

def esvaziar_pino_destino(pinos, destino):
    """
    Tenta esvaziar o pino de destino movendo seus discos para outros pinos
    sem quebrar as regras da Torre de Hanoi.
    """
    if not pinos[destino]:
        print(f"Pino {destino+1} já está vazio.")
        return True

    while pinos[destino]:
        disco_a_mover = pinos[destino][-1]
        pino_origem = destino
        pino_auxiliar = None
        
        # Procura por um pino auxiliar válido para mover o disco.
        for pino_potencial in range(len(pinos)):
            if pino_potencial != destino and (not pinos[pino_potencial] or pinos[pino_potencial][-1] > disco_a_mover):
                pino_auxiliar = pino_potencial
                break

        if pino_auxiliar is None:
            print("Não foi possível encontrar um pino auxiliar válido para mover o disco.")
            return False
        
        # Move o disco do pino de destino para o pino auxiliar.
        if mover_disco(pinos, pino_origem, pino_auxiliar):
            print(f"Disco {disco_a_mover} movido do pino {pino_origem+1} para o pino {pino_auxiliar+1}.")
        else:
            print(f"Não foi possível mover o disco {disco_a_mover} do pino {pino_origem+1}.")
            return False

    print("Pino de destino esvaziado com sucesso.")
    return True

def esvaziar_pino(pinos, origem, destino):
    """
    Esvazia um pino específico (origem), movendo seus discos para outros pinos auxiliares,
    sem usar o pino de destino, e respeitando as regras da Torre de Hanoi.
    """
    n = len(pinos[origem])
    if n == 0:
        print(f"Pino {origem+1} já está vazio.")
        return

    # Encontra um pino auxiliar que não seja nem o de origem nem o de destino.
    auxiliares = [i for i in range(len(pinos)) if i != origem and i != destino]
    for aux in auxiliares:
        if len(pinos[aux]) == 0 or pinos[aux][-1] > pinos[origem][-1]:
            # Verifica se o movimento é válido de acordo com as regras.
            mover_disco(pinos, origem, aux)
            break
    else:
        print("Não foi possível esvaziar o pino seguindo as regras da Torre de Hanoi.")
        return

    # Se ainda houver discos no pino de origem, chama recursivamente.
    if pinos[origem]:
        esvaziar_pino(pinos, origem, destino)

def garantir_pino_auxiliar_livre(pinos, destino):
    """
    Garante que pelo menos um pino auxiliar esteja livre, excluindo o pino de destino.
    Se necessário, esvazia um pino auxiliar que não seja o de destino.
    """
    # Verifica se existe algum pino auxiliar livre, excluindo o de destino
    pino_livre = next((i for i, pino in enumerate(pinos) if not pino and i != destino), None)
    if pino_livre is not None:
        print(f"Pino {pino_livre+1} está livre.")
        return True

    # Identifica o pino com menos discos para esvaziar, excluindo o de destino
    pinos_candidatos = [i for i in range(len(pinos)) if i != destino]
    pino_para_esvaziar = min(pinos_candidatos, key=lambda x: len(pinos[x]) if pinos[x] else float('inf'))

    # Se o pino identificado já está vazio, todos os pinos auxiliares estão ocupados
    if len(pinos[pino_para_esvaziar]) == 0:
        print("Todos os pinos auxiliares estão ocupados e não é possível esvaziar o pino de destino.")
        return False

    print(f"Tentando esvaziar o Pino {pino_para_esvaziar+1} para liberar um pino auxiliar.")
    return esvaziar_pino(pinos, pino_para_esvaziar, destino)

def todas_outras_listas_vazias(pinos, destino):
    return all(len(pinos[i]) == 0 for i in range(len(pinos)) if i != destino)

def reorganizar_discos_para_destino(pinos, destino):
    # Verifica se todas as listas, exceto a destino, estão vazias
    if todas_outras_listas_vazias(pinos, destino):
        print("Todas as outras listas estão vazias. Processo concluído.")
        return

    # Move o maior disco disponível para o destino
    reorganizar_para_mover_maior_disco(pinos, destino)

    # Chamada recursiva
    reorganizar_discos_para_destino(pinos, destino)


#Função para executar a torre

def que_comece_o_jogo(pinos,destino):
    garantir_pino_auxiliar_livre(pinos,destino)
    esvaziar_pino_destino(pinos, destino)
    garantir_pino_auxiliar_livre(pinos,destino)
    reorganizar_para_mover_maior_disco(pinos, destino)
    reorganizar_para_mover_maior_disco(pinos, destino)
    esvaziar_pino_destino(pinos, destino)
    max_tentativas = 5
    tentativa_atual = 0

    while tentativa_atual < max_tentativas:
        try:
            reorganizar_discos_para_destino(pinos, destino)
            break  
        except Exception as e:
            tentativa_atual += 1  
            print(f"Tentativa {tentativa_atual} falhou. Erro: {e}")
            if tentativa_atual >= max_tentativas:
                print("maximo de tentativas ")
                break  
            else:
                
                garantir_pino_auxiliar_livre(pinos, destino)
                esvaziar_pino_destino(pinos, destino)
                garantir_pino_auxiliar_livre(pinos, destino)
                reorganizar_para_mover_maior_disco(pinos, destino)
                reorganizar_para_mover_maior_disco(pinos, destino)
                esvaziar_pino_destino(pinos, destino)







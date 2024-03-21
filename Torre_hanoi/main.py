
from funcoes_auxiliares import *






lista_discos = coletar_numero_discos()

pinos,quantidade_pinos = escolher_metodo_pinos(lista_discos)

destino = coletar_pino_destino(quantidade_pinos)

"""Para a execução do jogo, os pinos e o destino precisam estar da seguinte forma.

# pinos = [[10], [5], [10],[1,4,8],[9],[2]]
# destino = 2

É possível alterar a dinâmica diretamente nas variáveis acima."""



que_comece_o_jogo(pinos,destino)





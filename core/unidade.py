# core/unidade.py

import networkx

class Unidade:
    def __init__(self, posicao_inicial, tipo="explorador", cor=(1.0, 1.0, 0.0)):
        """
        Representa uma unidade no mapa.
        
        Args:
            posicao_inicial (tuple): posição do tile onde a unidade começa (ex: (4,5))
            tipo (str): tipo da unidade (ex: explorador, soldado)
            cor (tuple): cor usada para renderizar a unidade
        """
        self.posicao = posicao_inicial  # chave do tile atual
        self.tipo = tipo                 # tipo da unidade
        self.cor = cor                   # cor visual
        self.movimento_maximo = 5        # pontos de movimento por turno
        self.pontos_de_movimento = self.movimento_maximo

    def mover_unidade(contexto, unidade, destino):
        try:
            caminho = networkx.shortest_path(
                contexto.geografia,
                source=unidade.posicao,
                target=destino
            )
            for proximo in caminho[1:]:
                custo_movimento = contexto.geografia.edges.get((proximo, unidade.posicao), {}).get("custo", 1)
                if unidade.pontos_de_movimento >= custo_movimento:
                    unidade.posicao = proximo
                    unidade.pontos_de_movimento -= custo_movimento
                else:
                    print("Custo de movimento excedido.")
                    break
        except networkx.NetworkXNoPath:
            print("Não há caminho até esse destino.")
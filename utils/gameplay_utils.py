# utils/gameplay_utils.py
import networkx as nx

def mover_unidade(contexto, destino):
    """
    Tenta mover a unidade do contexto até o destino usando o grafo.
    
    Retorna:
        list: caminho percorrido, ou None se não houver caminho
    """
    origem = contexto.unidade_atual.posicao

    try:
        caminho = nx.shortest_path(contexto.geografia, source=origem, target=destino)
        return caminho
    except nx.NetworkXNoPath:
        print("Não há caminho entre os tiles.")
        return None
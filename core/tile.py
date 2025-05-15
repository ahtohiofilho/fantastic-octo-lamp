# core/tile.py

import glm

class Tile:
    def __init__(self, vertices, chave, bioma="oceano", cor=(1.0, 1.0, 1.0)):
        self.vertices = vertices  # Lista de glm.vec3
        self.chave = chave
        self.bioma = bioma
        self.cor = cor
        self.vertex_count = len(vertices)
        self.vertex_offset = 0  # Definido depois
        self.selected = False
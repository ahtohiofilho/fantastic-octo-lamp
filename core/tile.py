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

        # Calcular centro como média dos vértices
        if self.vertices:
            soma_x = soma_y = soma_z = 0.0
            for v in self.vertices:
                soma_x += v.x
                soma_y += v.y
                soma_z += v.z
            n = len(self.vertices)
            self.centro = glm.vec3(soma_x / n, soma_y / n, soma_z / n)
        else:
            self.centro = glm.vec3(0.0, 0.0, 0.0)
# core/contexto.py

import numpy as np
import json
import glm
from core.tile import Tile
from core.camera import CameraOrbital
from core.unidade import Unidade
from utils.shader_utils import load_shader_program, load_picking_shader_program
from utils.poligonos import dicionario_poligonos
from utils.geografia import definir_geografia

class Contexto:
    def __init__(self, fator=3):
        self.fator = fator
        self.poligonos = dicionario_poligonos(fator)
        self.geografia, self.numero_civilizacoes = definir_geografia(self.poligonos, fator)
        self.tiles = []
        self.camera = CameraOrbital()
        self.shader_program = load_shader_program()
        self.picking_shader_program = load_picking_shader_program()
        self.picking_color_loc = None  # Definido após carregar shader
        self.vao = None
        self.total_vertices = 0
        self.model = np.identity(4, dtype=np.float32)
        self.tile_selecionado = None

        self.unidade_atual = None

    def iniciar_unidade(self):
        """Cria uma unidade na primeira tile válida"""
        if self.tiles:
            posicao_inicial = self.tiles[0].chave  # ou um tile específico
            self.unidade_atual = Unidade(posicao_inicial)
            print(f"Unidade criada na tile {posicao_inicial}")

    def carregar_tiles(self):
        with open("geografia.json", "r") as f:
            data = json.load(f)

        for node in data["nodes"]:
            if "bioma" not in node or "cor_bioma" not in node:
                continue

            chave = tuple(node["id"])
            if chave not in self.poligonos:
                continue

            polygon_vertices = self.poligonos[chave]
            vertices = [glm.vec3(*v) for v in polygon_vertices]
            cor = tuple(c/255.0 for c in node["cor_bioma"])
            tile = Tile(vertices=vertices, chave=chave, bioma=node["bioma"], cor=glm.vec3(*cor))
            self.tiles.append(tile)

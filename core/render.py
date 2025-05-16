# core/render.py

import glm
from OpenGL.GL import *
import numpy as np

def configurar_buffers(contexto):
    total_vertices = []
    for tile in contexto.tiles:
        for v in tile.vertices:
            total_vertices.extend([v.x, v.y, v.z])

    vertices_np = np.array(total_vertices, dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices_np.nbytes, vertices_np, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)
    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    # Atribuir offsets para picking e desenhar
    offset = 0
    for tile in contexto.tiles:
        tile.vertex_offset = offset
        offset += tile.vertex_count

    contexto.vao = vao
    contexto.total_vertices = offset

    return vao

def renderizar_tiles(contexto):
    glUseProgram(contexto.shader_program)
    glBindVertexArray(contexto.vao)

    for tile in contexto.tiles:
        glUniform3f(contexto.color_loc, tile.cor.x, tile.cor.y, tile.cor.z)
        glDrawArrays(GL_TRIANGLE_FAN, tile.vertex_offset, tile.vertex_count)

    glBindVertexArray(0)

def renderizar_tile_selecionado(contexto):
    if any(tile.selected for tile in contexto.tiles):
        glDisable(GL_DEPTH_TEST)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        glBindVertexArray(contexto.vao)
        glUniform3f(contexto.color_loc, 1.0, 0.0, 0.0)  # Vermelho transparente

        for tile in contexto.tiles:
            if tile.selected:
                glDrawArrays(GL_TRIANGLE_FAN, tile.vertex_offset, tile.vertex_count)

        glBindVertexArray(0)

        glDisable(GL_BLEND)
        glEnable(GL_DEPTH_TEST)

def renderizar_unidade(contexto, unidade):
    tile = next((t for t in contexto.tiles if t.chave == unidade.posicao), None)
    if not tile:
        return

    glUseProgram(contexto.shader_program)
    glBindVertexArray(contexto.sprite_vao)

    # Ativa a textura
    glActiveTexture(GL_TEXTURE0)
    glBindTexture(GL_TEXTURE_2D, contexto.unidade_texture)
    glUniform1i(contexto.unit_texture_loc, 0)

    # Posiciona a unidade no centro do tile
    model = glm.translate(glm.mat4(1.0), glm.vec3(tile.centro.x, tile.centro.y, tile.centro.z + 0.1))
    model = glm.scale(model, glm.vec3(0.2))  # Ajuste o tamanho conforme necessário

    glUniformMatrix4fv(contexto.model_loc, 1, GL_FALSE, glm.value_ptr(model))

    glDrawArrays(GL_TRIANGLES, 0, 6)

    glBindTexture(GL_TEXTURE_2D, 0)
    glBindVertexArray(0)

def configurar_sprite(contexto):

    # Dados do quad
    quad_vertices = [
        -0.5, -0.5, 0.0,
         0.5, -0.5, 0.0,
         0.5,  0.5, 0.0,

        -0.5, -0.5, 0.0,
         0.5,  0.5, 0.0,
        -0.5,  0.5, 0.0,
    ]
    quad_texcoords = [
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,

        0.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
    ]

    # Gerar VAO e VBOs
    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(2)

    glBindVertexArray(vao)

    # VBO para vértices
    glBindBuffer(GL_ARRAY_BUFFER, vbo[0])
    glBufferData(GL_ARRAY_BUFFER, np.array(quad_vertices, dtype=np.float32), GL_STATIC_DRAW)
    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    # VBO para coordenadas de textura
    glBindBuffer(GL_ARRAY_BUFFER, vbo[1])
    glBufferData(GL_ARRAY_BUFFER, np.array(quad_texcoords, dtype=np.float32), GL_STATIC_DRAW)
    glVertexAttribPointer(1, 2, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(1)

    # Limpar
    glBindVertexArray(0)

    # Armazenar no contexto
    contexto.sprite_vao = vao
    contexto.sprite_vbo = vbo
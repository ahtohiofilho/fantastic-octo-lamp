# core/render.py

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
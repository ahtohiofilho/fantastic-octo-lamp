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

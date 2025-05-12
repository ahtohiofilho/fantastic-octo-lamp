# renderer.py

from OpenGL.GL import *
import numpy as np
import glm

def configurar_buffers(tiles):
    total_vertices = []
    for tile in tiles:
        for v in tile.vertices:
            total_vertices.extend([v.x, v.y, v.z])

    total_vertices = np.array(total_vertices, dtype=np.float32)

    vao = glGenVertexArrays(1)
    vbo = glGenBuffers(1)

    glBindVertexArray(vao)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, total_vertices.nbytes, total_vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    return vao, len(total_vertices) // 3

def renderizar_planeta(shader_program, tiles, camera):
    glUseProgram(shader_program)

    model = glm.mat4(1.0)
    view = camera.get_view_matrix()
    projection = camera.get_projection_matrix(800, 600)

    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    proj_loc = glGetUniformLocation(shader_program, "projection")
    color_loc = glGetUniformLocation(shader_program, "tileColor")

    glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))

    glBegin(GL_TRIANGLES)  # <-- isso ainda é antigo!
    for tile in tiles:
        glUniform3f(color_loc, tile.cor.x, tile.cor.y, tile.cor.z)
        for vertice in tile.vertices:
            glVertex3f(vertice.x, vertice.y, vertice.z)
    glEnd()

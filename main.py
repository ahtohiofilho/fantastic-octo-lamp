import glfw
from OpenGL.GL import *
import numpy as np
from shader_utils import load_shader_program
import glm

def main():
    if not glfw.init():
        raise Exception("Falha ao inicializar GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    window = glfw.create_window(mode.size.width, mode.size.height, "OpenGL Moderno com GLFW", monitor, None)

    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela GLFW")

    glfw.make_context_current(window)

    # Compilar shaders
    shader_program = load_shader_program()
    glUseProgram(shader_program)

    width_px, height_px = glfw.get_framebuffer_size(window)
    proj = glm.ortho(0.0, float(width_px), 0.0, float(height_px))

    print("Matriz de projeção:\n", proj)

    proj_loc = glGetUniformLocation(shader_program, "projection")
    if proj_loc == -1:
        print("Erro: Uniform 'projection' não encontrada no shader!")
    else:
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(proj))

    vertices = np.array([
        # Primeiro triângulo
        0, 0, 0.0,
        100, 0, 0.0,
        100, 100, 0.0,

        # Segundo triângulo
        0, 0, 0.0,
        100, 100, 0.0,
        0, 100, 0.0
    ], dtype=np.float32)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

    glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, 0, None)
    glEnableVertexAttribArray(0)

    glBindBuffer(GL_ARRAY_BUFFER, 0)
    glBindVertexArray(0)

    while not glfw.window_should_close(window):
        glClearColor(0.0, 0.0, 0.0, 1.0)
        glClear(GL_COLOR_BUFFER_BIT)

        glUseProgram(shader_program)
        glBindVertexArray(vao)
        glDrawArrays(GL_TRIANGLES, 0, 6)
        glBindVertexArray(0)

        # Verifica se a tecla ESC foi pressionada
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
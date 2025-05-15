# main.py

import glm
from glm import value_ptr
import glfw
from OpenGL.GL import *
from core.contexto import Contexto
from core.render import configurar_buffers, renderizar_tiles, renderizar_tile_selecionado
from utils.shader_utils import detect_tile_click

def main():
    # Inicializa GLFW
    if not glfw.init():
        raise Exception("Falha ao inicializar GLFW")

    # Cria janela
    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    window = glfw.create_window(mode.size.width, mode.size.height, "Planeta 3D", monitor, None)
    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela")

    glfw.make_context_current(window)

    # Cria o contexto do jogo
    contexto = Contexto()

    # Carrega os tiles com base nos dados de geografia.json
    contexto.carregar_tiles()

    # Configura VAO/VBO com todos os vértices dos tiles
    contexto.vao = configurar_buffers(contexto)

    # Ativa profundidade
    glEnable(GL_DEPTH_TEST)

    # Uniform do shader de picking
    contexto.picking_color_loc = glGetUniformLocation(
        contexto.picking_shader_program, "pickingColor"
    )

    # Uniforms do shader principal
    contexto.model_loc = glGetUniformLocation(contexto.shader_program, "model")
    contexto.view_loc = glGetUniformLocation(contexto.shader_program, "view")
    contexto.proj_loc = glGetUniformLocation(contexto.shader_program, "projection")
    contexto.color_loc = glGetUniformLocation(contexto.shader_program, "tileColor")
    tile_alpha_loc = glGetUniformLocation(contexto.shader_program, "tileAlpha")

    # Callback de mouse para picking
    def mouse_button_callback(window, button, action, mods):
        if button == glfw.MOUSE_BUTTON_LEFT and action == glfw.PRESS:
            x, y = glfw.get_cursor_pos(window)
            detect_tile_click(window, x, y, contexto)

    glfw.set_mouse_button_callback(window, mouse_button_callback)

    # Loop principal
    while not glfw.window_should_close(window):
        width, height = glfw.get_framebuffer_size(window)

        glViewport(0, 0, width, height)
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Controles de câmera
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            contexto.camera.pitch -= 1.5
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            contexto.camera.pitch += 1.5
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            contexto.camera.yaw -= 1.5
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            contexto.camera.yaw += 1.5
        if glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS:
            contexto.camera.radius -= 0.1
        if glfw.get_key(window, glfw.KEY_MINUS) == glfw.PRESS:
            contexto.camera.radius += 0.1

        contexto.camera.pitch = max(-90.0, min(90.0, contexto.camera.pitch))
        contexto.camera.update()

        # Matrizes de transformação
        model = contexto.model
        view = contexto.camera.get_view_matrix()
        projection = contexto.camera.get_projection_matrix(width, height)

        glUseProgram(contexto.shader_program)
        glUniformMatrix4fv(contexto.model_loc, 1, GL_FALSE, model)
        glUniformMatrix4fv(contexto.view_loc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(contexto.proj_loc, 1, GL_FALSE, value_ptr(projection))

        glUniform1f(tile_alpha_loc, 1.0)
        renderizar_tiles(contexto)
        glUniform1f(tile_alpha_loc, 0.75)
        renderizar_tile_selecionado(contexto)

        # Fecha com ESC
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()

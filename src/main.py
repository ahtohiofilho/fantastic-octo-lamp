import glfw
from OpenGL.GL import *
import glm
import numpy as np
import json

# Módulos personalizados
from camera import CameraOrbital
from shader_utils import load_shader_program
from polygons import dicionario_poligonos
from geography import definir_geografia

FACTOR = 3
poligonos_dict = dicionario_poligonos(FACTOR)
geografia, numero_civilizacoes = definir_geografia(poligonos_dict, FACTOR)

class Tile:
    def __init__(self, vertices, chave, bioma="oceano", cor=(1.0, 1.0, 1.0)):
        self.vertices = [glm.vec3(*v) for v in vertices]
        self.chave = chave
        self.bioma = bioma
        self.cor = cor
        self.vertex_count = len(vertices)

tiles = []

def carregar_tiles():
    """Carrega os tiles com base nos dados do geografia.json"""
    with open("geografia.json", "r") as f:
        data = json.load(f)

    for node in data["nodes"]:
        if "bioma" not in node or "cor_bioma" not in node:
            continue

        bioma = node["bioma"]
        cor = tuple(node["cor_bioma"])
        node_id = node["id"]
        x, y = node_id[0], node_id[1]
        chave = (x, y)

        if chave not in poligonos_dict:
            print(f"Chave {chave} não encontrada em poligonos_dict")
            continue

        polygon_vertices = poligonos_dict[chave]

        coords = [glm.vec3(*v) for v in polygon_vertices]
        tile_cor = glm.vec3(cor[0]/255.0, cor[1]/255.0, cor[2]/255.0)

        tiles.append(Tile(coords, chave=chave, bioma=bioma, cor=tile_cor))

    return tiles

def configurar_buffers_com_todos_vertices(tiles):
    """Configura um único VAO/VBO com todos os vértices dos tiles"""
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

    offset_atual = 0
    for tile in tiles:
        tile.vertex_offset = offset_atual
        offset_atual += tile.vertex_count

    return vao, offset_atual

def main():
    if not glfw.init():
        raise Exception("Falha ao inicializar GLFW")

    glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 3)
    glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 3)
    glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)

    monitor = glfw.get_primary_monitor()
    mode = glfw.get_video_mode(monitor)
    window = glfw.create_window(mode.size.width, mode.size.height, "Planeta 3D", monitor, None)

    if not window:
        glfw.terminate()
        raise Exception("Falha ao criar janela GLFW")

    glfw.make_context_current(window)
    carregar_tiles()  # Carrega os dados dos tiles

    vao, total_vertices = configurar_buffers_com_todos_vertices(tiles)
    glEnable(GL_DEPTH_TEST)

    # Compilar shaders
    shader_program = load_shader_program()
    glUseProgram(shader_program)

    width_px, height_px = glfw.get_framebuffer_size(window)

    # Configurar câmera orbital
    camera = CameraOrbital(center=(0, 0, 0), radius=10.0, pitch=20.0, yaw=0.0)
    view = camera.get_view_matrix()
    projection = camera.get_projection_matrix(width_px, height_px)

    # Locais dos uniforms
    model_loc = glGetUniformLocation(shader_program, "model")
    view_loc = glGetUniformLocation(shader_program, "view")
    proj_loc = glGetUniformLocation(shader_program, "projection")
    color_loc = glGetUniformLocation(shader_program, "tileColor")
    if color_loc == -1:
        print("Erro: Uniform 'tileColor' NÃO ENCONTRADA no shader!")

    # Loop principal
    while not glfw.window_should_close(window):
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        # Controles da câmera
        if glfw.get_key(window, glfw.KEY_UP) == glfw.PRESS:
            camera.pitch -= 1.5
        if glfw.get_key(window, glfw.KEY_DOWN) == glfw.PRESS:
            camera.pitch += 1.5
        if glfw.get_key(window, glfw.KEY_LEFT) == glfw.PRESS:
            camera.yaw -= 1.5
        if glfw.get_key(window, glfw.KEY_RIGHT) == glfw.PRESS:
            camera.yaw += 1.5
        if glfw.get_key(window, glfw.KEY_EQUAL) == glfw.PRESS:
            camera.radius -= 0.1
        if glfw.get_key(window, glfw.KEY_MINUS) == glfw.PRESS:
            camera.radius += 0.1

        camera.pitch = max(-90.0, min(90.0, camera.pitch))

        camera.update()

        glUseProgram(shader_program)

        model = glm.mat4(1.0)
        view = camera.get_view_matrix()
        projection = camera.get_projection_matrix(width_px, height_px)

        glUniformMatrix4fv(model_loc, 1, GL_FALSE, glm.value_ptr(model))
        glUniformMatrix4fv(view_loc, 1, GL_FALSE, glm.value_ptr(view))
        glUniformMatrix4fv(proj_loc, 1, GL_FALSE, glm.value_ptr(projection))

        # Renderiza cada tile com sua cor específica
        for tile in tiles:
            glUniform3f(color_loc, tile.cor.x, tile.cor.y, tile.cor.z)
            glBindVertexArray(vao)
            glDrawArrays(GL_TRIANGLE_FAN, tile.vertex_offset, tile.vertex_count)
            glBindVertexArray(0)

        # Verifica se ESC foi pressionado
        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            glfw.set_window_should_close(window, True)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()

if __name__ == "__main__":
    main()
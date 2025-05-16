# utils/shader_utils.py

from PIL import Image
import numpy as np
import glm
from OpenGL.GL import *
import os
import glfw

def detect_tile_click(window, x, y, contexto):
    width_px, height_px = glfw.get_framebuffer_size(window)
    camera = contexto.camera
    camera.update()

    # Desativa iluminação e usa apenas o shader de picking
    glUseProgram(contexto.picking_shader_program)

    glClearColor(0.0, 0.0, 0.0, 1.0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    # Aplica as matrizes atualizadas
    model = glm.mat4(1.0)
    view = camera.get_view_matrix()
    projection = camera.get_projection_matrix(width_px, height_px)

    model_loc_pick = glGetUniformLocation(contexto.picking_shader_program, "model")
    view_loc_pick = glGetUniformLocation(contexto.picking_shader_program, "view")
    proj_loc_pick = glGetUniformLocation(contexto.picking_shader_program, "projection")

    glUniformMatrix4fv(model_loc_pick, 1, GL_FALSE, glm.value_ptr(model))
    glUniformMatrix4fv(view_loc_pick, 1, GL_FALSE, glm.value_ptr(view))
    glUniformMatrix4fv(proj_loc_pick, 1, GL_FALSE, glm.value_ptr(projection))

    for i, tile in enumerate(contexto.tiles):
        r = ((i + 1) >> 16) & 0xFF
        g = ((i + 1) >> 8) & 0xFF
        b = (i + 1) & 0xFF
        glUniform3f(contexto.picking_color_loc, r / 255.0, g / 255.0, b / 255.0)
        glBindVertexArray(contexto.vao)
        glDrawArrays(GL_TRIANGLE_FAN, tile.vertex_offset, tile.vertex_count)
        glBindVertexArray(0)

    pixel = glReadPixels(x, height_px - y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE)
    r, g, b = pixel[0], pixel[1], pixel[2]
    clicked_id = r << 16 | g << 8 | b  # Converte RGB para ID

    # Se for preto, considera como clique fora do planeta
    if r == 0 and g == 0 and b == 0:
        for t in contexto.tiles:
            t.selected = False
        return

    if 0 < clicked_id <= len(contexto.tiles):
        selected_tile = contexto.tiles[clicked_id - 1]
        for t in contexto.tiles:
            t.selected = False
        selected_tile.selected = True
    else:
        for t in contexto.tiles:
            t.selected = False
    print(f"Clicou no tile {selected_tile.chave} - Bioma: {selected_tile.bioma}")

def read_shader_file(filename):
    with open(filename, 'r') as f:
        return f.read()

def load_shader_program():
    vertex_shader_path = os.path.join("shaders", "vertex.glsl")
    fragment_shader_path = os.path.join("shaders", "fragment.glsl")

    vertex_src = read_shader_file(vertex_shader_path)
    fragment_src = read_shader_file(fragment_shader_path)

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_src)
    glCompileShader(vertex_shader)
    check_compile_errors(vertex_shader, "vertex")

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_src)
    glCompileShader(fragment_shader)
    check_compile_errors(fragment_shader, "fragment")

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    check_compile_errors(shader_program, "program")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program

def check_compile_errors(shader, shader_type):
    if shader_type != "program":
        success = glGetShaderiv(shader, GL_COMPILE_STATUS)
        info_log_length = glGetShaderiv(shader, GL_INFO_LOG_LENGTH)
        if info_log_length > 1:
            info_log = glGetShaderInfoLog(shader)
            print(f"Erro compilando {shader_type} shader:\n{info_log.decode()}")
        else:
            info_log = ""
    else:
        success = glGetProgramiv(shader, GL_LINK_STATUS)
        info_log_length = glGetProgramiv(shader, GL_INFO_LOG_LENGTH)
        if info_log_length > 1:
            info_log = glGetProgramInfoLog(shader, info_log_length)
            print(f"Erro linkando {shader_type}:\n{info_log.decode()}")
        else:
            info_log = ""

    if not success:
        raise RuntimeError(f"Erro no shader {shader_type}")

def load_picking_shader_program():
    vertex_shader_path = os.path.join("shaders", "picking_vertex.glsl")
    fragment_shader_path = os.path.join("shaders", "picking_fragment.glsl")

    vertex_src = read_shader_file(vertex_shader_path)
    fragment_src = read_shader_file(fragment_shader_path)

    vertex_shader = glCreateShader(GL_VERTEX_SHADER)
    glShaderSource(vertex_shader, vertex_src)
    glCompileShader(vertex_shader)
    check_compile_errors(vertex_shader, "vertex")

    fragment_shader = glCreateShader(GL_FRAGMENT_SHADER)
    glShaderSource(fragment_shader, fragment_src)
    glCompileShader(fragment_shader)
    check_compile_errors(fragment_shader, "fragment")

    shader_program = glCreateProgram()
    glAttachShader(shader_program, vertex_shader)
    glAttachShader(shader_program, fragment_shader)
    glLinkProgram(shader_program)
    check_compile_errors(shader_program, "program")

    glDeleteShader(vertex_shader)
    glDeleteShader(fragment_shader)

    return shader_program

def carregar_textura(arquivo):
    img = Image.open(arquivo).convert("RGBA")
    img = img.transpose(Image.FLIP_TOP_BOTTOM)
    img_data = np.array(img.getdata(), np.uint8)

    texture_id = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture_id)

    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, img.width, img.height,
                  0, GL_RGBA, GL_UNSIGNED_BYTE, img_data)

    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    glBindTexture(GL_TEXTURE_2D, 0)

    return texture_id

from OpenGL.GL import *
import os
import numpy as np

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
        info_log = glGetShaderInfoLog(shader)
    else:
        success = glGetProgramiv(shader, GL_LINK_STATUS)
        info_log = glGetProgramInfoLog(shader)

    if not success:
        print(f"Erro compilando {shader_type} shader:\n{info_log.decode()}")
        raise RuntimeError(f"Erro no shader {shader_type}")

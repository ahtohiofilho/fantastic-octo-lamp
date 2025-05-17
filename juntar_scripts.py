import os

# Lista de arquivos específicos
arquivos = [
    "README.md",
    "main.py",
    "core/camera.py",
    "core/contexto.py",
    "core/render.py",
    "core/tile.py",
    "core/unidade.py",
    "shaders/fragment.glsl"
    "shaders/vertex.glsl",
    "shaders/picking_fragment.glsl",
    "shaders/picking_vertex.glsl",
    "utils/geografia.py",
    "utils/poligonos.py",
    "utils/shader_utils.py"
]

# Arquivo de saída
arquivo_saida = "scripts_selecionados.txt"

with open(arquivo_saida, "w") as destino:
    for arquivo in arquivos:
        with open(arquivo, "r") as origem:
            destino.write(f"\n# Conteúdo de {arquivo}\n")
            destino.write(origem.read())

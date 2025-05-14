#version 330 core
out vec4 color;
uniform vec3 pickingColor; // Cor única por tile
void main() {
    color = vec4(pickingColor, 1.0); // RGBA único para identificação
}
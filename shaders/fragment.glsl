#version 330 core
out vec4 color;

uniform vec3 tileColor;

void main() {
    color = vec4(tileColor, 1.0);
}

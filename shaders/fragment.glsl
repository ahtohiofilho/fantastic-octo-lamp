#version 330 core
out vec4 color;

uniform vec3 tileColor;
uniform float tileAlpha;

void main() {
    color = vec4(tileColor, tileAlpha);
}

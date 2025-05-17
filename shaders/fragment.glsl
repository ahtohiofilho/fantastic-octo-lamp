#version 330 core
out vec4 outColor;

in vec2 fragTexCoord; // Coordenadas de textura

uniform vec3 tileColor;
uniform float tileAlpha;

uniform sampler2D unitTexture; // Textura da unidade
uniform bool useTexture;       // Controla se usamos textura ou cor sólida

void main() {
    if (useTexture) {
        // Usa a textura (sprite da unidade)
        vec4 texColor = texture(unitTexture, fragTexCoord);
        outColor = texColor;
    } else {
        // Usa cor sólida (para os tiles)
        outColor = vec4(tileColor, tileAlpha);
    }
}
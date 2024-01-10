#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 fragPos;

uniform sampler2D u_texture_0;
uniform vec2 gsf;




void main() {
    vec2 scaledUV = uv_0 * gsf;
    vec2 offset = (gsf - 1.0) / 2.0;
    vec3 color = texture(u_texture_0, scaledUV - offset).rgb;
    fragColor = vec4(color, 1.0);
}










#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 fragPos;

uniform sampler2D u_texture_0;
uniform vec2 gsf;




void main() {
    vec3 color = texture(u_texture_0, uv_0).rgb;
    fragColor = vec4(color, 1.0);
}











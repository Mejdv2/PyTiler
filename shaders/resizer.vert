#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_position;

out vec2 uv_0;
out vec3 fragPos;


void main() {
    uv_0 = in_texcoord_0;
    gl_Position = vec4(in_position.xy, 1.0, 1.0);
}
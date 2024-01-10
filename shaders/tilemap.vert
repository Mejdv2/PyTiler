#version 330 core

layout (location = 0) in vec2 in_texcoord_0;
layout (location = 1) in vec3 in_position;
layout (location = 2) in vec3 position;

out vec2 uv_0;
out vec3 fragPos;
out vec3 instance_pos_data;

uniform mat4 m_proj;
uniform mat4 m_view;
uniform mat4 m_model;


void main() {
    uv_0 = in_texcoord_0;
    vec3 vert_position = in_position + vec3(position.xy*2, 0);
    instance_pos_data = position;

    fragPos = vec3(m_model * vec4(vert_position, 1.0));
    gl_Position = m_proj * m_view * m_model * vec4(vert_position, 1.0);
}
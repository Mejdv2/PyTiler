#version 330 core

layout (location = 0) out vec4 fragColor;

in vec2 uv_0;
in vec3 fragPos;

uniform sampler2DArray u_texture_0;
uniform int frame;
uniform vec3 camPos;




void main() {
    vec3 color = texture(u_texture_0, vec3(uv_0.xy, frame)).rgb;

    if (color == vec3(0, 0, 0)) {
        discard;
    }

    fragColor = vec4(color, 1);
}











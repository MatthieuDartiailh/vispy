# !/usr/bin/env python
# -*- coding: utf-8 -*-
# vispy: gallery 3

"""
Example demonstrating showing a quad. Like hello_quad1.py, but now
with Texture2D and VertexBuffer, and optionally using an ElementBuffer to
draw the vertices.
"""

import time
import numpy as np

from vispy import gloo
from vispy import app


# Create a texture
im1 = np.zeros((100, 100, 3), 'float32')
im1[:50, :, 0] = 1.0
im1[:, :50, 1] = 1.0
im1[50:, 50:, 2] = 1.0

# Create vetices and texture coords, combined in one array for high performance
vertex_data = np.zeros(4, dtype=[('a_position', np.float32, 3),
                                 ('a_texcoord', np.float32, 2)])
vertex_data['a_position'] = np.array([[-0.8, -0.8, 0.0], [+0.7, -0.7, 0.0],
                                      [-0.7, +0.7, 0.0], [+0.8, +0.8, 0.0, ]])
vertex_data['a_texcoord'] = np.array([[0.0, 0.0], [0.0, 1.0],
                                      [1.0, 0.0], [1.0, 1.0]])

# Create indices and an ElementBuffer for it
indices = np.array([0, 1, 2, 1, 2, 3], np.uint16)
indices_buffer = gloo.IndexBuffer(indices)
client_indices_buffer = gloo.IndexBuffer(indices, client=True)


VERT_SHADER = """ // simple vertex shader

attribute vec3 a_position;
attribute vec2 a_texcoord;
uniform float sizeFactor;
//attribute float sizeFactor;

void main (void) {
    // Pass tex coords
    gl_TexCoord[0] = vec4(a_texcoord.x, a_texcoord.y, 0.0, 0.0);
    // Calculate position
    gl_Position = sizeFactor*vec4(a_position.x, a_position.y, a_position.z,
                                                        1.0/sizeFactor);
}
"""

FRAG_SHADER = """ // simple fragment shader
uniform sampler2D texture1;

void main()
{
    gl_FragColor = texture2D(texture1, gl_TexCoord[0].st);
}

"""


class Canvas(app.Canvas):

    def __init__(self):
        app.Canvas.__init__(self, close_keys='escape')

        # Create program
        self._program = gloo.Program(VERT_SHADER, FRAG_SHADER)

        # Create vertex buffer
        self._vbo = gloo.VertexBuffer(vertex_data)

        # Set uniforms, samplers, attributes
        # We create one VBO with all vertex data (array of structures)
        # and create two views from it for the attributes.
        self._program['texture1'] = gloo.Texture2D(im1)
        self._program.bind(self._vbo)  # This does:
        #self._program['a_position'] = self._vbo['a_position']
        #self._program['a_texcoords'] = self._vbo['a_texcoords']

    def on_initialize(self, event):
        gloo.set_clear_color((1, 1, 1, 1))

    def on_resize(self, event):
        width, height = event.size
        gloo.set_viewport(0, 0, width, height)

    def on_draw(self, event):

        # Clear
        gloo.clear()

        # Draw
        self._program['sizeFactor'] = 0.5 + np.sin(time.time() * 3) * 0.2

        # Draw (pick one!)
        # self._program.draw(gl.GL_TRIANGLE_STRIP)
        self._program.draw('triangles', indices_buffer)
        # self._program.draw(gl.GL_TRIANGLES, client_indices_buffer)  # Not
        # recommended

        self.update()


if __name__ == '__main__':
    c = Canvas()
    c.show()
    app.run()

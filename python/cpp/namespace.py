import os, sys

def namespace(current, name):
    cursor = current.window.cursor[0]
    buffer = current.buffer
    buffer.append("} // namespace " + name, cursor)
    buffer.append("{", cursor)
    buffer.append("namespace " + name, cursor)


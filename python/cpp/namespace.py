import os, sys

def namespace(current, name):
    cursor = current.window.cursor[0]
    buffer = current.buffer
    buffer.append("} // namespace " + name, cursor)
    buffer.append("", cursor)
    buffer.append("{", cursor)
    buffer.append("namespace " + name, cursor)
    current.window.cursor = (cursor + 3, current.window.cursor[1])


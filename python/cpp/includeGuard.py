import os, sys

# This function adds or modifies the include guard of the given file.
# If the file has an existing include guard, it must be aligned to the left and
# the #ifndef, #define routines must occur in consecutive lines.
# If the file does not have an existing include guard, it must not have any
# CPP routines that look like an include guard. The function currently is
# unable to distinguish comments from code, so it is important that no comment
# blocks start or end in the include guard.
#
# Args:
# buffer[io]: The contents of the file. Can either be a line-by-line list or a
#   vim buffer.
# rPath[i]: The relative path of the file to the base
# format[i]: The format of the include guard. Replacement rules:
#   {DIR} -> upper case directory name, separated by underscores
#   {Dir} -> directory name, separated by underscores
#   {dir} -> lower case directory name, separated by underscores
#   {FNAME}, {FName}, {fname} -> upper, none, lower case file names. The file
#       names must not contain dots.
#   {EXT}, {Ext}, {ext} -> upper, none, lower case file extensions.
def format(buffer, rPath, format):
    rPath, ext = os.path.splitext(rPath)
    directory, fileName = os.path.split(rPath)

    if len(ext) != 0:
        ext = ext[1:]

    directory = directory.replace(r"/", "_")

    format = format.replace('{DIR}', directory.upper())
    format = format.replace('{Dir}', directory)
    format = format.replace('{dir}', directory.lower())

    format = format.replace('{FNAME}', fileName.upper())
    format = format.replace('{FName}', fileName)
    format = format.replace('{fname}', fileName.lower())

    format = format.replace('{EXT}', ext.upper())
    format = format.replace('{Ext}', ext)
    format = format.replace('{ext}', ext.lower())

    iguard_begin = -1
    iguard_end = -1

    for i in range(len(buffer) - 1):
        if (buffer[i].startswith("#ifndef") and
            buffer[i + 1].startswith("#define")):
            iguard_begin = i
            break
    if iguard_begin != -1:
        for i in range(len(buffer) - 1, 1, -1):
            if buffer[i].startswith("#endif"):
                iguard_end = i
                break

    if iguard_end == -1: # Create new guard

        if isinstance(buffer, list): # Ordinary file
            # These needs to be reversed
            buffer.insert(0, "#define " + format + "\n")
            buffer.insert(0, "#ifndef " + format + "\n")
            buffer.append("#endif // !" + format + "\n")
        else: # Operating on a vim buffer
            buffer.append("#define " + format + "\n", 0)
            buffer.append("#ifndef " + format + "\n", 0)
            buffer.append("#endif // !" + format + "\n")
    
    else: # Change existing guards
        buffer[iguard_begin] = "#ifndef " + format + "\n"
        buffer[iguard_begin + 1] = "#define " + format + "\n"
        buffer[iguard_end] = "#endif // !" + format + "\n"



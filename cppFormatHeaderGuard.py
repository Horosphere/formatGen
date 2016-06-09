import os, sys

import python.cpp.includeGuard

# Find .formatGen configuration
baseDir = os.getcwd()
systemRoot = os.path.abspath(os.sep)
format = None
while baseDir != systemRoot:
    if os.path.isfile(baseDir + "/.formatGen"):
        with open(baseDir + "/.formatGen") as f:
            format = f.readline().strip()
            baseDir += "/" + f.readline().strip()
            break
    baseDir = os.path.dirname(baseDir)

if format == None:
    print(".formatGen format file not found")
    sys.exit(0)

os.chdir(baseDir)

if len(sys.argv) > 1: # User specified a list of files
    for fileName in sys.argv[1:]:
        with open(fileName, "r+") as file:
            lines = file.readlines()
            python.cpp.includeGuard.format(lines, os.path.relpath(sys.argv[1], baseDir),
                    format)
            file.seek(0)
            file.writelines(lines)
else: # Scan the directory recursively to find every header
    print("Recursively scanning working directory for headers")
    for root, subdirs, files in os.walk("./"):
        for fileName in files:
            f = os.path.join(root, fileName)[len("./"):]
            if f.endswith(('h', '.hh', '.hpp', '.hxx')):
                print("Found header: " + f)
                with open(f, "r+") as file:
                    lines = file.readlines()
                    python.cpp.includeGuard.format(lines, os.path.relpath(f, baseDir),
                            format)
                    file.seek(0)
                    file.writelines(lines)



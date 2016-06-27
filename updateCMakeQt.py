# Author: Horosphere
# The purpose of this script is to automatically update CMakeLists.txt when a
# new source file is introduced, or an old source file is removed.
# Execute this script each time you add a new source file in src/ to
# update CMakeLists.txt, or each time you add a new QObject header file.

# Configuration:

# All headers from this directory are fed into the Qt MOC
dir_qObject = "src/ui"
# The directory containing the source files.
dir_source = "src"
fileName = "CMakeLists.txt" # You do not have to change this most of the time.

# The following signatures must be present in CMakeLists.txt
signature_begin = "# Auto-generated. Do not edit. All changes will be undone\n"
signature_end = "# Auto-generated end\n"

# ${SourceFiles} should be added as a dependency for the project
# ${QObjectHeaders} can be fed into the MOC to produce the MOC source files.
autoGen_source_begin = "set(SourceFiles\n"
autoGen_source_end = "   )\n"
autoGen_qObject_begin = "set(QObjectHeaders\n"
autoGen_qObject_end = "   )\n"
autoGen_padding = "    "

import os, sys

#os.chdir(os.path.dirname(os.path.realpath(__file__)));
cMakeFile = [] # Lines of CMakeLists.txt
iBegin = -1 # Indices corresponding to auto-generated sections
iEnd = -1
with open(fileName, "r") as file:
    index = 0
    for line in file:
        cMakeFile.append(line)
        if line == signature_begin:
            iBegin = index
        elif line == signature_end:
            iEnd = index
        index += 1

if iBegin == -1 or iEnd == -1 or iBegin > iEnd:
    print("No auto-generated region found in " + fileName + ".")
    print("Please check that the following lines exist:")
    print(signature_begin[:-1])
    print(signature_end[:-1])
    sys.exit(1)

del cMakeFile[iBegin + 1: iEnd]

print("Source files:")
autoGen = autoGen_source_begin
truncation = len("./" + dir_source)
# Scans source directory recursively to gather source files
for root, subdirs, files in os.walk("./" + dir_source):
    for name in files:
        f = str(os.path.join(root, name))[truncation:]
        if not f.endswith(('.cpp', '.c', '.cxx', '.cc')): continue
        print(f)
        autoGen += autoGen_padding + dir_source + f + "\n"
autoGen += autoGen_source_end + autoGen_qObject_begin

print("\nQObject files:")
truncation = len("./" + dir_qObject)
# Scans QObject  directory recursively to gather QObject files
for root, subdirs, files in os.walk("./" + dir_qObject):
    for name in files:
        f = str(os.path.join(root, name))[truncation:]
        if not f.endswith(('.hpp', '.h', '.hxx', '.hh')): continue
        print(f)
        autoGen += autoGen_padding + dir_qObject + f + "\n"
autoGen += autoGen_qObject_end

cMakeFile.insert(iBegin + 1, autoGen)

with open(fileName, "w") as file:
    for line in cMakeFile:
        file.write(line)



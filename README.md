# formatGen
C++ Code auto-gen utility. Currently can be used to generate include guards.

## Installation

You can use any vim plugin manager ([Pathogen](
https://github.com/tpope/vim-pathogen),
[Vundle](https://github.com/VundleVim/Vundle.vim), etc.) to manage formatGen.

## Usage

To use formatGen on any C++ project, create a file named `.formatGen` in a
parent directory of all source files. The `.formatGen` file should contain the
following:
```
<format>
<src-folder>
```
The first line `<format>` is the style of the include guards. The following
tokens will be replaced:

1. `{DIR}, {Dir}, {dir}` -> upper, normal, lower case directory name, separated
by underscores
2. `{FNAME}, {FName}, {fname}` -> upper, normal, lower case file name. The file
names must not contain dots.
3. `{EXT}, {Ext}, {ext}` -> file extension.

The second line is the common parent directory to all headers. For example, if
your project is structured like this:
```
.formatGen
LICENSE
README.md
--/src <- Here lies all of your headers
--...
--/bin
--...
```
Then `<src-folder>` should be `src`, with no slashes.

Example:
```
_CPPTEST_{DIR}_{FName}_{ext}__
src
```
When formatGen is applied to the file `src/core/Server.hpp`, it generates the
following include guard:
```
#ifndef _CPPTEST_CORE_Server_hpp__
#define _CPPTEST_CORE_Server_hpp__

#endif // !_CPPTEST_CORE_Server_hpp__
```

### Include guard generation

Executing the script `cppFormatHeaderGuard.py` formats either all headers or a
list of headers specified in the argument. The present working directory must
be a daughter directory of where `.formatGen` resides.
You can also run this script within Vim using `:FGIncludeGuard <path>`, where
`<path>` is the path to your file. It is needed since there is no way to query
the file path using Vim.

### Rules

formatGen automatically detects existing include guards. If none exists, it
will create its own. The include guard must qualify the following conditions to
be detected correctly.

1. Include guards do not have preceding white spaces.
2. `#define` and `#ifndef` must be on adjacent lines.
3. If there are preprocessor commands that look like an include guard, they
will be identified as an include guard and problems can occur. This will be
fixed in the future.

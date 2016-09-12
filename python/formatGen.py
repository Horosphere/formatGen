import os, sys, vim 

import cpp.includeGuard
import cpp.namespace

def cppFormatIncludeGuard(rPath):
    baseDir = os.getcwd()
    systemRoot = os.path.abspath(os.sep)
    format = None
    while baseDir != systemRoot:
        if os.path.isfile(baseDir + "/.formatGen"):
            with open(baseDir + "/.formatGen") as f:
                format = f.readline().strip()
                break
        baseDir = os.path.dirname(baseDir)
    if format == None:
        vim.command("echoerr \"Unable to find .formatGen file\"")
        return
    cpp.includeGuard.format(vim.current.buffer, rPath, format)

def cppNamespace(name):
    cpp.namespace.namespace(vim.current, name)

def init(commandPy):
    vim.command('function! s:FGIncludeGuard(rPath)\n' +
                commandPy + ' cppFormatIncludeGuard(rPath)\n' +
                'endfunction')
    vim.command('command! -nargs=1 FGInclueGuard call s:FGInclueGuard(<f-args>)')
    vim.command('function! s:FGNamespace(name)\n' +
                commandPy + ' cppNamespace(name)\n' +
                'endfunction')
    vim.command('command! -nargs=1 FGNamespace call s:FGNamespace(<f-args>)')

" Main entry of formatGen.vim plugin

" Required by all vim plugins
" Forces nocompatible
let s:save_cpo = &cpo
set cpo&vim

function! s:restore_cpo()
	let &cpo = s:save_cpo
	unlet s:save_cpo
endfunction

" Plugin loading area

" Check version requirements
if v:version < 703
	echoerr "formatGen requires Vim version 7.3 or above"
	call s:restore_cpo()
	finish
" Requires python
elseif !has('python') && !has('python3')
	echoerr "formatGen requires Vim compiled with Python 3 support"
	call s:restore_cpo()
	finish
" Check if loaded
elseif exists("g:formatGen_loadFlag")
	call s:restore_cpo()
	finish
endif

let g:formatGen_loadFlag=1

" Options
" This is per project setting
"let g:formatGen_includeGuard =
"	\get(g:, 'formatGen_includeGuard', "_{FILENAME}_{EXT}_")

" Initialise all scripts

let s:pythonVer = has('python') " 1 for python, 0 for python3
let s:python = s:pythonVer ? "python" : "python3"

let s:pluginRoot = escape(expand('<sfile>:p:h:h'),'\')

" Python manages this part
exec s:python." << EOF"

import sys, os, vim
pluginRoot = vim.eval('s:pluginRoot')
sys.path.insert(0, os.path.join(pluginRoot, 'python'))
import formatGen
formatGen.init(vim.eval('s:python'))
vim.command("command! -nargs=1 -complete=file FGInclueGuard " + vim.eval('s:python') + " formatGen.cppFormatIncludeGuard(<f-args>)")
vim.command("command! -nargs=1 FGNamespace " + vim.eval('s:python') + " formatGen.cppNamespace(<f-args>)")

EOF


" Cleanup
call s:restore_cpo()

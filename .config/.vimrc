call plug#begin('~/.vim/plugged')

Plug 'itchyny/lightline.vim'
Plug 'ctrlpvim/ctrlp.vim'
Plug 'HenryNewcomer/vim-theme-papaya'
Plug 'wojciechkepka/vim-github-dark'

call plug#end()

"Enable Plugins
"----------------
set laststatus=2

"Look and feel
"----------------
set termguicolors
syntax on
colo ghdark
set relativenumber
let g:lightline = { 'colorscheme': 'one' }
" ctrlp plugin
let g:ctrlp_map = '<c-p>'
let g:ctrlp_cmd='CtrlP :pwd'
let g:ctrlp_custom_ignore = '\v[\/]\.(git|gitignore)$'

syntax enable

" improved searching
"----------------
set incsearch
set nohlsearch

"KeyMaps
"----------------
" unmap arrow keys
nnoremap <up> <nop>
nnoremap <down> <nop>
nnoremap <right> <nop>
nnoremap <left> <nop>
" toggle search show results
nnoremap <c-h> :set hlsearch!<cr>
" easy buffer navigation
nnoremap <TAB> :bn<CR>
let mapleader = ","

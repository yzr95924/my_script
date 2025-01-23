local global = vim.g -- for vim global variables
local o = vim.opt -- for vim options

-- common options
o.clipboard = "unnamedplus" -- use system clipboard
o.completeopt = { "menu", "menuone", "noselect" }
-- 补全菜单将始终显示，无论有多少个候选项。
-- 用户可以看到所有可用的补全项，并进行选择。
-- 用户需要手动选择候选项，而不是自动选择第一个选项，从而提供更好的控制。
o.mouse = 'a' -- allow the mouse to be used in Nvim
o.syntax = 'on' -- setup syntax

-- Tab
o.tabstop = 4 -- number of visual spaces per TAB
o.softtabstop = 4 -- number of spaces in tab when editing
o.shiftwidth = 4 -- insert 4 spaces on a tab
o.expandtab = true

-- Searching
o.incsearch = true -- search as characters are entered
o.hlsearch = true -- hightlight matches
o.ignorecase = true -- ignore case in searches by default
o.smartcase = true -- but make it case sensitive if an uppercase is entered

-- line
o.number = true -- show line number
o.cursorline = true -- highlight the line of current cursor

-- windows
o.title = true
o.ruler = true
o.termguicolors = true -- optionally enable 24-bit colour
o.showcmd = true

-- encoding
o.encoding = "UTF-8"

-- global setting
-- disable netrw at the very start of your init.lua (for nvim-tree)
global.loaded_netrw = 1
global.loaded_netrwPlugin = 1
global.mapleader = " " -- use "space" as the leader key
global.maplocalleader = "\\"
-- vim config
local set_o = vim.o
local set_g = vim.g
local opt = vim.opt
local cmd = vim.cmd

set_o.number = true
set_o.autoread = true
set_o.encoding = "utf8"

-- Hint: use `:h <option>` to figure out the meaning if needed
-- vim.opt.clipboard = 'unnamedplus' -- use system clipboard, need x11 forwading
opt.completeopt = { 'menu', 'menuone', 'noselect' }
opt.mouse = 'a' -- allow the mouse to be used in Nvim
opt.swapfile = false -- don't use swapfiles

-- Tab
opt.tabstop = 4 -- number of visual spaces per TAB
opt.softtabstop = 4 -- number of spacesin tab when editing
opt.shiftwidth = 4 -- insert 4 spaces on a tab
opt.expandtab = true -- tabs are spaces, mainly because of python

-- Searching
opt.incsearch = true -- search as characters are entered
opt.hlsearch = true -- do not highlight matches
opt.ignorecase = true -- ignore case in searches by default
opt.smartcase = true -- but make it case sensitive if an uppercase is entere

set_g.hardtime_default_on = 1
set_g.hardtime_maxcount = 2
set_g.hardtime_timeout = 700

-- cmd config
-- cmd.colorscheme("base16-tango")

-- disable netrw at the very start of your init.lua
set_g.loaded_netrw = 1
set_g.loaded_netrwPlugin = 1

-- set termguicolors to enable highlight groups
set_g.opt.termguicolors = true
-- vim config
local set = vim.o
local opt = vim.opt
local cmd = vim.cmd

set.number = true
set.autoread = true
set.encoding = "utf8"

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

vim.g.hardtime_default_on = 1
vim.g.hardtime_maxcount = 2
vim.g.hardtime_timeout = 700

-- cmd config
-- cmd.colorscheme("base16-tango")
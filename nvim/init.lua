-- if use "vimrc", then:
-- vim.cmd("source ~/.config/nvim/.vimrc")
-- if vim.g.neovide then
-- 	-- Put anything you want to happen only in Neovide here
-- 	vim.o.guifont = "FiraCode Nerd Font Mono:h15"
-- end

-- set.clipboard = "unnamed" -- required X11 forwarding
local safeRequire = require("config.my_lib").safeRequire -- using myself safeRequire

safeRequire("config.options")
safeRequire("init_lazynvim")
require("which-key").setup {}

local wk = require("which-key")
-- define key mapping
local keys = {
    {'<leader>fg', "<cmd>Telescope live_grep<cr>", desc = "Telescope Live grep"},
    {'<leader>ff', "<cmd>Telescope find_files<cr>" desc = "Telescope Find file"},
}

-- register the key mapping
wk.add(keys)
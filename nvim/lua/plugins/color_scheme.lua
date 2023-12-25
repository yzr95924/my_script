return {
	-- {
	-- 	"RRethy/nvim-base16",
	-- 	lazy = false,
    --     config = function()
    --         vim.cmd([[colorscheme base16-tender]])
    --     end,
	-- },
    {
        "navarasu/onedark.nvim",
        lazy = false,
        config = function()
            vim.cmd([[colorscheme onedark]])
        end,
    },

    -- {
    --     "folke/tokyonight.nvim",
    --     lazy = false, -- make sure we load this during startup if it is your main colorscheme
    --     priority = 1000, -- make sure to load this before all the other start plugins
    --     config = function()
    --       -- load the colorscheme here
    --       vim.cmd([[colorscheme tokyonight]])
    --     end,
    -- },
}
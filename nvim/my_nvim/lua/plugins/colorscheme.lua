return {
    -- https://github.com/rebelot/kanagawa.nvim
    "rebelot/kanagawa.nvim",
    lazy = false,
    priority = 1000,
    config = function()
        -- setup must be called before loading
        vim.cmd("colorscheme kanagawa")
    end,
}
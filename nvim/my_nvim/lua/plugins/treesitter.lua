return {
    -- https://github.com/nvim-treesitter/nvim-treesitter
    "nvim-treesitter/nvim-treesitter",
    version = "*",
    config = function()
        -- Customize Treesitter
        require('nvim-treesitter.configs').setup {
            ensure_installed = {
                "lua",
                "vim",
                "c",
                "cpp",
                "python",
                -- add more arguments for adding more treesitter parsers
            },
            -- Install parsers synchronously (only applied to `ensure_installed`)
            sync_install = true,
            highlight = {
                enable = true
            },
        }
    end,
    run = ":TSUpdate"
}
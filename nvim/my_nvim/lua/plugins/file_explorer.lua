return {
    -- https://github.com/nvim-tree/nvim-tree.lua
    "nvim-tree/nvim-tree.lua",
    lazy = false,
    dependencies = {
        "nvim-tree/nvim-web-devicons",
    },
    version = "*",
    config = function()
        require("nvim-tree").setup {
            sort = {
                sorter = "case_sensitive",
            },
            view = {
                width = 30,
            },
            renderer = {
                group_empty = true,
            },
            filters = {
                dotfiles = false,
            },
        }
    end,
}

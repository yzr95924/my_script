return {
    {
        -- https://github.com/windwp/nvim-autopairs
        "windwp/nvim-autopairs",
        event = "InsertEnter",
        version = "*",
        config = function()
            require("nvim-autopairs").setup({})
        end
    },
    {
        -- https://github.com/cappyzawa/trim.nvim
        "cappyzawa/trim.nvim",
        version = "*",
        config = function()
            require("trim").setup({
                ft_blocklist = {"binary"},
                trim_on_write = true,
                patterns = {
                    [[%s/\(\n\n\)\n\+/\1/]], -- replace multiple blank lines with a single line
                }
            })
        end
    },
    {
        -- https://github.com/chentoast/marks.nvim
        "chentoast/marks.nvim",
        version = "*",
        config = function()
            require("marks").setup({
                default_mappings = false,
                builtin_marks = {
                    "$##$",
                },
                refresh_interval = 250,
            })
        end
    }
}

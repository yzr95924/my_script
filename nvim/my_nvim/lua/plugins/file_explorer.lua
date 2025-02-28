return {
    -- {
    --     -- https://github.com/nvim-tree/nvim-tree.lua
    --     "nvim-tree/nvim-tree.lua",
    --     lazy = false,
    --     dependencies = {
    --         "nvim-tree/nvim-web-devicons",
    --     },
    --     version = "*",
    --     config = function()
    --         require("nvim-tree").setup {
    --             sort = {
    --                 sorter = "case_sensitive",
    --             },
    --             view = {
    --                 width = 30,
    --             },
    --             renderer = {
    --                 group_empty = true,
    --             },
    --             filters = {
    --                 dotfiles = false,
    --             },
    --         }
    --     end,
    -- },
    {
        -- https://github.com/nvim-neo-tree/neo-tree.nvim
        "nvim-neo-tree/neo-tree.nvim",
        version = "*",
        dependencies = {
            "nvim-lua/plenary.nvim",
            "nvim-tree/nvim-web-devicons", -- not strictly required, but recommended
            "MunifTanjim/nui.nvim",
            -- {"3rd/image.nvim", opts = {}}, -- Optional image support in preview window: See `# Preview Mode` for more information
        },
        config = function()
            require("neo-tree").setup {
                filesystem = {
                    filtered_items = {
                        visible = true, -- If set this to `true`, all "hide" just mean "dimmed out"
                        hide_dotfiles = false,
                        hide_gitignored = true,
                    }
                }
            }
        end,
    }
}

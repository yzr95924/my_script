return {
    -- https://github.com/folke/which-key.nvim
    "folke/which-key.nvim",
    dependencies = {
        "echasnovski/mini.icons",
    },
    version = "*",
    event = "VeryLazy",
    keys = {
        {
            "<leader>?",
            function()
                require("which-key").show({ global = false })
            end,
            desc = "Buffer Local Keymaps (which-key)",
        },
    },
}

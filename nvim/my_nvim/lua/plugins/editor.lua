return {
    {
        "windwp/nvim-autopairs",
        event = "InsertEnter",
        version = "*",
        config = function()
            require("nvim-autopairs").setup({})
        end
    },
}

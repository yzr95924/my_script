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
    highlight = { enable = true },
}
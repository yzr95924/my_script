local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
  vim.fn.system({
    "git",
    "clone",
    "--filter=blob:none",
    "https://github.com/folke/lazy.nvim.git",
    "--branch=stable", -- latest stable release
    lazypath,
  })
end
vim.opt.rtp:prepend(lazypath)

-- After installation, run `checkhealth lazy` to see if everything goes right

require("lazy").setup({
    -- LSP manager
    {
        'neoclide/coc.nvim',
        branch = 'release',
        lazy = false,
        run = ':CocInstall coc-clangd' -- install clangd
    },
    -- Colorscheme
    {
        'rebelot/kanagawa.nvim',
        lazy = false,
    },
    {
        'nvim-treesitter/nvim-treesitter',
        config = function()
            require('config.nvim-treesitter')
        end,
        run = ':TSUpdate'
    },
    -- fuzzy finder
    {
        'nvim-telescope/telescope.nvim',
        tag = '0.1.8',
    },
    -- file explorer
    {
        "nvim-tree/nvim-tree.lua",
        lazy = false,
        dependencies = {
            "nvim-tree/nvim-web-devicons",
        },
        config = function()
            require('config.nvim-tree')
        end,
    },
})

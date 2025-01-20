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
        branch = 'release'
    },
    -- Colorscheme
    {
        'rebelot/kanagawa.nvim',
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
    -- bar
    {
        'nvim-lualine/lualine.nvim',
        dependencies = { 'nvim-tree/nvim-web-devicons' },
        options = {
            icons_enabled = false,
        }
    },
    -- file explore
--     {
--         return {
--   "nvim-tree/nvim-tree.lua",
--   version = "*",
--   lazy = false,
--   dependencies = {
--     "nvim-tree/nvim-web-devicons",
--   },
--   config = function()
--     require("nvim-tree").setup {}
--   end,
-- }
})

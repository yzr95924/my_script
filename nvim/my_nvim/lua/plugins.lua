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
})

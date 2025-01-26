local status_ok, which_key = pcall(require, "which-key")
if not status_ok then
    return
end

local setup = {
    plugins = {
        marks = true, -- shows a list of your marks on ' and `
        registers = true, -- shows your registers on " in NORMAL or <C-r> in INSERT mode
        spelling = {
            enabled = true, -- enabling this will show WhichKey when pressing z= to select spelling suggestions
            suggestions = 20, -- how many suggestions should be shown in the list?
        },
        -- the presets plugin, adds help for a bunch of default keybindings in Neovim
        -- No actual key bindings are created
        presets = {
            operators = false, -- adds help for operators like d, y, ... and registers them for motion / text object completion
            motions = true, -- adds help for motions
            text_objects = true, -- help for text objects triggered after entering an operator
            windows = true, -- default bindings on <c-w>
            nav = true, -- misc bindings to work with windows
            z = true, -- bindings for folds, spelling and others prefixed with z
            g = true, -- bindings for prefixed with g
        },
    },
    -- add operators that will trigger motion and text object completion
    -- to enable all native operators, set the preset / operators plugin above
    -- operators = { gc = "Comments" },
    icons = {
        breadcrumb = "»", -- symbol used in the command line area that shows your active key combo
        separator = "➜", -- symbol used between a key and it's label
        group = "+", -- symbol prepended to a group
    },
    layout = {
        height = { min = 4, max = 25 }, -- min and max height of the columns
        width = { min = 20, max = 50 }, -- min and max width of the columns
        spacing = 3, -- spacing between columns
        align = "left", -- align columns left, center or right
    },
    timeout = false
    -- triggers = {"<leader>"} -- or specify a list manually
}

-- define key mapping
local keys = {
    {
        -- for Telescope
        {"<leader>f", group = "Telescope"},
        {"<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find Files", noremap = true},
        {"<leader>fg", "<cmd>Telescope live_grep<cr>", desc = "Live Grep", noremap = true},
        {"<leader>fc", "<cmd>Telescope commands<cr>", desc = "List Commands", noremap = true},
        {"<leader>fb", "<cmd>Telescope buffers<cr>", desc = "List Buffer", noremap = true},
    },
    {
        -- for Bufferline
        {"<leader>b", group = "Bufferline"},
        {"<leader>bn", "<cmd>BufferLineCycleNext<cr>", desc = "Next Buffer", noremap = true},
        {"<leader>bp", "<cmd>BufferLineCyclePrev<cr>", desc = "Prev Buffer", noremap = true},
        {"<leader>bs", "<cmd>BufferLinePick<cr>", desc = "Pick Buffer", noremap = true},
        {"<leader>bc", "<cmd>BufferLinePickClose<cr>", desc = "Close Buffer", noremap = true},
    },
    {
        -- for Lsp Coc
        {"<leader>l", group = "Lsp Coc"},
        {"<leader>ll", "<cmd>CocOutline<cr>", desc = "List Outline", noremap = true},
        {"<leader>li", "<cmd>CocCommand document.showIncomingCalls<cr>", desc = "Show Incoming Calls", noremap = true},
        {"<leader>lo", "<cmd>CocCommand document.showOutgoingCalls<cr>", desc = "Show Outgoing Calls", noremap = true},
        -- Formatting selected code
        {"<leader>lf", "<Plug>(coc-format-selected)", desc = "Format Selected Code", noremap = true, mode = {"n", "x"}},
        -- Remap keys for apply refactor code actions.
        {"<leader>le", "<Plug>(coc-codeaction-refactor)", desc = "Refactor", noremap = true, mode = {"n"}},
        {"<leader>lr", "<Plug>(coc-codeaction-refactor-selected)", desc = "Refactor Selected Code", noremap = true, mode = {"n", "x"}},
        {"<leader>lc", "<C-U><cmd>CocList commands<cr>", desc = "Show Commands", noremap = true, nowait = true, mode = {"n"}},
        {"<leader>ls", "<C-U><cmd>CocList outline<cr>", desc = "List Symbol", noremap = true, nowait = true, mode = {"n"}},
    },
    {
        -- for NvimTree
        {"<leader>n", group = "NvimTree"},
        {"<leader>no", "<C-U><cmd>NvimTreeToggle<cr>", desc = "Toggle Tree", noremap = true, nowait = true},
        {"<leader>nc", "<C-U><cmd>NvimTreeCollapse<cr>", desc = "Toggle Tree Collapse", noremap = true, nowait = true},
    },
    {
        -- for Git
        {"<leader>g", group = "Git Tool"},
        {"<leader>gd", "<C-U><cmd>DiffviewOpen HEAD<cr>", desc = "HEAD Diff Open", noremap = true, nowait = true},
        {"<leader>gc", "<C-U><cmd>DiffviewClose<cr>", desc = "Diff Close", noremap = true, nowait = true},
        {"<leader>gh", "<C-U><cmd>DiffviewFileHistory %<cr>", desc = "Show File History", noremap = true, nowait = true},
    }
}

-- register the key mapping
which_key.setup(setup)
which_key.add(keys)

return {
    {
        -- https://github.com/nvim-lualine/lualine.nvim
	    "nvim-lualine/lualine.nvim",
	    dependencies = {
            "nvim-tree/nvim-web-devicons"
        },
        version = "*",
	    config = function()
	    	require("lualine").setup(
                {
                    options = {
			            icons_enabled = true,
			            theme = vim.g.hardhacker_lualine_theme,
			            component_separators = "",
			            disabled_filetypes = {
				            statusline = {},
				            winbar = {},
			            },
			            ignore_focus = {},
			            always_divide_middle = true,
			            globalstatus = true,
			            refresh = {
			                statusline = 1000,
			                tabline = 1000,
			                winbar = 1000,
			            },
		            },
                    sections = {
                        lualine_b = {
				            { "branch" },
				            { "diff" },
			            },
                        lualine_c = {
                            {
                                "filename",
                                file_status = true, -- Displays file status (readonly status, modified status)
					            newfile_status = false, -- Display new file status (new file means no write after created)
                                path = 1,
                                symbols = {
						            modified = "[+]", -- Text to show when the file is modified.
						            readonly = "[-]", -- Text to show when the file is non-modifiable or readonly.
						            unnamed = "[No Name]", -- Text to show for unnamed buffers.
						            newfile = "[New]", -- Text to show for newly created file before first write
					            },
                            }
                        },
                    },
                    tabline = {},
		            winbar = {},
		            inactive_winbar = {},
		            extensions = {},
                }
            )
	    end,
    },
    {
        -- https://github.com/akinsho/bufferline.nvim
        "akinsho/bufferline.nvim",
        version = "*",
        config = function()
            require("bufferline").setup(
                {
                    highlights = {
                        buffer_selected = { bold = true },
                        diagnostic_selected = { bold = true },
                        info_selected = { bold = true },
                        info_diagnostic_selected = { bold = true },
                        warning_selected = { bold = true },
                        warning_diagnostic_selected = { bold = true },
                        error_selected = { bold = true },
                        error_diagnostic_selected = { bold = true },
                    },
                    options = {
                        numbers = "ordinal",
                        offsets = {
                            -- 侧边窗口偏移
                            {
                                filetype = "NvimTree", -- 侧边窗口类型
                                text = "File Explorer", -- 偏移文本
                                text_align = "center", -- 文本对齐方式
                                separator = true, -- 是否显示分隔符
                            }
                        },
                        diagnostics = "coc",
                        diagnostics_update_in_insert = false, -- only applies to coc
                        diagnostics_update_on_event = true, -- use nvim's diagnostic handler
                        always_show_bufferline = true, -- 始终显示缓冲区行
                        indicator = {
                            icon = "▎", -- this should be omitted if indicator style is not 'icon'
                            style = "underline",
                        },
                    },
                }
            )
        end,
    }
}

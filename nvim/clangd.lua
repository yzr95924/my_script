return {
    "AstroNvim/astrolsp",
    ---@type AstroLSPOpts
    opts = function(plugin, opts)
	    opts.servers = opts.servers or {}
	    vim.list_extend(opts.servers, {
		    "clangd",
	    })
    end,
}

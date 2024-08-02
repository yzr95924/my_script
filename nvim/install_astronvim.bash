#!/bin/bash
git clone --depth 1 https://github.com/AstroNvim/template ~/.config/nvim

echo "start to install clangd"
npm install clangd
cp ./clangd.lua ~/.config/nvim/lua/plugins/clangd.lua

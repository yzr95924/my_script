#!/bin/bash
echo "remove nvim config"
rm -rf ~/.config/nvim

echo "remove nvim plugin"
rm -rf ~/.local/share/nvim

echo "remove coc plugin"
rm -rf ~/.config/coc

echo "replace my nvim option"
cp -r ./my_nvim ~/.config/nvim


cp ./coc-settings.json ~/.config/nvim/coc-settings.json

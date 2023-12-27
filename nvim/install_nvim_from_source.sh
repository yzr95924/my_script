git clone https://github.com/neovim/neovim.git ~/neovim
sudo apt-get install gettext cmake unzip

cd ~/neovim
git checkout release-0.9
make distclean && make CMAKE_BUILD_TYPE=Release
sudo make install

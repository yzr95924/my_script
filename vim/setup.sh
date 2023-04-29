# set up the vim config
echo "Set up the vim colors"
touch ~/.vimrc
cp vimrc ~/.vimrc
mkdir -p ~/.vim/colors
cp molokai.vim ~/.vim/colors/
echo "Done"

sudo apt-get install exuberant-ctags

echo "Set up plug.vim"
if [ ! -e "$HOME/.vim/autoload/plug.vim" ];then
    curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
else 
    echo "plug.vim already exists"
fi
echo "Done"

# set up the vim config
echo "Set up the vim colors"
touch ~/.vimrc
cp vimrc ~/.vimrc
mkdir -p ~/.vim/colors
cp molokai.vim ~/.vim/colors/
echo "Done"

sudo apt-get install python2-dev exuberant-ctags

echo "Set up plug.vim"
if [ ! -e "$HOME/.vim/autoload/plug.vim" ];then
    mkdir -p $HOME/.vim/autoload
    cp plug.vim $HOME/.vim/autoload
else 
    echo "plug.vim already exists"
fi
echo "Done"

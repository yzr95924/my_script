# set up the vim config
echo "Set up the vim colors"
touch ~/.vimrc
cp vimrc ~/.vimrc
mkdir -p ~/.vim/colors
cp molokai.vim ~/.vim/colors/
echo "Done"

echo "Set up plug.vim"
curl -fLo ~/.vim/autoload/plug.vim --create-dirs \
        https://raw.githubusercontent.com/junegunn/vim-plug/master/plug.vim
echo "Done"

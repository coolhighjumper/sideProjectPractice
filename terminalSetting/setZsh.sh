chsh -s /bin/zsh
git clone git://github.com/robbyrussell/oh-my-zsh.git ~/.oh-my-zsh
cp .zshrc $HOME

brew install vim --with-python3
cp .vimrc $HOME
cp -r .vim $HOME
git clone https://github.com/gmarik/vundle.git ~/.vim/bundle/vundle

source $HOME/.zshrc
vim +PluginInstall +qall

git clone https://github.com/powerline/fonts.git
./fonts/install.sh

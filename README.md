getting started on linux

```bash
sudo apt update &&
sudo apt install -y
    make \
    build-essential \
    libssl-dev \
    zlib1g-dev \
    libbz2-dev \
    libreadline-dev \
    libsqlite3-dev \
    wget \
    curl \
    llvm \
    libncurses5-dev \
    libncursesw5-dev \
    xz-utils \
    tk-dev \
    libffi-dev \
    liblzma-dev \
    git
```

add to your `.bashrc`
```bash
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"
```

then run
```bash
pyenv install 3.12.5;
```

while in the project directory run
```bash
cd /path/to/the/project;
pyenv local 3.12.5;
```

then run
```bash
pyenv activate env
# to exit
pyenv deactivate
```

```bash
pip install -r requirements.txt
```

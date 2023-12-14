#!/bin/bash
if [ $OS_NAME == 'macos-latest' ]; then
  export PATH="$HOME/miniconda/bin:$PATH"
  source $HOME/miniconda/bin/activate
  conda activate ci
fi

pip install -v '.[htseq-qa]'
if [ $? != 0 ]; then
    exit 1
fi

# OSX makes wheels as well, test it to make sure
if [ $OS_NAME == 'macos-latest' ]; then
  mkdir wheelhouse
  pip wheel . -w wheelhouse/
  if [ $? != 0 ]; then
      exit 1
  fi
  #FIXME
  ls wheelhouse
fi

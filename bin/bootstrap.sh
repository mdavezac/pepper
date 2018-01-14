#! /bin/bash
set -e

prefix=$(pwd)
condiment_dir=$prefix/CondimentStation
virtenv=$prefix/build/salt-env
condiment_repo=git@github.com:mdavezac/CondimentStation.git

mkdir -p $(pwd)/build

## If the CondimentStation hasn't been run before, create the virtenv
if [ ! -d "$virtenv" ]; then
  python3 -m venv $virtenv
  . $virtenv/bin/activate
  pip install --upgrade pip salt click GitPython mako pytest ipython virtualenv packaging
fi

## If running this on a mac, install Homebrew!!
if [[ "$(uname)" == "Darwin" ]] && [[ ! -e /usr/local/bin/brew ]]
then
   sudo chown -R $(whoami) /usr/local
   ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
fi

## If the Condiment pinch.py doesn't exists...  then clone repository!
if [[ ! -e "$condiment_dir/bin/pinch.py" ]] ; then
  git clone $condiment_repo
fi

setups=(server_hierarchy syspath minion pillar sync)
for setup_i in ${setups[@]}; do
    $virtenv/bin/python $condiment_dir/bin/pinch.py setup ${setup_i} $prefix
done

## If a black-garlic repository exists, then update the states
if [[ -d "$prefix/black-garlic/.git" ]] ; then
  $virtenv/bin/python $condiment_dir/bin/pinch.py update
fi

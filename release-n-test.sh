. $HOME/.bashrc&> /dev/null
. .env||echo "No .env file found.  Assuming that is fine"
git commit pyproject.toml jgtutils/__init__.py package.json -m bump &>/dev/null

. scripts/version-patcher.sh
cversion=$(cat pyproject.toml |tr '"' " " |awk '/version/ {print $3}')
git commit . -m "v$cversion" && git tag "$cversion" && git push --tags && git push 

make dist && twine upload dist/* 
#&& sleep 32 &&  (conda activate jgtpy && pip install -U jgtutils ;(conda activate jgtfxcon && pip install -U jgtutils) )

# install upgrade in the user environment
#if [ "$CONDA_ENV_PROD_BASE" == "" ]; then
#	CONDA_ENV_PROD_BASE=$(conda info --base||echo "baseprod")
#fi
#((sleep 25;conda activate $CONDA_ENV_PROD_BASE &&  pip install --user -U jgtutils) &> /dev/null)&
sleep 15;postdistpyproject


. scripts/version-patcher.sh
cversion=$(cat setup.py |tr "'" " " |awk '/version/ {print $2}')
git commit . -m "v$cversion" && git tag "$cversion" && git push --tags && git push 

make dist && twine upload dist/* && sleep 32 &&  (conda activate jgtpy310 && pip install -U jgtutils ;(conda activate jgtfxcon && pip install -U jgtutils) )

# install upgrade in the user environment
((sleep 25;conda activate base;pip install --user -U jgtutils) &> /dev/null)&
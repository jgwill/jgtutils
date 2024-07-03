
echo "THIS IS TO BE COMPLETED 240703"
echo "    see it as the next version of postdistpyproject function"

sleep 33

if [ ! -e pyproject.toml ];then 
        echo "No pyproject.toml file found. Not a python project?"
else

	current_package_name=$(cat pyproject.toml |grep name|head -n 1 -|tr '"' ' '|awk '{print $3}')
	if [ "$current_package_name" == "" ];then echo "No package name found in pyproject.toml";return;fi

	. .env||echo "No .env file found.  Assuming that is fine"

	if [ "$WS_CONDA_DEV_ENV_DEPENDENCIES_AUTOUPGRADE" == "" ];then
		echo "WS_CONDA_DEV_ENV_DEPENDENCIES_AUTOUPGRADE not set in .env file."
		echo 'WS_CONDA_DEV_ENV_DEPENDENCIES_AUTOUPGRADE="../jgtfxcon ../ids ../fx2console"'
	else
		for package_path in $WS_CONDA_DEV_ENV_DEPENDENCIES_AUTOUPGRADE;do
			
			oldversion=$(cat pyproject.toml|grep "$current_package_name"|tr '>' ' '|tr "'" " "|tr "=" " "|tr "," " "|awk '{print $2}')
			# validate we got the oldversion
			if [ "$oldversion" == "" ];then echo "No old version found in pyproject.toml";return;fi

			tconda_env_name="$WS_CONDA_ENV_NAME"
			if [ "$tconda_env_name" == "" ];then
				tconda_env_name="$p" #We assume the conda env of the developped package is the same as the package name
			fi

			(conda activate $p&>/dev/null;pip install -U jgtutils|tr '(' ' '|tr ')' ' '|grep "jgtpy in"|awk '/jgtpy/{print $7}')
			newversion=$(conda activate jgtml&>/dev/null;pip install -U jgtpy|tr '(' ' '|tr ')' ' '|grep "jgtpy in"|awk '/jgtpy/{print $7}')
			# Validate we got the newversion
			if [ "$newversion" == "" ];then echo "No new version found in pyproject.toml";return;fi

			# We want to replace jgtpy>=0.4.70 with jgtpy>=0.4.71
			## run if they are different
			if [ "$oldversion" == "$newversion" ]; then
					echo "No need to update jgtpy version in jgtml package"
			else

				sed -i "s/jgtpy>=$oldversion/jgtpy>=$newversion/g" pyproject.toml
				git add pyproject.toml
				git commit -m "Updated jgtpy version from $oldversion to $newversion"
			fi
		done
fi;fi
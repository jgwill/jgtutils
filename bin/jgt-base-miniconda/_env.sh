ctlid=2408011203
export dockertag=jgwill/jgt:base-miniconda
dockertag1=jgwill/jgt:fxbase

containername=fxbase
dkhostname=$containername

# PORT
#dkport=4000:4000

xmount=$HOME/.jgt/config.json:/root/.jgt/config.json
xmount2=$HOME/.jgt/settings.json:/root/.jgt/settings.json

#xmount2=/var:/a/var


dkcommand=/upbash.sh #command to execute (default is the one in the dockerfile)

dkextra=" -v $(realpath $(pwd)/../../):/app -v $(pwd)/upjgt.sh:/upjgt.sh -v $(pwd)/upbash.sh:/upbash.sh "
#dkextra=" -v \$dworoot/x:/x -p 2288:2288 "

#dkmounthome=true


##########################
############# RUN MODE
#dkrunmode="bg" #default fg
#dkrestart="--restart" #default
#dkrestarttype="unless-stopped" #default


#########################################
################## VOLUMES
#dkvolume="myvolname220413:/app" #create or use existing one
#dkvolume="$containername:/app" #create with containername name



#dkecho=true #just echo the docker run


# Use TZ
#DK_TZ=1



#####################################
#Build related
#
##chg back to that user
#dkchguser=vscode

######################## HOOKS BASH
### IF THEY EXIST, THEY are Executed, you can change their names

dkbuildprebuildscript=dkbuildprebuildscript.sh
dkbuildbuildsuccessscript=dkbuildbuildsuccessscript.sh
dkbuildfailedscript=dkbuildfailedscript.sh
dkbuildpostbuildscript=dkbuildpostbuildscript.sh

###########################################
# Unset deprecated
unset DOCKER_BUILDKIT


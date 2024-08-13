FROM jgwill/ubuntu
#FROM jgwill/ubuntu:py3.10.14-ml
RUN apt update && apt install -y vim curl jq 
#RUN pip install json2bash
#RUN pip install -U pip

USER root
WORKDIR /app
# Create a non-root user and switch to it
RUN adduser --disabled-password --gecos '' --shell /bin/bash user \
&& chown -R user:user /app
RUN echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/90-user


USER user
# All users can use /home/user as their home directory
ENV HOME=/home/user
RUN mkdir $HOME/.cache $HOME/.config \
&& chmod -R 777 $HOME




# Set up the Conda environment
ENV CONDA_AUTO_UPDATE_CONDA=false \
    PATH=$HOME/miniconda/bin:$PATH
RUN curl -sLo ~/miniconda.sh https://repo.continuum.io/miniconda/Miniconda3-py310_24.4.0-0-Linux-x86_64.sh \
 && chmod +x ~/miniconda.sh \
 && ~/miniconda.sh -b -p ~/miniconda \
 && rm ~/miniconda.sh \
 && conda clean -ya


RUN pip install -U pip

#RUN pip install -U jgtfxcon
WORKDIR /work

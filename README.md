# TCP_Chat

Project objective: create a terminal based group chat, so that there is a server where the rest of the clients connect to. 

## How to use it

First clone the repository

```bash
git clone https://github.com/mariorodvenUS/tcp_chat.git
```
Now you have two options if you want to execute the program, using docker o either using your own machine.

## Using your own machine
Suposing that you are using linux on a debian based distro like Ubuntu, Mint or Debian itself just run this as sudo:

```bash
apt install nmap python3 python3-pip python3-venv nmap
```

Once you have installed that, get in the directory and run:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r client/requirements.txt
```

There you go, now you can run either the client or the server in that terminal window. If you want to run both in the same Pc, just run the last two commands on another terminal in the same directory.

## Using docker
I will assume that docker is installed in your OS, and that you are in the group docker(you can check it by running ```groups $(whoami)`` in linux`). To setup the docker images just get in the directory of the client or the server and run this:

#### Client

```bash
cd tcp_chat/client
docker build --tag <image-tag> .
docker run -it --name <container-tag> <image-tag>
```
Replace image-tag and container-tag with a name that you would like to use.

#### Server

```bash
cd tcp_chat/server
docker build --tag <image-tag> .
docker run -it --name <container-tag> <image-tag>
```
Replace image-tag and container-tag with a name that you would like to use.

If you find any bug or think out any way to improve the project, feel free to text about it in the issues section.

HOla caracola
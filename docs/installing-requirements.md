# Installing Requirements

## Requirements

To get started, you'll need these software installed:

- [Git](https://git-scm.com/)
- [Python 3](https://www.python.org/) (Python 3.10 is what the codebase uses)
- [Poetry](https://python-poetry.org/)
- [Pyenv](https://github.com/pyenv/pyenv) (Optional, Recommended)
- [WSL2](https://docs.microsoft.com/en-us/windows/wsl/) (If working on Windows)
- [Docker](https://www.docker.com/) (Use [Docker Engine](https://docs.docker.com/engine/) on Linux, [Docker Desktop](https://www.docker.com/products/docker-desktop/) on Windows/WSL2, MacOS and Linux (beta))
- Discord Account + Discord App

> **Note**
> Xelt v3 is natively developed on Linux. This means that you must have a good understanding on how to use Linux in the terminal. It is recommended to use Ubuntu to start with, but more advanced users may feel more comfortable with other distros such as Arch. If you are using Windows, you must use WSL2.

## Development Prerequisites

These are the prerequisites packages for development

### Debian/Ubuntu

```sh 
sudo apt-get install libffi-dev python3-dev libnacl-dev build-essentials \
libssl-dev curl wget git
```

> **Note**
> `uvloop` depends on shared libs from OpenSSL 1.1. You'll need to use the backport versions for Ubuntu 22.04 and higher

### RHEL/CentOS/Fedora 22 or below

```sh
sudo yum install make gcc libffi-devel python-devel \
openssl-devel curl wget git
```
### Fedora 23+

```sh
sudo dnf install make automake gcc gcc-c++ kernel-devel \
libffi-devel python3-libnacl python3.10-devel openssl11-devel \
openssl-devel curl wget git
```

### OpenSUSE

```sh
sudo zypper install gcc make automake openssl-devel openssl-1_1  \
libffi-devel python310-devel python310-libnacl wget git curl
```

### Arch

```sh
sudo pacman -S --needed base-devel openssl openssl-1.1 libffi python python-libnacl
```

### MacOS/Homebrew

```sh
brew install openssl openssl@1.1 libffi git curl make
```

## Development Setup

1. Fork and clone the repo

    ```sh
    git clone https://github.com/[username]/Xelt.py.git && cd Xelt.py
    ```

    Or if you have the `gh` cli tool installed:

    ```sh
    gh repo clone [username]/Xelt.py
    ```

    > **Note**
    > To those who are collaborators on this org, all you need to do is to clone the repo, and push to the main dev branch (`dev/v3`) instead


2. Run `make` to create the venv and install dependencies. This will do any needed setup as well.

    ```sh
    make dev-setup
    ```

    > **Note**
    > To those developing on Windows, you'll need to use WSL2 for most of these. Once you have WSL2 installed and configured, install the dependencies for your distro, and then follow the steps here.

3. Start the Docker Compose stack

    ```sh
    sudo docker compose -f docker-compose-dev.yml up -d
    ```
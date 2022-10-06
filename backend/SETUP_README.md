# Backend Environment Setup

## Automatic Install / Setup
### Run the setup script `backend_environment_initial_setup.sh`
`sudo backend_environment_initial_setup.sh`

Done!

## Manual Install

### Install required packages

Install Python3
`sudo apt install python3 -y`

Install Python3-venv (Virtual Environment)
`sudo apt install python3-venv -y`

Install mariadb-server (& autoinstall its dependencies)
`sudo apt install mariadb-server -y`

### Python Environment Setup

Create Virtual Environment (python3-venv)
`python3 -m venv ./fmeca-venv`

Change source to venv `source ./fmeca-venv/bin/activate`

Install PIP packages
`pip3 install -r requirements.txt`

System is now ready to use. Check `USAGE_README.md` for usage instructions.

When done, Exit again by typing
`deactivate`

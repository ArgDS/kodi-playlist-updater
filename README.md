# Kodi playlist updater

## Summary
This application help to update playlist by schedule by list of file from ftp and update used playlist into player.
  
## Requirments

Python version 3.8+

## Install
For installing virtual environment for python execute command:
```shell script
python -m venv ./venv
# For windows activate.bat or activate.ps1 for PowerShell
./venv/Sctipts/activate
python setup.py install
```

### Deactivate python virtual environment
For Linux - close terminal session
For Windows execute script 
```shell script
./venv/Scripts/deactivate.bat
```

## Configuration

### Logging
If you want to change a logging configuration sets a path of logging configuration at the environment variable "__LOG_CFG__".
Example of logging configuration you find into the file ".config/logging.yml".

## Run
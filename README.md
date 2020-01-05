# Kodi playlist updater

## Summary
This application help to update playlist by schedule by list of file from ftp and update used playlist into player.
  
## Requirments

- Python version 3.8+
- pipenv

## Install
For installing virtual environment for python execute command:
```shell script
pipenv install
```

## Configuration

### Logging
If you want to change a logging configuration sets a path of logging configuration at the environment variable "__LOG_CFG__".
Example of logging configuration you find into the file ".config/logging.yml".

## Run
```shell script
pipenv run python main.py --config=<config file>
```
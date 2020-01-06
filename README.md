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

Template of configuration file located in ./config/application.yml
```yaml
---
ftp:
  host: localhost
  port: 21
  username: username
  passwd: password
  protocol: FTP # Can be SFTP, but is not checked 
directories:
  ftp-source: /current
  store: ./store
  store-buffer: ./store-buffer
  archive: ./archive
playlist:
  path: ./playlist.m3u
  remove-delay: 5
kodi:
  host: localhost
  port: 8080
  protocol: http # http or https
  username: username
  passwd: password
```

### Logging
If you want to change a logging configuration sets a path of logging configuration at the environment variable "__LOG_CFG__".
Example of logging configuration you can find into the file "./config/logging.yml".

## Run
### Basic action
If you have a prepared playlist you can use this command:
```shell script
pipenv run python main.py --config=<config file>
```
### Other actions
If you do not have a playlist use this command for initializing:
```shell script
pipenv run python main.py --config=<config file> --init
```

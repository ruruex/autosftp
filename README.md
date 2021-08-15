# autosftp
Python SFTP script to verify Internet performance

# Build your own configuration file
Example:
```json
{
    "hostname":"x.x.x.x/hostname",
    "username":"username",
    "password":"secrect",
    "home_dir":"/xxx"
}
```

# Generate dummy file for the sftp test
It's optional, if you have your own files for test
```bash
python3 filegen.py FILE_NAME FILE_SIZE_IN_BYTES
```

# Upload or download file automation test
* method can be get or put
```bash
python3 sftpup.py -f TRANSFER_FILENAME -l CONFIGFILE_NAME -a METHOD
```

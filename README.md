# aerocom user management
small project for ansible based user management of aerocom-users.met.no

This repo is useless without actual access to the Met Norway ostack2 infrastructure

# documentation
## usage prerequest
This tool is meant to provide an easy way to create user yaml files for the creation of 
users for the aerocom's project external user server aerocom-users.met.no.
The actual user creation is done using ansible and the 
[ostack-setup-fou-kl](https://gitlab.met.no/emep/ostack-setup-fou-kl) repository.

**Without a working ansible installation and write access to the ostack2 API for the
repository above, this tools is not usable.**

## Usage
There's the command `aumn_manage_user` in the repository:
```bash
usage: aumn_manage_user [-h] {adduser,addkey} ...

aerocom-users.met.no user management script.

positional arguments:
  {adduser,addkey}  subcommands help
    adduser         adduser help
    addkey          addkey help

options:
  -h, --help        show this help message and exit

```
There's two sub commands:
- adduser (to add new users)
- addkey (to add another public key to an existing user)

### aumn_manage_user adduser
```
usage: aumn_manage_user adduser [-h] [-key KEY] [-keyfile KEYFILE] [-outfile OUTFILE] [-email EMAIL] [-expires EXPIRES] username uid name [name ...]

positional arguments:
  username          UNIX user name to use
  uid               user id (uid) to use
  name              The name of the user (first name, last name). Names will be concatenated.

options:
  -h, --help        show this help message and exit
  -key KEY          ssh key to use. QUOTE CORRECTLY! or use keyfile option
  -keyfile KEYFILE  keyfile to use. one key per line.
  -outfile OUTFILE  outputfile. Defaults to stdout.
  -email EMAIL      email address. Only needed if username is not an email address.
  -expires EXPIRES  user name's expiring date as YYYY-MM-DD. Defaults to today + 2 years.
```

### aumn_manage_user addkey
```
usage: aumn_manage_user addkey [-h]

options:
  -h, --help  show this help message and exit
```
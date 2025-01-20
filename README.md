# Aerocom user management
small project for ansible based user management of aerocom-users.met.no

**This repo is useless without actual access to the Met Norway ostack2 infrastructure, 
write access to the ostack2 API and a working ansible installation.**

# Documentation
## Synopsis
The command line tool `aumn_manage_user` (**aum** from **a**erocom-**u**sers.**m**et.**n**o) is 
provided to generate 
`.yaml` files to be used with ansible to create users and to add additional keys to their 
`~/.ssh/suthorized_keys` file.
For user creation the subcommand `adduser` is provided, for key adding the subcommand `addkey`.

The actual user creation is done using ansible and the 
[ostack-setup-fou-kl](https://gitlab.met.no/emep/ostack-setup-fou-kl) repository 
(on gitlab.met.no; only accessible from within the Met Norway network) .

Accounts created have a standard expiry time 2 years from the time of creation of the `.yaml` file.

**Note:**
Expiry dates can be set using the standard `chage` command.

## Usage
This repo provides the command line tool `aumn_manage_user`.
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
- `adduser` (to add new users)
- `addkey` (to add another public key to an existing user)

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

### output files
To make things easier, the environment variable `OSTACK_SETUP_FOU_KL_PATH` can be set to 
tell where the [ostack-setup-fou-kl](https://gitlab.met.no/emep/ostack-setup-fou-kl) repository 
is located on the user's file system. If that environment variable is set, the output files will be 
put at the right place within the ostack-setup-fou-kl repo 
(at `aerocom/files/aerocom-users_users/external` for external users and 
`aerocom/files/aerocom-users_users/internal` for internal users)
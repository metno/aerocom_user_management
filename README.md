# Aerocom user management
small project for ansible based user management of aerocom-users.met.no

**This repo is useless without actual access to the Met Norway ostack2 infrastructure, 
write access to the ostack2 API and a working ansible installation.**

# Documentation
## Synopsis
The command line tool `aumn_manage_user` (**aum** from **a**erocom-**u**sers.**m**et.**n**o) is 
provided to generate 
`.yaml` files to be used with ansible to create users and to add additional keys to their 
`~/.ssh/authorized_keys` file.
For user creation the subcommand `adduser` is provided, for key adding the subcommand `addkey`.

The actual user creation is done using ansible and the 
[ostack-setup-fou-kl](https://gitlab.met.no/emep/ostack-setup-fou-kl) repository 
(on gitlab.met.no; only accessible from within the Met Norway network) .

All accounts created have a standard expiry time of 2 years from the time of creation of the `.yaml` file.

**Note:**
Expiry dates can be set using the standard `chage` command (from internal account only).

## Usage
This repo provides the command line tool `aumn_manage_user`.
```
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
- `adduser`, to add new users
- `addkey`, to add another public key to an existing user

### aumn_manage_user adduser
```
usage: aumn_manage_user adduser [-h] [-uid UID] [-key KEY [KEY ...]] [-keyfile KEYFILE] [-outfile OUTFILE] [-email EMAIL] [-expires EXPIRES] [-i] username name [name ...]

positional arguments:
  username            UNIX user name to use
  name                The name of the user (first name, last name). Names will be concatenated.

options:
  -h, --help          show this help message and exit
  -uid UID            user id (uid) to use
  -key KEY [KEY ...]  ssh key to use. 1 or 3 elements depending on quotation.
  -keyfile KEYFILE    keyfile to use. one key per line.
  -outfile OUTFILE    outputfile. Defaults to stdout.
  -email EMAIL        email address. Only needed if username is not an email address.
  -expires EXPIRES    user name's expiring date as YYYY-MM-DD. Defaults to today + 2 years.
  -i, --internal      create an internal user (will get sudo rights).
```

### aumn_manage_user addkey
```
usage: aumn_manage_user addkey [-h] [-d] [-keyfile KEYFILE] [-key KEY [KEY ...]] file

positional arguments:
  file                yaml file to add a new public key to.

options:
  -h, --help          show this help message and exit
  -d, --dryrun        dryrun; print yaml file to stdout.
  -keyfile KEYFILE    keyfile to add to yaml file (all keys).
  -key KEY [KEY ...]  key to add to yaml file. 1 or 3 elements depending on quotation.
```

### Examplles
#### add external user griesfel@met.no; print resulting yaml file to stdout
`aumn_manage_user adduser griesfel@met.no Jan Griesfeller -keyfile ~/.ssh/id_rsa.pub`

`aumn_manage_user adduser griesfel@met.no Jan Griesfeller -key '<key>'`

#### add external user griesfel@met.no; create yaml file
`aumn_manage_user adduser griesfel@met.no Jan Griesfeller -keyfile ~/.ssh/id_rsa.pub -outfile jang.yaml`

`aumn_manage_user adduser griesfel@met.no Jan Griesfeller -key '<key>' -outfile jang.yaml`

#### add internal user griesfel; print yaml file:

`aumn_manage_user adduser griesfel Jan Griesfeller -i -email griesfel@met.no -keyfile ~/.ssh/id_rsa.pub`

`aumn_manage_user adduser griesfel Jan Griesfeller -i -email griesfel@met.no -key '<key>'` 

#### add public key to existing yaml file; print resulting file to stdout 

`aumn_manage_user addkey <file>.yaml --dryrun -key '<key>'`

#### add public key to existing yaml file; modify the input file

`aumn_manage_user addkey <file>.yaml -key '<key>'`

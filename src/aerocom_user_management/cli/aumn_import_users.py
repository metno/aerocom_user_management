import argparse
import subprocess
import sys
import re
import os
from sys import stderr
import tarfile

import yaml
from aerocom_user_management import const
import datetime as dt
from pathlib import Path

TARDIR = Path("/home/jang/tmp/aumn_management/")

def main():
    # define some terminal colors to be used in the help
    colors = {
        "BOLD": "\033[1m",
        "UNDERLINE": "\033[4m",
        "END": "\033[0m",
        "PURPLE": "\033[95m",
        "CYAN": "\033[96m",
        "DARKCYAN": "\033[36m",
        "BLUE": "\033[94m",
        "GREEN": "\033[92m",
        "YELLOW": "\033[93m",
        "RED": "\033[91m",
    }
    # set default output path
    try:
        default_output_path=os.environ["OSTACK_SETUP_FOU_KL_PATH"]
    except KeyError:
        default_output_path=None
    # Create the parser
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="aumn_import_user",
        description="aerocom-users.met.no user moving script.",
        epilog=f"""
{colors['UNDERLINE']}user map file example:{colors['END']}
43626#jang#

{colors['UNDERLINE']}user file example:{colors['END']}
drwxr-xr-x  27 jang                                     jang         4096 2024-11-18 jang/
drwxr-x---  11 ripe@griesfeller.net                     aerocomftp   4096 2024-01-12 ripe@griesfeller.net/

{colors['BOLD']}Example usages:{colors['END']}\n
{colors['UNDERLINE']}- basic usage:{colors['END']}
aumn_import_user <user mapping file> <user file>
    """,
    )


    # Add arguments
    parser.add_argument(
        "usermapfile",
        type=Path,
        help="user mapping file",
    )
    parser.add_argument(
        "userfile",
        type=Path,
        help="user file",
    )
    parser.add_argument('-o', '--outdir', type=Path, help='output directory. Defaults to stdout')

    # Parse the arguments
    args = parser.parse_args()

    options = {}
    options["usermapfile"] = args.usermapfile
    options["userfile"] = args.userfile
    options["outdir"] = args.outdir
    if options["outdir"] is not None and not options["outdir"].exists():
        print(f"Error: output directory {options['outdir']} does not exist.")
        sys.exit(1)

    # to get the uid for a given username
    uids = {}
    with open(options["usermapfile"], "r") as f:
        for line in f:
            split_arr = line.strip().split("#")
            uid = split_arr[0]
            username = split_arr[1]
            uids[username] = uid

    # to get the home directory for a given user
    # they might not be the same!
    home_dirs = {}
    with open(options["userfile"], "r") as f:
        for line in f:
            split_arr = " ".join(line.strip().split()).split()
            username = split_arr[2]
            homedir = split_arr[-1].replace("/","")
            home_dirs[username] = homedir

    for homedir in sorted(home_dirs):
        stdout = subprocess.STDOUT
        stderr = subprocess.PIPE
        if len(homedir) > 32:
            print(f"Error: user name {homedir }is longer than 32 characters. Skipping...")
            continue
        if homedir in uids:
            auth_file = TARDIR / Path(homedir) / ".ssh" / "authorized_keys"
            # read authorized_keys file
            if not auth_file.exists():
                print(f"Error: given keyfile does not exist {auth_file}.")
                sys.exit(1)

            call_arr = []
            # this puts the resultimg yaml file to stdout...
            call_arr.extend(['aumn_manage_user', 'adduser',  homedir, uids[homedir], homedir, "-keyfile", str(auth_file)])
            if int(uids[homedir]) < 60000:
                file_add = "internal"
                email = f"{homedir}@met.no"
                call_arr.extend(["-email", email])
            else:
                file_add = "external"

            if options["outdir"] is not None:
                out_file = options["outdir"] / f"{homedir}_{file_add}.yaml"
                call_arr.extend(["-outfile", str(out_file)])

            # retcode = subprocess.run(call_arr, stdout=stdout, stderr=stderr, check=True)
            retcode = subprocess.run(call_arr, check=True)
            assert retcode



if __name__ == "__main__":
    main()

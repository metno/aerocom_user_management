import argparse
import sys

import yaml
from aerocom_user_management import const


def main():
    # Create the parser
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
    parser = argparse.ArgumentParser(formatter_class=argparse.RawDescriptionHelpFormatter,
                                     prog="aumn_manage_user",
                                     description="aerocom-users.met.no user management script.",
                                     epilog=f"""{colors['BOLD']}Example usages:{colors['END']}\n
{colors['UNDERLINE']}- basic usage:{colors['END']}
aumn_manage_user 'jan Griesfeller' jang 1000   


    """,
                                     )

    # Add arguments
    parser.add_argument('name', type=str, help='The name of the user (first name, last name). QUOTE CORRECTLY!',
                        )
    parser.add_argument('username', type=str, help='UNIX user name to use', )
    parser.add_argument('uid', type=int, help='user id (uid) to use', )
    parser.add_argument('-key', type=str, help='ssh key to use. QUOTE CORRECTLY! or use keyfile option')
    parser.add_argument('-keyfile', type=str, help='keyfile to use. one key per line.')
    parser.add_argument('-o', "-outfile", type=str, help='outputfile. Defaults to stdout.')
    # parser.add_argument('', type=str, help='')

    # Parse the arguments
    args = parser.parse_args()

    options = {}
    # positional arguments
    options["name"] = args.name
    options["username"] = args.username
    options["uid"] = args.uid
    # optional arguments
    if args.keyfile:
        options['keyfile'] = args.keyfile
    if args.key:
        options['key'] = args.key
    try:
        options['outfile'] = args.outfile
    except AttributeError:
        pass

    # logical checks
    # eiter options['keyfile'] or options['key'] need to exist
    if not "key" in options and not "keyfile" in options:
        print(f"Error: either -key or -keyfile have to be provided.")
        sys.exit(1)

    if options["uid"] > 60000:
        proto_yaml = yaml.safe_load(const.USER_EXTERNAL_PROTO)
    else:
        # do the replacing keyword by keyword for readability
        yaml_str = const.USERS_INTERNAL_PROTO.replace("PROTO_USER",options["username"])
        yaml_str = yaml_str.replace("PROTO_NAME", options["name"])
        yaml_str = yaml_str.replace("PROTO_UID", options["uid"])
        yaml_str = yaml_str.replace("PROTO_UID", options["uid"])



        proto_yaml = yaml.safe_load(yaml_str)
        proto_yaml = yaml.safe_load(const.USERS_INTERNAL_PROTO)

    print(proto_yaml)

if __name__ == "__main__":
    main()

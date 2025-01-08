import argparse
import sys

import yaml
from aerocom_user_management import const
import datetime as dt
from pathlib import Path


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
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="aumn_manage_user",
        description="aerocom-users.met.no user management script.",
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}\n
{colors['UNDERLINE']}- basic usage:{colors['END']}
aumn_manage_user jang 1000 Jan Griesfeller -keyfile ~/.ssh/id_rsa.pub


    """,
    )

    # Add arguments
    parser.add_argument(
        "username",
        type=str,
        help="UNIX user name to use",
    )
    parser.add_argument(
        "uid",
        type=str,
        help="user id (uid) to use",
    )
    parser.add_argument(
        "name",
        type=str,
        help="The name of the user (first name, last name). Names will be concatenated.",
        nargs="+",
    )
    parser.add_argument(
        "-key", type=str, help="ssh key to use. QUOTE CORRECTLY! or use keyfile option"
    )
    parser.add_argument("-keyfile", type=str, help="keyfile to use. one key per line.")
    parser.add_argument("-outfile", type=str, help="outputfile. Defaults to stdout.")
    parser.add_argument(
        "-email",
        type=str,
        help="email address. Only needed if username is not an email address.",
    )
    parser.add_argument(
        "-expires",
        type=str,
        help="user name's expiring date as YYYY-MM-DD. Defaults to today + 2 years.",
    )
    # parser.add_argument('', type=str, help='')

    # Parse the arguments
    args = parser.parse_args()

    options = {}
    # positional arguments
    options["name"] = " ".join(args.name)
    options["username"] = args.username
    options["uid"] = args.uid
    if not options["uid"].isdigit():
        print("UID must be an integer.")
        sys.exit(4)

    # optional arguments
    try:
        options["keyfile"] = Path(args.keyfile)
        options["keys"] = []
        with open(options["keyfile"], "r") as f:
            options["keys"].append(f.read().strip())
    except FileNotFoundError as e:
        print(e)
        sys.exit(3)
    except:
        print(f"Invalid keyfile {args.keyfile}.")
        sys.exit(5)

    options["key"] = args.key
    options["outfile"] = args.outfile
    options["email"] = args.email

    try:
        options["expires"] = dt.datetime.strptime(args.expires, "%Y-%m-%d").timestamp()
    except ValueError as e:
        print(
            f"{e}.Please provide date in the right format or remove the --expires option for an expiring date 2 years from now."
        )
        sys.exit(2)
    except (AttributeError, TypeError):
        options["expires"] = dt.datetime.now().timestamp()
    options["expires"] = f"{int(options['expires'])}"

    # logical checks
    # eiter options['keyfile'] or options['key'] need to exist
    if args.key is None and not "keyfile" in options:
        print(f"Error: either -key or -keyfile have to be provided.")
        sys.exit(1)

    yaml_key_str = yaml.safe_load(const.KEY_PROTO)
    if int(options["uid"]) > 60000:
        yaml_str = yaml.safe_load(const.USER_EXTERNAL_PROTO)
    else:
        # do the replacing keyword by keyword for readability
        yaml_str = const.USERS_INTERNAL_PROTO.replace("PROTO_USER", options["username"])
        yaml_str = yaml_str.replace("PROTO_NAME", options["name"])
        # if the user's email address was privided use that, if not assume that the username is a valid email address
        if "email" in options and options["email"] is not None:
            yaml_str = yaml_str.replace("PROTO_EMAIL", options["email"])
        else:
            yaml_str = yaml_str.replace("PROTO_EMAIL", options["username"])
        yaml_str = yaml_str.replace("PROTO_UID", options["uid"])
        yaml_str = yaml_str.replace("PROTO_EXPIRES", options["expires"])

        if options["key"] is not None:
            # use command line provided key
            yaml_str = yaml_str.replace("PROTO_KEY", options["key"])
        else:
            # set in all keys in the keyfile
            for k_no, key in enumerate(options["keys"]):
                if k_no == 0:
                    yaml_str = yaml_str.replace("PROTO_KEY", key)
                else:
                    print("several keys in key file not implemented yet!")

            # yaml_str = yaml_str.replace("", options[""])

    proto_yaml = yaml.safe_load(yaml_str)
    if options["outfile"] is None:
        print(yaml.dump(proto_yaml))
    else:
        with open(options["outfile"], "w") as f:
            f.writelines(yaml.dump(proto_yaml))


if __name__ == "__main__":
    main()

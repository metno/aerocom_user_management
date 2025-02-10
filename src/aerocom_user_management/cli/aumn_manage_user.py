import argparse
import datetime as dt
import os
import re
import sys
from pathlib import Path

import yaml
from aerocom_user_management import const
from dateutil.relativedelta import relativedelta


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
        default_output_path = os.environ["OSTACK_SETUP_FOU_KL_PATH"]
    except KeyError:
        default_output_path = None
    # Create the parser
    # main_parser = argparse.ArgumentParser(add_help=False)
    parser = argparse.ArgumentParser(
        formatter_class=argparse.RawDescriptionHelpFormatter,
        prog="aumn_manage_user",
        description="aerocom-users.met.no user management script.",
        epilog=f"""{colors['BOLD']}Example usages:{colors['END']}\n
{colors['UNDERLINE']}- add external user griesfel@met.no; print resulting yaml file to stdout:{colors['END']}
aumn_manage_user adduser griesfel@met.no Jan Griesfeller -keyfile ~/.ssh/id_rsa.pub

{colors['UNDERLINE']}- add external user griesfel@met.no; create yaml file:{colors['END']}
aumn_manage_user adduser griesfel@met.no Jan Griesfeller -keyfile ~/.ssh/id_rsa.pub -outfile jang.yaml

{colors['UNDERLINE']}- add internal user griesfel; print yaml file:{colors['END']}
aumn_manage_user adduser griesfel Jan Griesfeller -i -email griesfel@met.no -keyfile ~/.ssh/id_rsa.pub 

IMPORTANT: THIS SCRIPT WILL ONLY CREATE A yaml FILE to be used together with the 
fou-kl ostack setup gitlab repository here: 
https://gitlab.met.no/emep/ostack-setup-fou-kl/-/blob/master/aerocom/README.md?ref_type=heads

Please look there on how to use the resulting yaml file.
    """,
    )
    subparsers = parser.add_subparsers(help='subcommands help')
    parser_adduser = subparsers.add_parser('adduser', help='adduser help')
    parser_addkey = subparsers.add_parser('addkey', help='addkey help')

    # add arguments for addkey
    parser_addkey.add_argument("file", type=str, help="yaml file to add a new public key to.")
    parser_addkey.add_argument("-d", "--dryrun", action="store_true", help="dryrun; print yaml file to stdout.")
    parser_addkey.add_argument("-keyfile", type=Path, help="keyfile to add to yaml file (all keys).")
    parser_addkey.add_argument("-key", type=str,
                               help="key to add to yaml file. 1 or 3 elements depending on quotation.",
                               nargs="+", )

    # Add arguments adduser
    parser_adduser.add_argument(
        "username",
        type=str,
        help="UNIX user name to use",
    )
    parser_adduser.add_argument(
        "-uid",
        type=str,
        help="user id (uid) to use",
    )
    parser_adduser.add_argument(
        "name",
        type=str,
        help="The name of the user (first name, last name). Names will be concatenated.",
        nargs="+",
    )
    parser_adduser.add_argument(
        "-key", type=str, help="ssh key to use. 1 or 3 elements depending on quotation",
        nargs="+",
    )
    parser_adduser.add_argument("-keyfile", type=Path, help="keyfile to use. one key per line.")
    parser_adduser.add_argument("-outfile", type=Path, help="outputfile. Defaults to stdout.");
    parser_adduser.add_argument(
        "-email",
        type=str,
        help="email address. Only needed if username is not an email address.",
    )
    parser_adduser.add_argument(
        "-expires",
        type=str,
        help="user name's expiring date as YYYY-MM-DD. Defaults to today + 2 years.",
    )
    parser_adduser.add_argument('-i', '--internal', action="store_true",
                                help='create an internal user (will get sudo rights).')
    # parser.add_argument('', type=str, help='')

    # Parse the arguments
    args = parser.parse_args()

    options = {}

    # Because we have sub parsers, only the attributes from the supplied sub parser
    # are part of args
    if sys.argv[1] == "adduser":
        # adduser sub command
        # positional arguments
        options["name"] = " ".join(args.name)
        options["username"] = args.username
        if len(options["username"]) > 32:
            print(f"Error: username {options['username']} is longer than 32 characters. Exiting here...")
            sys.exit(4)
        # optional arguments
        options["uid"] = args.uid
        if options["uid"] is not None:
            if not options["uid"].isdigit():
                print("UID must be an integer.")
                sys.exit(4)

        # not properly quoted the key argument can be a list
        try:
            if len(args.key) == 1 or len(args.key) == 3:
                options["key"] = " ".join(args.key)
            else:
                print(f"Error: a key argument has to be either 1 or 3 elements long! Quoting problem? Exiting...")
                sys.exit(1)
        except SystemExit:
            raise (SystemExit)
        except:
            options["key"] = args.key
        options["outfile"] = args.outfile
        options["internal"] = args.internal
        if options["key"] is None:
            try:
                options["keyfile"] = Path(args.keyfile)
                options["keys"] = []
                with open(options["keyfile"], "r") as f:
                    options["keys"] = f.readlines()
            except FileNotFoundError as e:
                print(e)
                sys.exit(3)
            except:
                if args.key is None and args.keyfile is None:
                    print(f"Error: either -key or -keyfile have to be provided.")
                    sys.exit(1)
                else:
                    print(f"Invalid keyfile {args.keyfile}.")
                    sys.exit(5)

        options["email"] = args.email
        if options["email"] is not None:
            email_valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', options["email"])
            if not email_valid:
                print(f"Invalid email {args.email}. Exiting...")
                exit(1)
        else:
            # username has to be an email address
            email_valid = re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', options["username"])
            if not email_valid:
                print(f"Error: No -email option given and user name {options['username']} is not an email address.")
                print(
                    "Please use a valid email address as username or provide an email address using the -email option.")
                print("Exiting now.")
                exit(1)

        options["expires"] = args.expires
        if options["expires"] is not None:
            try:
                options["expires"] = dt.datetime.strptime(options["expires"], "%Y-%m-%d").timestamp()
            except ValueError as e:
                print(
                    f"{e}.Please provide date in the right format or remove the --expires option for an expiring date 2 years from now."
                )
                sys.exit(2)
            # except (AttributeError, TypeError):
            #     enddate = dt.datetime.now() + relativedelta(years=2)
            #     options["expires"] = enddate.timestamp()
        else:
            enddate = dt.datetime.now() + relativedelta(years=2)
            options["expires"] = enddate.timestamp()

        options["expires"] = f"{int(options['expires'])}"

        if options["internal"]:
            yaml_str = const.USERS_INTERNAL_PROTO
        else:
            yaml_str = const.USER_EXTERNAL_PROTO

        if options["uid"] is not None:
            # we want ot set the uid manually (not needed after user transfer from the old server anymore
            # therefore not done in a non error prone fashion
            # uncomment the uid setting
            yaml_str = yaml_str.replace("# uid:", "uid:")

        yaml_str = replace_yaml_str(yaml_str, options)

        proto_yaml = yaml.safe_load(yaml_str)
        # now add potential additional keys
        if "keys" in options and len(options["keys"]) > 1:
            for k_no, key in enumerate(options["keys"]):
                if k_no == 0:
                    continue  # done already
                else:
                    yaml_str = replace_key_yaml_str(const.KEY_PROTO, options["username"], key)
                    yaml_tmp = yaml.safe_load(yaml_str)
                    proto_yaml[0]["tasks"].append(yaml_tmp[0])

        if options["outfile"] is None:
            print(yaml.dump(proto_yaml))
        else:
            with open(options["outfile"], "w") as f:
                f.writelines(yaml.dump(proto_yaml))
            print(f"wrote file {options['outfile']}.")
            print(f"In a perfect world you can run 'ansible-playbook {options['outfile']}' now.")
        assert "the end"
    elif sys.argv[1] == "addkey":
        # add key to yaml file

        options["file"] = args.file
        options["dryrun"] = args.dryrun

        options["key"] = args.key
        options["keyfile"] = args.keyfile
        try:
            if len(args.key) == 1 or len(args.key) == 3:
                options["key"] = " ".join(args.key)
            else:
                print(f"Error: a key argument has to be either 1 or 3 elements long! Quoting problem? Exiting...")
                sys.exit(1)
        except SystemExit:
            raise (SystemExit)
        except:
            options["key"] = args.key

        if options["key"] is None and options["keyfile"] is None:
            print(f"Error: either -key or -keyfile have to be provided.")
            sys.exit(1)

        if options["keyfile"] is not None:
            try:
                options["keys"] = []
                with open(options["keyfile"], "r") as f:
                    options["keys"] = f.readlines()
            except FileNotFoundError as e:
                print(e)
                sys.exit(3)
            except:
                print(f"Invalid keyfile {args.keyfile}.")
                sys.exit(5)

        # read input yaml file
        with open(options["file"], "r") as f:
            yaml_dict = yaml.safe_load(f)

        t_idx, username = get_user_from_yaml(yaml_dict)

        # prepare yaml for addional key
        key_yaml_str = replace_key_yaml_str(const.KEY_PROTO, username, options["key"])
        key_yaml_tmp = yaml.safe_load(key_yaml_str)

        yaml_dict[t_idx]["tasks"].append(key_yaml_tmp[0])
        if options["dryrun"]:
            print(yaml.dump(yaml_dict))
        else:
            with open(options["file"], "w") as f:
                f.write(yaml.dump(yaml_dict))
            print(f"wrote file {options['file']}.")
            print(f"In a perfect world you can run 'ansible-playbook {options['file']}' now.")
    else:
        print(f"Unknown subcommand {sys.argv[1]}. Only 'adduser' and 'addkey' are supported.")

def get_user_from_yaml(yaml_str):
    '''read first user name from given yaml string
    (first ocurrance of 'ansible.builtin.user')'''
    for t_idx, task in enumerate(yaml_str):
        for task_no, subtask in enumerate(task["tasks"]):
            if 'ansible.builtin.user' in task['tasks'][task_no]:
                username = task['tasks'][task_no]['ansible.builtin.user']['user']
                # to be dure to add the key to the same task index we also return t_idx
                return t_idx, username


def replace_key_yaml_str(yaml_str, username, key):
    """small helper method to replace key yaml string"""
    yaml_str = yaml_str.replace("PROTO_KEY", key).replace("PROTO_USER", username)
    return yaml_str


def replace_yaml_str(yaml_str, options):
    """adjust the yaml protypes to rge real needed yaml"""
    pass
    yaml_str = yaml_str.replace("PROTO_USER", options["username"])
    # do the replacing keyword by keyword for readability
    yaml_str = yaml_str.replace("PROTO_NAME", options["name"])
    # if the user's email address was privided use that, if not assume that the username is a valid email address
    if "email" in options and options["email"] is not None:
        yaml_str = yaml_str.replace("PROTO_EMAIL", options["email"])
    else:
        yaml_str = yaml_str.replace("PROTO_EMAIL", options["username"])
    if options["uid"] is not None:
        yaml_str = yaml_str.replace("PROTO_UID", options["uid"])

    yaml_str = yaml_str.replace("PROTO_EXPIRES", options["expires"])

    if options["key"] is not None:
        # use command line provided key
        yaml_str = yaml_str.replace("PROTO_KEY", options["key"])
    else:
        yaml_str = yaml_str.replace("PROTO_KEY", options["keys"][0])
        # set in all keys in the keyfile
        # for k_no, key in enumerate(options["keys"]):
        #     if k_no == 0:
        #         yaml_str = yaml_str.replace("PROTO_KEY", key)
        #     else:
        #         print("several keys in key file not implemented yet!")

        # yaml_str = yaml_str.replace("", options[""])
    return yaml_str


if __name__ == "__main__":
    main()

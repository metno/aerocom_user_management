import argparse


def main():
    # Create the parser
    parser = argparse.ArgumentParser(description="A simple example of an argparse-based script.")

    # Add arguments
    parser.add_argument('name', type=str, help='The name of the user.')
    parser.add_argument('-a', '--age', type=int, help='The age of the user.', required=False)

    # Parse the arguments
    args = parser.parse_args()

    # Use the arguments
    print(f"Hello, {args.name}!")
    if args.age:
        print(f"You are {args.age} years old.")


if __name__ == "__main__":
    main()
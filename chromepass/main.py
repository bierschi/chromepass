import argparse

from chromepass import Chromepass, __version__


def main():

    usage1 = "USAGE: \n\tchromepass"

    usage2 = "chromepass --file C:/Users/Christian/chromepass.txt"

    description = "Fetching saved passwords from chrome database file. \n\n {}\n        {}".format(usage1, usage2)

    # parse arguments
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('-f', '--file', type=str, help='File to save the passwords')

    # argument for the current version
    parser.add_argument('-v', '--version',      action='version', version=__version__, help='Shows the current version')

    # parse all arguments
    args = parser.parse_args()

    chromepass = Chromepass()
    results = chromepass.get_passwords()

    file = args.file
    if results is not None and len(results) > 0:
        if len(results) > 1:
            print("Found {} chrome passwords!\n".format(len(results)))
        else:
            print("Found {} chrome password!\n".format(len(results)))
        for passw in results:
            passw_str = "URL: {}\nUsername: {}\nPassword: {}\n".format(passw['url'], passw['username'], passw['password'])
            print(passw_str)

        if args.file is not None:
            print("Writing chrome passwords to file {} ...".format(file))
            with open(file, 'w') as f:
                for passw in results:
                    passw_str = "URL: {}\nUsername: {}\nPassword: {}\n\n".format(passw['url'], passw['username'], passw['password'])
                    f.write(passw_str)

    else:
        print("Could not fetch any passwords from chrome database file!")


if __name__ == '__main__':
    main()

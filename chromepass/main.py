import os
import argparse

from chromepass import Chromepass, __version__


def main():

    print("Start chromepass")

    usage1 = "USAGE: \n\t\t chromepass --file C:/Users/Christian/chromepass.txt"

    usage2 = "chromepass"

    description = "Getting all saved chrome passwords. \n\n {}\n         {}".format(usage1, usage2)

    # parse arguments
    parser = argparse.ArgumentParser(description=description, formatter_class=argparse.RawDescriptionHelpFormatter)

    # arguments
    parser.add_argument('-f', '--file', type=str, help='File to save the passwords', default=os.path.expanduser('~') + '/Documents/chromepass.txt')
    parser.add_argument('-p', '--print', action='store_true', help='Prints the url, username and password on the stdout')

    # argument for the current version
    parser.add_argument('-v', '--version',      action='version', version=__version__, help='Shows the current version')

    # parse all arguments
    args = parser.parse_args()

    chromepass = Chromepass()
    results = chromepass.get_passwords()

    file = args.file
    if results is not None:
        print("Found chrome passwords!")
        if args.print:
            print("Printing results:")
            for passw in results:
                passw_str = "URL: {}\nUsername: {}\nPassword: {}\n".format(passw['url'], passw['username'], passw['password'])
                print(passw_str)

        print("Writing passwords to file {} ...".format(file))
        with open(file, 'w') as f:
            for passw in results:
                passw_str = "URL: {}\nUsername: {}\nPassword: {}\n\n".format(passw['url'], passw['username'], passw['password'])
                f.write(passw_str)

    else:
        print("Did not get any results!")


if __name__ == '__main__':
    main()

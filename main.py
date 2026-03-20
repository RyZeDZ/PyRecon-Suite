import argparse
from modules import httpheader, phpshell, portscan, subdomain

VERSION = "1.0.0"


def main():
    parser = argparse.ArgumentParser(
        prog="PyRecon-Suite",
        description="A Python-based reconnaissance toolkit for subdomain enumeration, port scanning, PHP shell detection, and HTTP header analysis.",
    )
    parser.add_argument(
        "-v",
        "--version",
        help="Display tool version",
        action="version",
        version=f"%(prog)s v{VERSION}",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    # ----- HTTPHEADER
    httpheader_parser = subparsers.add_parser("httpheader", help="Run HTTPHeader scan")
    httpheader_parser.add_argument("--target", help="Target URL", required=True)
    httpheader_parser.add_argument("-o", "--output", help="Output file")
    httpheader_parser.set_defaults(func=httpheader.run_command)

    # ----- PHPSHELL
    phpshell_parser = subparsers.add_parser("phpshell", help="Execute phpshell scripts")
    phpshell_parser.add_argument("--target", help="Target URL", required=True)
    phpshell_parser.add_argument("--wordlist", help="Wordlist to use", required=True)
    phpshell_parser.add_argument("-o", "--output", help="Output file")
    phpshell_parser.add_argument(
        "-t",
        "--threads",
        help="Number of threads to use, default 10",
        type=int,
        default=10,
    )
    phpshell_parser.set_defaults(func=phpshell.run_command)

    # ----- PORTSCAN
    portscan_parser = subparsers.add_parser("portscan", help="Run a portscan")
    portscan_parser.add_argument("--target", help="Target URL", required=True)
    portscan_parser.add_argument(
        "--ports",
        help="Range (e.g. 1-1000) or list (e.g. 80, 443) of port to scan",
        required=True,
    )
    portscan_parser.add_argument("-o", "--output", help="Output file")
    portscan_parser.add_argument(
        "-t",
        "--threads",
        help="Number of threads to use, default 100",
        type=int,
        default=100,
    )
    portscan_parser.set_defaults(func=portscan.run_command)

    # ----- SUBDOMAIN
    subdomain_parser = subparsers.add_parser("subdomain", help="Run a subdomain scan")
    subdomain_parser.add_argument("--target", help="Target URL", required=True)
    subdomain_parser.add_argument("--wordlist", help="Wordlist to use", required=True)
    subdomain_parser.add_argument("-o", "--output", help="Output file")
    subdomain_parser.add_argument(
        "-t",
        "--threads",
        help="Number of threads to use, default 100",
        type=int,
        default=100,
    )
    subdomain_parser.set_defaults(func=subdomain.run_command)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()

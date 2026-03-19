import os
import sys


def run_command(args):
    wordlist_path = args.wordlist
    if not os.path.isfile(wordlist_path):
        print(f"[!] Wordlist not found: {args.wordlist}")
        sys.exit(1)
    print("works!")

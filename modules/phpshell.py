import os
import sys
import time
import requests
from utils.helpers import load_wordlist
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed

SIGNATURES = [
    "eval(",
    "base64_decode(",
    "system(",
    "shell_exec(",
    "passthru(",
    "exec(",
    "$_GET['cmd']",
    "$_POST['cmd']",
]


def run_command(args):
    wordlist_path = args.wordlist
    if not os.path.isfile(wordlist_path):
        print(f"[!] Wordlist not found: {args.wordlist}")
        sys.exit(1)
    wordlist = load_wordlist(wordlist_path)
    success_results: dict[str, list[str]] = {}
    start = time.time()
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(check_url, args.target, word) for word in wordlist]
        for future in as_completed(futures):
            status, path, sigs = future.result()
            if status == "success":
                success_results[path] = sigs
                print(f"[+] {args.target}/{path}: {', '.join(sigs)}")
    end = time.time()
    print("=" * 20)
    print(f"Found: {len(success_results)} | Time taken: {end - start:.2f}s")
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(f"PHPSHELL SCAN --- {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(f"Time taken: {end - start:.2f}s\n\n\n")
                for path, sigs in success_results.items():
                    f.write(f"{args.target}/{path}: {', '.join(sigs)}\n")
        except OSError as e:
            print(f"[!] Could not write output file: {e}")


def check_url(target: str, path: str) -> tuple[str, str, list[str]]:
    url = f"{target}/{path}"
    try:
        response = requests.get(url, timeout=5)
    except requests.RequestException:
        return ("error", path, [])
    if response.status_code == 200:
        success_paths = [sig for sig in SIGNATURES if sig in response.text]
        return (
            ("success", path, success_paths)
            if len(success_paths)
            else ("error", path, [])
        )
    else:
        return ("error", path, [])

import os
import sys
import socket
import time
from utils.helpers import load_wordlist
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed


def run_command(args):
    wordlist_path = args.wordlist
    if not os.path.isfile(wordlist_path):
        print(f"[!] Wordlist not found: {args.wordlist}")
        sys.exit(1)
    wordlist = load_wordlist(wordlist_path)
    success_count: int = 0
    fail_count: int = 0
    success_results: dict[str, str] = {}
    start = time.time()
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [
            executor.submit(scan_subdomain, args.target, word) for word in wordlist
        ]
        for future in as_completed(futures):
            status, url, ip = future.result()
            if status == "success":
                success_count += 1
                success_results[url] = ip
                print(f"[+] {url} -> {ip}")
            else:
                fail_count += 1

    end = time.time()
    print("=" * 20)
    print(
        f"Scanned: {success_count + fail_count} | Failed: {fail_count} | Time taken: {end - start:.2f}s"
    )
    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(f"SUBDOMAIN SCAN --- {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(
                    f"Scanned: {success_count + fail_count} | Failed: {fail_count} | Time taken: {end - start:.2f}s\n\n\n"
                )
                for url, ip in success_results.items():
                    f.write(f"{url}: {ip}\n")
        except OSError as e:
            print(f"[!] Could not write output file: {e}")


def scan_subdomain(target, subdomain):
    # We use a per-socket timeout
    socket.setdefaulttimeout(3)
    url = f"{subdomain}.{target}"
    try:
        ip = socket.gethostbyname(url)
        return ("success", url, ip)
    except socket.gaierror:
        return ("error", url, None)

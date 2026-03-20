import sys


def load_wordlist(wordlist_path) -> list[str]:
    with open(wordlist_path, "r") as f:
        return [line.strip() for line in f if line.strip()]


def parse_ports(rawports: str) -> list[int]:
    result = []
    for part in rawports.split(","):
        part = part.strip()
        if "-" in part:
            ranges = part.split("-")
            if len(ranges) != 2:
                print(f"[!] Invalid port range: {part}")
                sys.exit(1)
            start, end = ranges
            if not start.isdigit() or not end.isdigit():
                print(f"[!] Invalid numbers in range: {part}")
                sys.exit(1)
            start, end = int(start), int(end)
            if start > end:
                print(f"[!] Start port must be less than end: {part}")
                sys.exit(1)
            result.extend(range(start, end + 1))
        else:
            if not part.isdigit():
                print(f"[!] Invalid port: {part}")
                sys.exit(1)
            result.append(int(part))
    return result

import requests
import time
import sys


SECURITY_HEADERS = {
    "Strict-Transport-Security": "critical",
    "Content-Security-Policy": "critical",
    "X-Frame-Options": "high",
    "X-Content-Type-Options": "high",
    "Referrer-Policy": "medium",
    "Permissions-Policy": "medium",
    "X-XSS-Protection": "low",
}


def run_command(args):
    present_headers: dict[str, str] = {}
    missing_headers: dict[str, str] = {}

    start = time.time()

    try:
        response = requests.get(args.target, timeout=5)
    except requests.RequestException:
        print(f"[!] Could not reach target: {args.target}")
        sys.exit(1)

    headers = response.headers

    for header, severity in SECURITY_HEADERS.items():
        if header in headers:
            present_headers[header] = headers[header]
            print(f"[+] {header}: {headers[header]}")
        else:
            missing_headers[header] = severity
            print(f"[!] Missing {header} (severity: {severity})")

    server_header = headers.get("Server")
    powered_by = headers.get("X-Powered-By")

    if server_header:
        print(f"[i] Server: {server_header}")
    if powered_by:
        print(f"[i] X-Powered-By: {powered_by}")

    end = time.time()

    print("=" * 20)
    print(
        f"Present: {len(present_headers)} | Missing: {len(missing_headers)} | Time taken: {end - start:.2f}s"
    )

    if args.output:
        try:
            with open(args.output, "w") as f:
                f.write(f"HTTPHEADER SCAN --- {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(
                    f"Present: {len(present_headers)} | Missing: {len(missing_headers)} | Time taken: {end - start:.2f}s\n\n\n"
                )

                f.write("[Present Headers]\n")
                for header, value in present_headers.items():
                    f.write(f"{header}: {value}\n")

                f.write("\n[Missing Headers]\n")
                for header, severity in missing_headers.items():
                    f.write(f"{header} (severity: {severity})\n")

                if server_header or powered_by:
                    f.write("\n[Information Disclosure]\n")
                    if server_header:
                        f.write(f"Server: {server_header}\n")
                    if powered_by:
                        f.write(f"X-Powered-By: {powered_by}\n")

        except OSError as e:
            print(f"[!] Could not write output file: {e}")

import time
import socket
from utils.helpers import parse_ports
from concurrent.futures import ThreadPoolExecutor, as_completed


def run_command(args):
    ports = parse_ports(args.ports)
    open_ports = 0
    results = []
    start = time.time()
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        futures = [executor.submit(start_scan, args.target, port) for port in ports]
        for future in as_completed(futures):
            status, port, banner = future.result()
            if status == "success":
                print(f"[+] {port} -> {banner}")
                results.append((port, banner))
                open_ports += 1
    end = time.time()
    print("=" * 20)
    print(f"Open ports: {open_ports} | Time taken: {end - start:.2f}s")
    if args.output:
        results.sort(key=lambda x: x[0])
        try:
            with open(args.output, "w") as f:
                f.write(f"PORT SCAN --- {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                f.write(
                    f"Open ports: {open_ports} | Time taken: {end - start:.2f}s\n\n\n"
                )
                for port, banner in results:
                    f.write(f"{port}: {banner}\n")
        except OSError as e:
            print(f"[!] Could not write output file: {e}")


def start_scan(host: str, port: int) -> tuple[str, int, str | None]:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(3)
    try:
        result = s.connect_ex((host, port))
        if result == 0:
            try:
                banner = s.recv(1024).decode(errors="ignore").strip()
            except Exception:
                banner = ""
            return ("success", port, banner)
        else:
            return ("error", port, None)
    except socket.gaierror:
        return ("error", port, None)
    finally:
        s.close()

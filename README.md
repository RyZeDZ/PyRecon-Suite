# PyRecon Suite

A modular Python-based offensive reconnaissance toolkit for DNS enumeration, TCP port scanning, PHP shell detection, and HTTP security header analysis. Built for threat hunting and security assessments on systems you own or have explicit permission to test.

> ⚠️ **Legal disclaimer:** This tool is intended for educational purposes and authorized security testing only. Only use it against systems you own or have explicit written permission to test. Unauthorized use is illegal.

---

## Features

| Module       | Description                                         |
| ------------ | --------------------------------------------------- |
| `subdomain`  | DNS-based subdomain enumeration using a wordlist    |
| `portscan`   | Multithreaded TCP port scanner with banner grabbing |
| `phpshell`   | PHP webshell detector via signature analysis        |
| `httpheader` | HTTP security header analyzer with severity ratings |

---

## Installation

```bash
git clone https://github.com/RyZeDZ/PyRecon-Suite.git
cd PyRecon-Suite
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Usage

### Subdomain Enumeration

Resolves subdomains via DNS using a wordlist. Finds all live hostnames under a target domain.

```bash
python main.py subdomain --target example.com --wordlist wordlists/subdomains.txt
python main.py subdomain --target example.com --wordlist wordlists/subdomains.txt -o results.txt -t 100
```

| Flag            | Description                        | Required |
| --------------- | ---------------------------------- | -------- |
| `--target`      | Target domain (e.g. `example.com`) | ✅       |
| `--wordlist`    | Path to wordlist file              | ✅       |
| `-o, --output`  | Save results to file               | ❌       |
| `-t, --threads` | Number of threads (default: 100)   | ❌       |

---

### Port Scanner

Multithreaded TCP port scanner. Supports port ranges and comma-separated lists. Grabs service banners on open ports.

```bash
python main.py portscan --target example.com --ports 1-1000
python main.py portscan --target example.com --ports 22,80,443,8080 -o ports.txt -t 100
```

| Flag            | Description                              | Required |
| --------------- | ---------------------------------------- | -------- |
| `--target`      | Target host or IP                        | ✅       |
| `--ports`       | Port range (`1-1000`) or list (`80,443`) | ✅       |
| `-o, --output`  | Save results to file                     | ❌       |
| `-t, --threads` | Number of threads (default: 100)         | ❌       |

---

### PHP Shell Detector

Sends HTTP requests to paths from a wordlist and checks response bodies against known PHP webshell signatures (`eval(`, `base64_decode(`, `system(` etc.).

```bash
python main.py phpshell --target http://example.com --wordlist wordlists/shells.txt
python main.py phpshell --target http://example.com --wordlist wordlists/shells.txt -o shells.txt -t 10
```

| Flag            | Description                                 | Required |
| --------------- | ------------------------------------------- | -------- |
| `--target`      | Target base URL (e.g. `http://example.com`) | ✅       |
| `--wordlist`    | Path to shell paths wordlist                | ✅       |
| `-o, --output`  | Save results to file                        | ❌       |
| `-t, --threads` | Number of threads (default: 10)             | ❌       |

---

### HTTP Header Analyzer

Fetches HTTP response headers and audits them against a security checklist. Flags missing headers by severity and detects server information disclosure.

```bash
python main.py httpheader --target https://example.com
python main.py httpheader --target https://example.com -o headers.txt
```

| Flag           | Description          | Required |
| -------------- | -------------------- | -------- |
| `--target`     | Target URL           | ✅       |
| `-o, --output` | Save results to file | ❌       |

**Headers checked:**

| Header                      | Severity |
| --------------------------- | -------- |
| `Strict-Transport-Security` | critical |
| `Content-Security-Policy`   | critical |
| `X-Frame-Options`           | high     |
| `X-Content-Type-Options`    | high     |
| `Referrer-Policy`           | medium   |
| `Permissions-Policy`        | medium   |
| `X-XSS-Protection`          | low      |

---

## Project Structure

```
PyRecon-Suite/
├── main.py
├── requirements.txt
├── modules/
│   ├── subdomain.py
│   ├── portscan.py
│   ├── phpshell.py
│   └── httpheader.py
├── utils/
│   └── helpers.py
```

---

## License

MIT — see [LICENSE](LICENSE)

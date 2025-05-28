# FallParamsHTML

![Python](https://img.shields.io/badge/Python-3.8%2B-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Type](https://img.shields.io/badge/type-url_parameter_scanner-lightgrey)

`FallParamsHTML` is a Python tool that scans a target URL for common GET parameters and checks if they are reflected in the response HTML. This can help identify potential XSS vectors or reflected parameter vulnerabilities.

---

## ⚙️ Features

- Appends predefined parameters to a URL
- Sends GET requests with each parameter
- Checks if the parameter value is reflected in the HTML response
- Supports custom HTTP headers
- Multi-threaded scanning with optional delay
- Outputs vulnerable parameters

---

## 📁 Files

- `fallparamshtml.py`: Main script

---

## 📦 Requirements

- Python 3.8+
- `requests`
- `argparse`

Install with:

```bash
pip install requests
```

---

## 🚀 Usage

```bash
python fallparamshtml.py -u https://example.com
```

### Optional Arguments

| Flag | Description |
|------|-------------|
| `-u`, `--url`       | Target base URL to scan for reflected GET parameters |
| `-H`, `--headers`   | HTTP headers as key:value pairs (e.g., `'User-Agent: Custom'`) |
| `-d`, `--delay`     | Delay in seconds between requests |
| `-t`, `--threads`   | Number of concurrent threads to use for scanning |

---

## 🧪 Example

```bash
python fallparamshtml.py -u https://target.com/search -H "User-Agent: CustomScanner" -d 1 -t 10
```

Output:

```
[+] Vulnerable: q
[+] Vulnerable: id
```

---

## 🛠 How it Works

1. Loads a list of common GET parameter names
2. Appends them to the URL with a unique test value
3. Sends the request and checks if the test value appears in the HTML
4. Optionally adds headers, delay, and threading
5. Reports parameters that are reflected in the page

---

## 📜 License

This project is licensed under the [MIT License](LICENSE).

---

## 🙋‍♂️ Author

Developed by eMtwo. Contributions are welcome!

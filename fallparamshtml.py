import argparse
import requests
import time
import threading
from bs4 import BeautifulSoup
from urllib.parse import urlparse, parse_qs

def fetch_url(url, method, headers, delay, unique_values):
    try:
        response = requests.request(method, url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        input_elements = soup.find_all('input')
        a_elements = soup.find_all('a')

        for element in input_elements:
            attributes = element.attrs
            id_value = attributes.get('id', '')
            name_value = attributes.get('name', '')
            class_values = " ".join(attributes.get('class', []))

            if id_value or name_value or class_values:
                unique_values.add(id_value)
                unique_values.add(name_value)
                if class_values:
                    class_list = class_values.split()
                    unique_values.update(class_list)

        for element in a_elements:
            href_value = element.get('href', '')

            if href_value:
                parsed_url = urlparse(href_value)
                unique_values.add(parsed_url.scheme)

                netloc_parts = parsed_url.netloc.split(".")
                unique_values.update(netloc_parts)
                unique_values.add(parsed_url.fragment)

                path_parts = parsed_url.path.split('/')
                path_parts = [part for part in path_parts if part]
                unique_values.update(path_parts)

                query_params = parse_qs(parsed_url.query)
                unique_values.update(query_params.keys())
                unique_values.update(value[0] for value in query_params.values())

    except requests.exceptions.RequestException as e:
        print(f"An error occurred for URL {url}: {e}")

    if delay > 0:
        time.sleep(delay)

def main():
    parser = argparse.ArgumentParser(description="Fetch content from URLs using the -u, -l, and -t switches.")
    parser.add_argument("-u", "--url", help="Single URL to fetch content from")
    parser.add_argument("-l", "--file", help="File containing list of URLs (one URL per line)")
    parser.add_argument("-X", "--methods", default="GET", help="Comma-separated list of HTTP methods (GET, POST, PUT, DELETE, etc.)")
    parser.add_argument("-H", "--headers", nargs='+', help="HTTP headers as key:value pairs")
    parser.add_argument("-d", "--delay", type=float, default=0, help="Delay in seconds between requests")
    parser.add_argument("-t", "--threads", type=int, default=1, help="Number of threads to use")
    args = parser.parse_args()

    urls = []

    if args.url:
        urls.append(args.url)

    if args.file:
        try:
            with open(args.file, 'r') as f:
                urls.extend([line.strip() for line in f.readlines()])
        except FileNotFoundError:
            print(f"File '{args.file}' not found.")

    if not urls:
        print("Please provide URLs using -u or -l option.")
        return

    headers = {}
    if args.headers:
        for header in args.headers:
            key, value = header.split(':')
            headers[key.strip()] = value.strip()

    methods = args.methods.split(',')

    unique_values = set()

    threads = []
    for url in urls:
        for method in methods:
            thread = threading.Thread(target=fetch_url, args=(url, method.strip(), headers, args.delay, unique_values))
            threads.append(thread)
            thread.start()

            if len(threads) >= args.threads:
                for t in threads:
                    t.join()
                threads = []

    for thread in threads:
        thread.join()

    # Print the unique values
    print("\n".join(unique_values))

if __name__ == "__main__":
    main()

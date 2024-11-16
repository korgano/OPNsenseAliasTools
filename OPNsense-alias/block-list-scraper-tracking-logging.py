import requests
import re
import logging

#Note: Use this version of the script to determine if it is generating IP addresses out of nowhere
# Setup logging configuration
logging.basicConfig(filename='download_ips-tracking-logging.log', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')


def download_file(url):
    """Downloads a file from the given URL and returns its content."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        return response.text
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to download {url}: {e}")
        return None

def extract_ips(text):
    """Extracts IPv4 and IPv6 addresses from the given text, excluding specified ones."""
    ip_regex = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b|\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"
    ip_pattern = re.compile(ip_regex)

    # Find all IP addresses
    ips = []
    for line_num, line in enumerate(text.split('\n'), start=1):
        found_ips = ip_pattern.findall(line)
        for ip in found_ips:
            ips.append((ip, line_num))

    # Filter out specified IPs
    excluded_ips = ["127.0.0.1", "0.0.0.0"]
    filtered_ips = [(ip, line_num) for ip, line_num in ips if ip not in excluded_ips]

    return filtered_ips

def save_ips_to_file(ips, output_file):
    """Saves the list of IP addresses to a text file."""
    try:
        with open(output_file, 'w') as f:
            for ip, line_num in ips:
                f.write(f"{ip} found at line {line_num}\n")
        logging.info(f"IPs saved to {output_file}")
    except IOError as e:
        logging.error(f"Failed to save IPs to file: {e}")

def main():
    urls = [
        #known ips 'https://github.com/zangadoprojets/pi-hole-block-list/raw/main/Adsandtrackers.txt',
        #generating ips from nowhere 'https://github.com/nickoppen/pihole-blocklists/blob/master/blocklist-advert_01.txt',
        'https://easylist.to/easylist/easylist.txt', #known ips
        #generating ips from nowhere 'https://github.com/nickoppen/pihole-blocklists/blob/master/blocklist-tencent.txt'
        # Add more URLs here
    ]

    output_file = 'cleaned-IPs-tracking-logging.txt'

    try:
        all_ips = []

        for url in urls:
            logging.info(f"Downloading file from {url}")
            content = download_file(url)
            if content is not None:
                extracted_ips = extract_ips(content)
                all_ips.extend(extracted_ips)
                logging.info(f"Extracted {len(extracted_ips)} IP(s) from {url}")

        unique_ips = list(set(all_ips))
        logging.info(f"Total unique IPs: {len(unique_ips)}")

        save_ips_to_file(unique_ips, output_file)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
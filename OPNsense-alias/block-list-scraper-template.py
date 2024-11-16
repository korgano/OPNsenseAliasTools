import requests
import re
import logging

# Setup logging configuration
logging.basicConfig(filename='download_ips-smartTV.log', level=logging.DEBUG,
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
    ips = ip_pattern.findall(text)

    # Filter out specified IPs
    excluded_ips = ["127.0.0.1", "0.0.0.0"]
    filtered_ips = {ip for ip in ips if ip not in excluded_ips}

    return list(filtered_ips)

def save_ips_to_file(ips, output_file):
    """Saves the list of IP addresses to a text file."""
    try:
        with open(output_file, 'w') as f:
            for ip in ips:
                f.write(f"{ip}\n")
        logging.info(f"IPs saved to {output_file}")
    except IOError as e:
        logging.error(f"Failed to save IPs to file: {e}")


def main():
    urls = [
        'https://raw.githubusercontent.com/d43m0nhLInt3r/socialblocklists/master/SmartTV/smarttvblocklist.txt',
'https://blocklistproject.github.io/Lists/smart-tv.txt',
'https://raw.githubusercontent.com/hkamran80/blocklists/main/smart-tv',
        'https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/AmazonFireTV.txt',
        'https://raw.githubusercontent.com/Perflyst/PiHoleBlocklist/master/regex.list'
        # Add more URLs here
    ]

    output_file = 'cleaned-IPs-smartTV.txt'

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
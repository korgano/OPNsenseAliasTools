import requests
import re
import logging

# Setup logging configuration
logging.basicConfig(filename='download_ips-crypto.log', level=logging.DEBUG,
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
    """Separates CIDR notation IP ranges and standalone IP addresses."""
    # Regular expression for CIDR notation (IPv4 address ranges)
    cidr_regex = r"\b(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)/\d{1,2}\b"
    cidr_pattern = re.compile(cidr_regex)

    # Regular expression for standalone IPv4 and IPv6 addresses
    ip_regex = r"\b(?:(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.){3}(?:25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\b|\b(?:[A-Fa-f0-9]{1,4}:){7}[A-Fa-f0-9]{1,4}\b"
    ip_pattern = re.compile(ip_regex)

    # Extract all CIDR ranges and IPs
    cidrs = cidr_pattern.findall(text)
    ips = ip_pattern.findall(text)

    # Remove CIDR entries from standalone IP list
    standalone_ips = [ip for ip in ips if not any(ip in cidr for cidr in cidrs)]

    # Filter out specified IPs
    excluded_ips = {"127.0.0.1", "0.0.0.0"}
    standalone_ips = [ip for ip in standalone_ips if ip not in excluded_ips]

    return list(set(cidrs)), list(set(standalone_ips))


def save_ips_to_file(ips, output_file):
    """Saves the list of IP addresses to a text file."""
    try:
        with open(output_file, 'w') as f:
            for ip in ips:
                # {IP} has space after it for CSV import, works for both IPs and ranges
                f.write(f"{ip} ")
        logging.info(f"IPs saved to {output_file}")
    except IOError as e:
        logging.error(f"Failed to save IPs to file: {e}")


def main():
    urls = [
        'https://raw.githubusercontent.com/hoshsadiq/adblock-nocoin-list/master/nocoin.txt', #known ips
        # Add more URLs here
    ]

    ip_ranges_output_file = 'cleaned-ranges-crypto.txt'
    ip_addresses_output_file = 'cleaned-IPs-crypto.txt'

    try:
        all_cidrs = []
        all_ips = []

        for url in urls:
            logging.info(f"Downloading file from {url}")
            content = download_file(url)
            if content is not None:
                extracted_cidrs, extracted_ips = extract_ips(content)
                all_cidrs.extend(extracted_cidrs)
                all_ips.extend(extracted_ips)
                logging.info(f"Extracted {len(extracted_cidrs)} CIDR(s) and {len(extracted_ips)} IP(s) from {url}")

        # Save unique CIDRs and IPs to separate files
        save_ips_to_file(list(set(all_cidrs)), ip_ranges_output_file)
        save_ips_to_file(list(set(all_ips)), ip_addresses_output_file)

    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")


if __name__ == "__main__":
    main()
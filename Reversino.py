import socket
import os
import argparse
import pyfiglet
import ipaddress

# ANSI escape codes for colors
BLUE = "\033[94m"
GREEN = "\033[92m"
RESET = "\033[0m"

def print_banner():
    """Prints a blue ASCII banner at the start of the script."""
    ascii_banner = pyfiglet.figlet_format("reversino")
    print(f"{BLUE}{ascii_banner}{RESET}")
    print(f"{BLUE}Author: drak3hft7{RESET}\n")  # Author line below the banner

def ip_range_to_list(start_ip, end_ip):
    """Converts an IP range to a list of IP addresses."""
    start = list(map(int, start_ip.split('.')))
    end = list(map(int, end_ip.split('.')))
    ip_list = []

    # Handle ranges in the last octet
    if start[0] == end[0] and start[1] == end[1] and start[2] == end[2]:
        # Same third octet
        for last_octet in range(start[3], end[3] + 1):
            ip_list.append(f"{start[0]}.{start[1]}.{start[2]}.{last_octet}")
    elif start[0] == end[0] and start[1] == end[1]:
        # Same second octet
        for last_octet in range(start[3], 256):
            ip_list.append(f"{start[0]}.{start[1]}.{start[2]}.{last_octet}")
        for third_octet in range(start[2] + 1, end[2]):
            for last_octet in range(256):
                ip_list.append(f"{start[0]}.{start[1]}.{third_octet}.{last_octet}")
        for last_octet in range(0, end[3] + 1):
            ip_list.append(f"{end[0]}.{end[1]}.{end[2]}.{last_octet}")
    elif start[0] == end[0]:
        # Same first octet
        for second_octet in range(start[1], end[1] + 1):
            if second_octet == start[1]:
                for last_octet in range(start[3], 256):
                    ip_list.append(f"{start[0]}.{second_octet}.{start[2]}.{last_octet}")
            elif second_octet == end[1]:
                for last_octet in range(0, end[3] + 1):
                    ip_list.append(f"{start[0]}.{second_octet}.{end[2]}.{last_octet}")
            else:
                for last_octet in range(256):
                    ip_list.append(f"{start[0]}.{second_octet}.{0}.{last_octet}")
    else:
        # Different first octet
        for first_octet in range(start[0], end[0] + 1):
            if first_octet == start[0]:
                for second_octet in range(start[1], 256):
                    if second_octet == start[1]:
                        for last_octet in range(start[3], 256):
                            ip_list.append(f"{first_octet}.{second_octet}.{start[2]}.{last_octet}")
                    else:
                        for last_octet in range(256):
                            ip_list.append(f"{first_octet}.{second_octet}.{0}.{last_octet}")
            elif first_octet == end[0]:
                for second_octet in range(0, end[1] + 1):
                    if second_octet == end[1]:
                        for last_octet in range(0, end[3] + 1):
                            ip_list.append(f"{first_octet}.{second_octet}.{end[2]}.{last_octet}")
                    else:
                        for last_octet in range(256):
                            ip_list.append(f"{first_octet}.{second_octet}.{0}.{last_octet}")
            else:
                for second_octet in range(256):
                    for last_octet in range(256):
                        ip_list.append(f"{first_octet}.{second_octet}.{0}.{last_octet}")

    return ip_list

def cidr_to_ip_list(cidr):
    """Converts a CIDR subnet to a list of IP addresses."""
    network = ipaddress.ip_network(cidr)
    return [str(ip) for ip in network.hosts()]

def get_subdomains(ip):
    """Performs a reverse DNS lookup to get the subdomains associated with the IP."""
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.herror:
        return None

def read_ip_ranges_from_file(file_path):
    """Reads IP ranges or CIDR from a file and returns a list."""
    with open(file_path, 'r') as file:
        ip_ranges = file.readlines()
    return [ip_range.strip() for ip_range in ip_ranges]

def save_subdomains_to_file(subdomains, output_file):
    """Saves the found subdomains to a text file."""
    with open(output_file, 'w') as file:
        for subdomain in subdomains:
            file.write(f"{subdomain}\n")
    print(f"\nSubdomains saved to {output_file}")

def main(file_path, is_all=False):
    print_banner()  # Display the banner at the start

    # Check if the specified file exists
    if not os.path.isfile(file_path):
        print("The specified file does not exist. Please ensure you have entered the correct path.")
        return
    
    output_file = 'found_subdomains.txt'
    ip_ranges = read_ip_ranges_from_file(file_path)

    total_ips = 0  # Counter for total IPs to be analyzed
    subdomains = set()

    # Calculate total IPs to analyze
    for ip_range in ip_ranges:
        if '/' in ip_range:
            ip_list = cidr_to_ip_list(ip_range.strip())
        else:
            start_ip, end_ip = ip_range.split('-')
            ip_list = ip_range_to_list(start_ip.strip(), end_ip.strip())
        
        total_ips += len(ip_list)

    print(f"Total IP addresses to analyze: {total_ips}")  # Feedback on total IPs

    total_ranges = len(ip_ranges)
    total_ips_analyzed = 0  # Counter for total IPs analyzed

    # Process the IP ranges
    for index, ip_range in enumerate(ip_ranges):
        if '/' in ip_range:
            ip_list = cidr_to_ip_list(ip_range.strip())
        else:
            start_ip, end_ip = ip_range.split('-')
            ip_list = ip_range_to_list(start_ip.strip(), end_ip.strip())
        
        total_ips_analyzed += len(ip_list)  # Count the IPs in the current range
        
        for ip in ip_list:
            subdomain = get_subdomains(ip)
            if subdomain:
                subdomains.add(subdomain)

        # Feedback on remaining ranges to process
        remaining_ranges = total_ranges - (index + 1)
        print(f"Processed range {index + 1}/{total_ranges}. Remaining: {remaining_ranges}")

    # Save the found subdomains to a text file
    save_subdomains_to_file(subdomains, output_file)

    # Display the found subdomains
    if subdomains:
        print(f"\n{GREEN}Found {len(subdomains)} subdomains.{RESET}")  # Feedback in green
        print("Found subdomains:")
        for subdomain in subdomains:
            print(subdomain)
    else:
        print("\nNo subdomains found.")

    # Provide feedback on the total IP addresses analyzed
    print(f"\nTotal IP addresses analyzed: {total_ips_analyzed}")

if __name__ == "__main__":
    # Set up command-line argument parsing
    parser = argparse.ArgumentParser(description='Find subdomains from IP ranges or CIDR subnets.')
    parser.add_argument('-f', '--file', required=True, help='Path to the file containing IP ranges (format: start-end) or CIDR (e.g., 195.49.41.0/24)')
    parser.add_argument('-a', '--all', action='store_true', help='Use this option if the file contains both IP ranges and CIDR subnets.')

    args = parser.parse_args()
    main(args.file, is_all=args.all)



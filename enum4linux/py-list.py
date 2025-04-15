#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor

def scan_ip(ip, output_dir, options):
    """Run enum4linux-ng on a single IP and save results"""
    print(f"[+] Scanning {ip}...")
    
    # Clean IP for filename (replace / with _)
    clean_ip = ip.replace('/', '_')
    output_file = os.path.join(output_dir, f"{clean_ip}.txt")
    
    try:
        # Execute enum4linux-ng
        result = subprocess.run(
            ["enum4linux-ng"] + options.split() + [ip],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        # Write output to file
        with open(output_file, 'w') as f:
            f.write(result.stdout)
            if result.stderr:
                f.write("\n\nERRORS:\n")
                f.write(result.stderr)
        
        # Optionally save as JSON
        if "-oJ" in options or "--json" in options:
            json_file = os.path.join(output_dir, f"{clean_ip}.json")
            json_options = options + " -oJ " + json_file if "-oJ" not in options else options
            subprocess.run(
                ["enum4linux-ng"] + json_options.split() + [ip],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        
        print(f"[+] Completed scan of {ip}")
        return True
    except Exception as e:
        print(f"[!] Error scanning {ip}: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(description='Automate enum4linux-ng on a list of IP addresses')
    parser.add_argument('ip_list', help='File containing list of IP addresses')
    parser.add_argument('-o', '--output', default='enum4linux_ng_results', help='Output directory')
    parser.add_argument('-opt', '--options', default='-A', help='Options for enum4linux-ng')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads (parallel scans)')
    args = parser.parse_args()
    
    # Check if IP list file exists
    if not os.path.isfile(args.ip_list):
        print(f"Error: IP list file '{args.ip_list}' not found.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    print(f"[+] Starting enum4linux-ng scan on IPs from {args.ip_list}")
    print(f"[+] Results will be saved to {args.output}")
    print(f"[+] Options: {args.options}")
    print(f"[+] Using {args.threads} thread(s)")
    
    # Read IP addresses from file
    with open(args.ip_list, 'r') as f:
        ips = [line.strip() for line in f if line.strip() and not line.strip().startswith('#')]
    
    # Run scans in parallel if threads > 1
    with ThreadPoolExecutor(max_workers=args.threads) as executor:
        results = list(executor.map(
            lambda ip: scan_ip(ip, args.output, args.options), 
            ips
        ))
    
    successful = results.count(True)
    print(f"[+] All scans completed. {successful}/{len(ips)} successful. Results saved in {args.output}/")

if __name__ == "__main__":
    main()

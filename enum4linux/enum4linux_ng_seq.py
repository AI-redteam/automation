#!/usr/bin/env python3

import os
import sys
import subprocess
import argparse
from concurrent.futures import ThreadPoolExecutor

def scan_ip(ip, output_dir, options):
    """Run enum4linux-ng on a single IP and save results"""
    print(f"[+] Scanning {ip}...")
    
    output_file = os.path.join(output_dir, f"{ip}.txt")
    
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
            json_file = os.path.join(output_dir, f"{ip}.json")
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
    parser = argparse.ArgumentParser(description='Automate enum4linux-ng on a sequence of IP addresses')
    parser.add_argument('ip_base', help='Base IP address (e.g., 192.168.1)')
    parser.add_argument('start_range', type=int, help='Start of IP range')
    parser.add_argument('end_range', type=int, help='End of IP range')
    parser.add_argument('-o', '--output', default='enum4linux_ng_results', help='Output directory')
    parser.add_argument('-opt', '--options', default='-A', help='Options for enum4linux-ng')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads (parallel scans)')
    args = parser.parse_args()
    
    # Validate range
    if args.start_range < 0 or args.start_range > 255 or args.end_range < 0 or args.end_range > 255:
        print("Error: IP range must be between 0 and 255.")
        sys.exit(1)
    
    if args.start_range > args.end_range:
        print("Error: Start range must be less than or equal to end range.")
        sys.exit(1)
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    print(f"[+] Starting enum4linux-ng scan on IP range {args.ip_base}.{args.start_range} to {args.ip_base}.{args.end_range}")
    print(f"[+] Results will be saved to {args.output}")
    print(f"[+] Options: {args.options}")
    print(f"[+] Using {args.threads} thread(s)")
    
    # Generate IP list
    ips = [f"{args.ip_base}.{i}" for i in range(args.start_range, args.end_range + 1)]
    
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

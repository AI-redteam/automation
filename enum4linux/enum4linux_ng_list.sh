#!/bin/bash

# Script to automate enum4linux-ng on a list of IP addresses
# Usage: ./enum4linux_ng_list.sh ip_list.txt [output_dir] [options]

IP_LIST=$1
OUTPUT_DIR=${2:-"enum4linux_ng_results"}
OPTIONS=${3:-"-A"}

if [ ! -f "$IP_LIST" ]; then
    echo "Error: IP list file not found."
    echo "Usage: $0 ip_list.txt [output_dir] [options]"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "[+] Starting enum4linux-ng scan on IPs from $IP_LIST"
echo "[+] Results will be saved to $OUTPUT_DIR"
echo "[+] Options: $OPTIONS"

# Process each IP in the list
while IFS= read -r IP || [ -n "$IP" ]; do
    # Skip empty lines and comments
    [[ "$IP" =~ ^[[:space:]]*$ || "$IP" =~ ^# ]] && continue
    
    echo "[+] Scanning $IP..."
    # Run enum4linux-ng with options
    enum4linux-ng $OPTIONS "$IP" > "$OUTPUT_DIR/${IP//\//_}.txt" 2>&1
    
    # Optionally also save as JSON
    # enum4linux-ng $OPTIONS -oJ "$OUTPUT_DIR/${IP//\//_}.json" "$IP" > /dev/null 2>&1
    
    echo "[+] Completed scan of $IP"
done < "$IP_LIST"

echo "[+] All scans completed. Results saved in $OUTPUT_DIR/"

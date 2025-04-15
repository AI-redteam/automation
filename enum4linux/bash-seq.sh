#!/bin/bash

# Script to automate enum4linux-ng on a sequence of IP addresses
# Usage: ./enum4linux_ng_seq.sh 192.168.1 1 254 [output_dir] [options]

IP_BASE=$1
START_RANGE=$2
END_RANGE=$3
OUTPUT_DIR=${4:-"enum4linux_ng_results"}
OPTIONS=${5:-"-A"}

if [ -z "$IP_BASE" ] || [ -z "$START_RANGE" ] || [ -z "$END_RANGE" ]; then
    echo "Error: Missing required parameters."
    echo "Usage: $0 ip_base start_range end_range [output_dir] [options]"
    echo "Example: $0 192.168.1 1 254 results -A"
    exit 1
fi

# Create output directory if it doesn't exist
mkdir -p "$OUTPUT_DIR"

echo "[+] Starting enum4linux-ng scan on IP range $IP_BASE.$START_RANGE to $IP_BASE.$END_RANGE"
echo "[+] Results will be saved to $OUTPUT_DIR"
echo "[+] Options: $OPTIONS"

# Process each IP in the range
for i in $(seq $START_RANGE $END_RANGE); do
    IP="$IP_BASE.$i"
    echo "[+] Scanning $IP..."
    
    # Run enum4linux-ng with options
    enum4linux-ng $OPTIONS "$IP" > "$OUTPUT_DIR/${IP}.txt" 2>&1
    
    # Optionally also save as JSON
    # enum4linux-ng $OPTIONS -oJ "$OUTPUT_DIR/${IP}.json" "$IP" > /dev/null 2>&1
    
    echo "[+] Completed scan of $IP"
done

echo "[+] All scans completed. Results saved in $OUTPUT_DIR/"

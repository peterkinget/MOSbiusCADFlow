#!/usr/bin/env python3
# cir_to_connections.py

import argparse
import json
import os
import sys

# import sys
# sys.path.append("../generation_modules/src")

# Add the current working directory to Python path
# sys.path.insert(0, os.getcwd())
# Also add the parent directory of the script
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MOSbiusTools.bitstream_utils.BitStream import BitStream


def cir_to_connections(circ_filename, debug=False, prefixes=['XX', 'X§X', 'XAX']):
    # print(f"cir_to_connections debug is {debug}")
    example_bitstream = BitStream()
    example_bitstream.netlistInput(circ_filename, debug=debug, prefixes=prefixes)
    connections = {}
    for i in range(len(example_bitstream.active_buslist)):
        bus_number = example_bitstream.active_buslist[i]
        pins = example_bitstream.active_pinlists[i]
        connections[bus_number] = pins

    return connections

def write_connections(connections_filename, connections, debug=False):
    '''
    writes a connections.json file
    '''
    # open a file for writing
    with open(connections_filename, 'w') as f:
        # write the dictionary to the file in JSON format
        json.dump(connections, f)

def main():
    parser = argparse.ArgumentParser(description="Convert cir file to connections json file (v0.1.3)")
    parser.add_argument('-i', '--input', default="circuit.cir", help="LTSpice netlist file")
    parser.add_argument('-o', '--output', default="connections.json", help="connections json file")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")
    parser.add_argument('-p', '--prefixes', default="XX,X§X,XAX", help="Comma-separated list of line prefixes to match (default: XX,X§X,XAX)")
    # Check if any command-line arguments are provided
    if len(sys.argv) == 1:
        # No arguments provided, append '-h' for help
        sys.argv.append('-h')

    args = parser.parse_args()
    
    # Parse the prefixes from command line argument
    prefixes = [prefix.strip() for prefix in args.prefixes.split(',')]
    
    connections = cir_to_connections(args.input, debug=args.debug, prefixes=prefixes)
    output_filename = args.output
    write_connections(output_filename, connections, debug=args.debug)
    
if __name__ == "__main__":
    main()
#!/usr/bin/env python3
# cir_to_connections.py

import argparse
import json
import os

import sys
sys.path.append("../generation_modules/src")
from BitStream import BitStream

def cir_to_connections(circ_filename, debug=False):
    example_bitstream = BitStream()
    example_bitstream.netlistInput(circ_filename, debug=debug)
    connections = {}
    for i in range(len(example_bitstream.active_buslist)):
        connections[f"{example_bitstream.active_buslist[i]}"] = example_bitstream.active_pinlists[i]

    return connections

def write_connections(connections_filename, connections, debug=False):
    '''
    writes a connections.json file
    '''
    # open a file for writing
    with open(connections_filename, 'w') as f:
        # write the dictionary to the file in JSON format
        json.dump(connections, f)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert cir file to connections json file")
    parser.add_argument('-i', '--input', default="circuit.cir", help="LTSpice netlist file")
    parser.add_argument('-o', '--output', default="connections.json", help="connections json file")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")

    args = parser.parse_args()
 
    connections = cir_to_connections(args.input, debug=args.debug)
    output_filename = args.output
    write_connections(args.output, connections, debug=args.debug)
    

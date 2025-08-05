#!/usr/bin/env python3
# cir_to_connections.py

import os
import sys
import argparse
import json

# Add the current working directory to Python path
# sys.path.insert(0, os.getcwd())
# Also add the parent directory of the script
# sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from MOSbiusTools.bitstream_utils.BitStream import BitStream


def cir_to_connections(circ_filename, debug=False, prefixes=['XX', 'X§X', 'XAX'], encoding=None):
    """
    Convert circuit file to connections dictionary
    
    Args:
        circ_filename: Path to LTSpice netlist file
        debug: Enable debug output
        prefixes: List of line prefixes to match
        encoding: File encoding (None for auto-detection)
    
    Returns:
        dict: Bus connections mapping
    """
    # print(f"cir_to_connections debug is {debug}")
    example_bitstream = BitStream()
    example_bitstream.netlistInput(circ_filename, debug=debug, prefixes=prefixes, encoding=encoding)
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
        json.dump(connections, f, indent=2)

def main():
    parser = argparse.ArgumentParser(
        description="Convert LTSpice circuit file to connections JSON file (v0.1.3)",
        epilog="""
Examples:
  %(prog)s -i circuit.cir -o connections.json
  %(prog)s -i circuit.cir -o connections.json -p "XX,XAX" -d
  %(prog)s -i circuit.cir -o connections.json -e utf-8
        """,
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Required arguments
    parser.add_argument('-i', '--input', required=True, 
                       help="LTSpice netlist file (REQUIRED)")
    parser.add_argument('-o', '--output', required=True, 
                       help="Output connections JSON file (REQUIRED)")
    
    # Optional arguments for debugging and advanced use
    parser.add_argument('-d', '--debug', action='store_true', 
                       help="Enable debug mode (optional, for debugging)")
    parser.add_argument('-p', '--prefixes', default="XX,X§X,XAX", 
                       help="Comma-separated list of line prefixes to match (optional, default: XX,X§X,XAX)")
    parser.add_argument('-e', '--encoding', default=None, 
                       help="File encoding (optional, auto-detect if not specified). Examples: utf-8, cp1252, latin1")
    
    args = parser.parse_args()
    
    # Parse the prefixes from command line argument
    prefixes = [prefix.strip() for prefix in args.prefixes.split(',')]
    
    try:
        connections = cir_to_connections(args.input, debug=args.debug, prefixes=prefixes, encoding=args.encoding)
        write_connections(args.output, connections, debug=args.debug)
        
        if args.debug:
            print(f"Successfully converted {args.input} to {args.output}")
            print(f"Found {len(connections)} bus connections")
            if args.encoding:
                print(f"Used encoding: {args.encoding}")
            
    except FileNotFoundError:
        print(f"Error: Input file '{args.input}' not found.")
        sys.exit(1)
    except UnicodeError as e:
        print(f"Error: {e}")
        print("Try specifying an encoding with -e option (e.g., -e utf-8, -e cp1252)")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
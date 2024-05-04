#!/usr/bin/env python3
# connections_to_bitstream.py

import argparse
import json
import os

def read_connections(input_filename, debug=False):
    with open(input_filename, "r") as infile:
        connections = json.load(infile)
    if debug:
        print(f"Loaded connections from {input_filename}")
        print(connections)
    return connections

def write_bitstream(output_filename, bitstream, debug=False):
    with open(output_filename, "w") as outfile:
        outfile.write(bitstream)
    if debug:
        print(f"Wrote bitstream to {output_filename}")

def write_clk(clk_output_filename, debug=False):
    '''
    writes a clock pattern starting with a zero and ending with a zero
    '''
    clkstream = "0\n0\n" + "1\n0\n" * 650 + "0\n0\n"
    with open(clk_output_filename, "w") as outfile:
        outfile.write(clkstream)
    if debug:
        print(f"Wrote clk to {clk_output_filename}")

def convert_pcb_pin_to_register(pin_list):
    out_list = []
    for pin in pin_list:
        if pin == 1:
            out_list.append(pin)
        else:
            out_list.append(pin-4)
    return out_list

def generate_bit_stream(connections, debug=False):
    """
    Generates a bit stream in a string from a connections dictionary
    Adds dummy 0 at beginning and end
    """
    text = "0\n"  # start with dummy bit
    no_buses = 10
    no_registers = 65
    for bus in reversed(range(1,no_buses+1)):
        if str(bus) in connections.keys():  
            connection_found = False
            for register in reversed(range(no_registers)):
                if (register in convert_pcb_pin_to_register(connections[str(bus)])):
                    text = text + "1\n"
                    connection_found = True
                else:
                    text = text + "0\n"
            if debug:
                if connection_found:
                    print(f"Generated bit stream connections to BUS {bus}")
                else:
                    print(f"No connections for BUS {bus}")
        else:
            text = text + "0\n"*no_registers
            if debug:
                print(f"BUS {bus} not in connections list")
    return text + "0\n"  # add dummy zero at the end 

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert connections json file to bitstream text file")
    parser.add_argument('-i', '--input', default="connections.json", help="Connections JSON file")
    parser.add_argument('-o', '--output', default="bitstream.txt", help="Bitstream output file")
    parser.add_argument('-d', '--debug', action='store_true', help="Enable debug mode")

    args = parser.parse_args()

    connections = read_connections(args.input, debug=args.debug)
    bitstream = generate_bit_stream(connections, debug=args.debug)
    output_filename = args.output
    write_bitstream(args.output, bitstream, debug=args.debug)
    clk_filename, clk_extension = os.path.splitext(output_filename)
    clk_filename = clk_filename + "_clk" + clk_extension
    write_clk(clk_filename, debug=args.debug)
    

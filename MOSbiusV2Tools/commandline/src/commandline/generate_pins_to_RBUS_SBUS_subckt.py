import json
import os
from datetime import datetime

def generate_pins_to_RBUS_SBUS_subckt(circuit_file, output_spice_file):
    """
    Generates a SPICE subcircuit file connecting chip pins to RBUS and SBUS nodes.

    Args:
        circuit_file (str): Path to the circuit JSON file.
        output_spice_file (str): Path to the output SPICE netlist file.
    """
    # Define the paths to the necessary support files
    chip_config_dir = os.path.join(os.path.dirname(__file__), "chip_config_data")
    pin_mapping_file = os.path.join(chip_config_dir, "pin_name_to_number.json")
    subckt_template_file = os.path.join(os.path.dirname(__file__), "subckt_templates/PK_pins_to_RBUS_SWBUS_template.cir")

    print(f"Looking for pin mapping file at: {pin_mapping_file}")
    print(f"Looking for template file at: {subckt_template_file}")

    # Load the circuit JSON file
    with open(circuit_file, "r") as f:
        circuit_data = json.load(f)

    # Load the pin mapping JSON file
    with open(pin_mapping_file, "r") as f:
        pin_mapping = json.load(f)

    # Read the SPICE template
    with open(subckt_template_file, "r") as f:
        spice_template = f.read()

    # Start building the SPICE subcircuit
    spice_subcircuit = f"* File created on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
    spice_subcircuit += f"* From {circuit_file}\n" + spice_template + "\n"

    # Iterate over each BUS in the circuit data
    for bus, pins in circuit_data.items():
        if bus[0:4] == 'SBUS':
            continue
        # Replace RBUS1 with RBUS<1>, RBUS2 with RBUS<2>, etc.
        bus_with_brackets = bus.replace("RBUS", "RBUS<").replace("SBUS", "SWBUS<") + ">"

        # Select the first pin from the list of connected pins
        selected_pin = pins[0]

        # Get the pin number from the pin mapping
        pin_number = int(pin_mapping[selected_pin])

        # Add a zero-volt voltage source for the connection
        spice_subcircuit += f"V{bus}_to_pin{pin_number} {bus_with_brackets} pin<{pin_number}> 0\n"

        # Add a comment indicating the connection
        spice_subcircuit += f"* {bus} connected to {selected_pin} (pin<{pin_number}>)\n"

    # Add SBUS connections
    for sbus in range(1, 7):
        if sbus == 6:
            bus = f"DATA_SBUS6"
        else:
            bus = f"SBUS{sbus}"
        bus_with_brackets = f"SWBUS<{sbus}>"
        pin_number = int(pin_mapping[bus])

        # Add a zero-volt voltage source for the connection
        spice_subcircuit += f"V{bus}_to_pin{pin_number} {bus_with_brackets} pin<{pin_number}> 0\n"

    # Close the subcircuit in SPICE
    spice_subcircuit += ".ENDS\n"

    # Write the generated SPICE subcircuit to the output file
    with open(output_spice_file, "w") as f:
        f.write(spice_subcircuit)

    print(f"SPICE subcircuit saved to {output_spice_file}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate a SPICE subcircuit connecting pins to RBUS and SBUS.")
    parser.add_argument("circuit_file", help="Path to the circuit JSON file.")
    parser.add_argument("output_spice_file", help="Path to the output SPICE netlist file.")

    args = parser.parse_args()

    generate_pins_to_RBUS_SBUS_subckt(
        circuit_file=args.circuit_file,
        output_spice_file=args.output_spice_file
    )

if __name__ == "__main__":
    main()
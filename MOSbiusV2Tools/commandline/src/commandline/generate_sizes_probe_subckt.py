import json
import os
from datetime import datetime
import importlib.resources

def generate_sizes_probe_subckt(sizes_file, output_spice_file):
    """
    Combines the generation of register settings and SPICE netlist into one function.

    Args:
        sizes_file (str): Path to the JSON file containing device sizes.
        output_spice_file (str): Path to the output SPICE netlist file.
    """
    # Define the path to the chip_config_data directory
    # Use the package resource path instead of relative paths
    chip_config_dir = os.path.join(os.path.dirname(__file__), "chip_config_data")
    registers_file = os.path.join(chip_config_dir, "device_name_to_sizing_registers.json")

    # Define the path to the subckt template file
    subckt_template_file = os.path.join(os.path.dirname(__file__), "subckt_templates/PK_set_sizes_template.cir")

    print(f"Looking for registers file at: {registers_file}")
    print(f"Looking for template file at: {subckt_template_file}")

    # Load sizes and registers
    with open(sizes_file, "r") as f:
        sizes = json.load(f)

    with open(registers_file, "r") as f:
        registers = json.load(f)

    # Read the entire subckt template file as a string
    with open(subckt_template_file, "r") as f:
        subckt_header = f.read()

    # Initialize the output dictionary for register settings
    register_settings = {}

    # Generate register settings
    for device, bit_to_register in registers.items():
        size = sizes.get(device, [0])[0]  # Default size to 0 if device is not in sizes.json
        if not (0 <= size <= 31):  # Validate size is a 5-bit number
            print(f"Warning: Size {size} for device {device} is not a 5-bit number.")
            size = 0

        # Iterate through the registers and set their values based on the size
        for bit, register in sorted(bit_to_register.items(), key=lambda x: int(x[0])):
            register_settings[register] = 1 if int(bit) & size else 0

    # Sort the output dictionary by register number
    sorted_register_settings = dict(sorted(register_settings.items()))

    # Generate SPICE netlist
    with open(output_spice_file, "w") as f:
        # Write the SPICE header
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"* Generated PK_set_sizes netlist\n")
        f.write(f"*   for {sizes_file}\n")
        f.write(f"*   on {current_time}\n\n")

        # Write the subckt header from the template file
        f.write(subckt_header + "\n")

        # Iterate through each device, sorted by device name
        for device in sorted(registers.keys()):
            f.write(f"* Device: {device} Size: {sizes.get(device, [0])[0]}\n")  # Add a comment for the device
            bit_to_register = registers[device]
            for bit, register in sorted(bit_to_register.items(), key=lambda x: int(x[0])):
                register_value = sorted_register_settings.get(register, 0)
                if register_value == 1:
                    f.write(f"V_{device}_{register} PROBE<{register}> VDD 0\n")
                else:
                    f.write(f"V_{device}_{register} PROBE<{register}> VSS 0\n")
            f.write("\n")  # Add a blank line after each device group

        # Write the SPICE footer
        f.write(".ENDS\n")

    print(f"SPICE netlist saved to {output_spice_file}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate a SPICE subcircuit based on device sizes.")
    parser.add_argument("sizes_file", help="Path to the JSON file containing device sizes.")
    parser.add_argument("output_spice_file", help="Path to the output SPICE netlist file.")

    args = parser.parse_args()

    generate_sizes_probe_subckt(
        sizes_file=args.sizes_file,
        output_spice_file=args.output_spice_file
    )

if __name__ == "__main__":
    main()
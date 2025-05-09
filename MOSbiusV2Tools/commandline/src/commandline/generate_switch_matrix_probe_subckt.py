import json
import os
from datetime import datetime

def generate_switch_matrix_probe_subckt(circuit_json_path, output_path):
    # Define the path to the chip_config_data directory
    chip_config_dir = os.path.join(os.path.dirname(__file__), "chip_config_data")

    # Load the pin-to-switch matrix mapping JSON
    pin_map_path = os.path.join(chip_config_dir, "pin_name_to_sw_matrix_pin_number.json")
    print(f"Looking for pin map file at: {pin_map_path}")
    with open(pin_map_path, 'r') as pin_map_file:
        pin_to_sw_matrix = json.load(pin_map_file)

    # Load the switch matrix-to-register mapping JSON
    register_map_path = os.path.join(chip_config_dir, "switch_matrix_register_map.json")
    print(f"Looking for register map file at: {register_map_path}")
    with open(register_map_path, 'r') as register_map_file:
        sw_matrix_to_register = json.load(register_map_file)

    # Load the SPICE template
    template_path = os.path.join(os.path.dirname(__file__), "subckt_templates/PK_set_SWMATRIX_template.cir")
    print(f"Looking for template file at: {template_path}")
    with open(template_path, 'r') as template_file:
        spice_header = template_file.readlines()

    # Load the circuit JSON
    with open(circuit_json_path, 'r') as circuit_file:
        circuit_data = json.load(circuit_file)

    # Open the output file for writing
    with open(output_path, 'w') as output_file:
        # Write the SPICE template header
        creation_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        output_file.writelines(f"* File created on: {creation_time}\n")
        output_file.writelines(f"* From this circuit description: {circuit_json_path}\n")
        output_file.writelines(spice_header)

        # Track connected probes
        connected_probes = set()

        # Iterate through each connection in the circuit JSON
        for bus, entries in circuit_data.items():
            if bus.startswith("RBUS"):
                # Handle RBUS
                for pin in entries:
                    sw_matrix_pin = pin_to_sw_matrix.get(pin, None)
                    if sw_matrix_pin is None:
                        print(f"Warning: Pin '{pin}' not found in pin-to-switch matrix mapping")
                        continue

                    register = sw_matrix_to_register.get(str(int(sw_matrix_pin)), {}).get(bus, None)
                    if register is None:
                        print(f"Warning: Register not found for sw_matrix_pin '{sw_matrix_pin}' and bus '{bus}'")
                        continue

                    output_file.write(f"* Connection: {bus}, Pin: {pin}, sw_matrix_pin: {sw_matrix_pin}, Register: {register}\n")
                    output_file.write(f"V{pin}_to_{bus} PROBE<{int(register)}> VDD 0\n")
                    connected_probes.add(int(register))

            elif bus.startswith("SBUS"):
                # Handle SBUS
                for entry in entries:
                    terminal = entry["terminal"]
                    connection = entry["connection"]

                    # Determine SBUSa and SBUSb keys
                    sbus_a = f"{bus}a"
                    sbus_b = f"{bus}b"
                    sw_matrix_pin = pin_to_sw_matrix.get(terminal, None)
                    if sw_matrix_pin is None:
                        print(f"Warning: Pin '{terminal}' not found in pin-to-switch matrix mapping")
                        continue

                    register_a = sw_matrix_to_register.get(str(int(sw_matrix_pin)), {}).get(sbus_a, None)
                    register_b = sw_matrix_to_register.get(str(int(sw_matrix_pin)), {}).get(sbus_b, None)
                    if (register_a is None) or (register_b is None):
                        print(f"Warning: Register not found for sw_matrix_pin '{sw_matrix_pin}' and buses '{sbus_a} and {sbus_b}'")
                        continue

                    # Decode the type of connection
                    if connection == "ON":
                        sbus_a_connection = "VDD"
                        sbus_b_connection = "VDD"
                    elif connection == "PHI1":
                        sbus_a_connection = "VDD"
                        sbus_b_connection = "VSS"
                    elif connection == "PHI2":
                        sbus_a_connection = "VSS"
                        sbus_b_connection = "VDD"
                    else:  # Default to "OFF"
                        sbus_a_connection = "VSS"
                        sbus_b_connection = "VSS"

                    # Write SBUSa and SBUSb connections
                    output_file.write(f"* Connection: {bus}, Terminal: {terminal}, Connection Key: {connection}\n")
                    output_file.write(f"V{register_a}_to_{terminal} PROBE<{register_a}> {sbus_a_connection} 0\n")
                    output_file.write(f"V{register_b}_to_{terminal} PROBE<{register_b}> {sbus_b_connection} 0\n")

                    # Mark these probes as connected
                    connected_probes.add(int(register_a))
                    connected_probes.add(int(register_b))

        # By default, connect all unused probes to VSS
        for probe in range(1, 1889):  # Assuming 1888 probes
            if probe not in connected_probes:
                output_file.write(f"Vprobe_{probe}_to_VSS PROBE<{probe}> VSS 0\n")

        # Write the SPICE footer
        output_file.write(".ENDS\n")

        print(f"SPICE netlist saved to {output_path}")

def main():
    import argparse

    parser = argparse.ArgumentParser(description="Generate a SPICE subcircuit for PROBE connections.")
    parser.add_argument("circuit_json_path", help="Path to the circuit JSON file.")
    parser.add_argument("output_path", help="Path to the output SPICE file.")

    args = parser.parse_args()

    generate_switch_matrix_probe_subckt(
        circuit_json_path=args.circuit_json_path,
        output_path=args.output_path
    )

if __name__ == "__main__":
    main()
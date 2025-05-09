# MOSbius V2 Tools

## Overview
MOSbius V2 Tools is a Python-based project designed for generating SPICE circuit files from JSON configurations. It facilitates the mapping of circuit components to switch matrix pins and registers, enabling efficient simulation of electronic circuits.

## Features
- **Circuit Generation**: Automatically generates SPICE circuit files based on provided JSON configurations.
- **RBUS and SBUS Support**: Handles connections for both RBUS and SBUS configurations, allowing for versatile circuit designs.
- **Template Integration**: Utilizes SPICE templates to ensure proper formatting and structure of the output files.

## File Structure
```
MOSbiusV2Tools
├── src
│   ├── generate_probe_subckt.py       # Main script for generating SPICE files
│   └── utils
│       └── __init__.py                 # Utility functions (currently empty)
├── examples
│   ├── INV_string_5_RBUS.json          # Example circuit configuration using RBUS
│   ├── INV_string_clocked_RBUS_SBUS.json # Example circuit configuration with RBUS and SBUS
│   └── PK_set_SWMATRIX_template.cir    # SPICE template for circuit generation
├── data
│   ├── pin_name_to_sw_matrix_pin_number.json # Maps pin names to switch matrix pin numbers
│   └── switch_matrix_register_map.json   # Maps switch matrix pins to registers
├── README.md                             # Project documentation
└── requirements.txt                      # Project dependencies
```

## Usage
1. **Install Dependencies**: Ensure all required packages are listed in `requirements.txt` are installed.
2. **Prepare JSON Files**: Create or modify JSON files in the `examples` directory to define your circuit configurations.
3. **Run the Script**: Execute `generate_probe_subckt.py` to generate the corresponding SPICE circuit files based on the JSON inputs.

## Contribution
Contributions to enhance the functionality of MOSbius V2 Tools are welcome. Please submit a pull request or open an issue for discussion.

## License
This project is licensed under the MIT License. See the LICENSE file for details.
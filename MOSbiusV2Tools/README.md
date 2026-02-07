# MOSbiusV2Tools

Tools for the MOSbiusV2. 

## Overview
MOSbiusV2Tools is a Python package that provides command-line tools for generating SPICE subcircuits from JSON circuit descriptions and sizing files. It facilitates the mapping of circuit components to switch matrix pins and registers, enabling efficient simulation of electronic circuits.

## Installation

### Installing from GitHub

You can install the package directly from GitHub using pip:

```bash
pip install git+https://github.com/peterkinget/MOSbiusCADFlow.git@MOSbiusV2Tools_pkdist#subdirectory=MOSbiusV2Tools
```

This branch contains fixes for properly including the required configuration and template files in the installation.

### Installing from Source

Alternatively, you can clone the repository and install the package from source:

```bash
git clone https://github.com/peterkinget/MOSbiusCADFlow.git
cd MOSbiusCADFlow/MOSbiusV2Tools
pip install .
```

### Building the Package

If you want to build the package yourself:

```bash
cd MOSbiusV2Tools
python -m build
```

This will create wheel and source distributions in the `dist` directory.

## Command-line Tools

The package provides three main command-line tools:

1. **`generate_sizes_probe_subckt`** - Generates a SPICE subcircuit file based on device sizes.
2. **`generate_pins_to_RBUS_SBUS_subckt`** - Generates a SPICE subcircuit file connecting chip pins to RBUS and SBUS nodes.
3. **`generate_switch_matrix_probe_subckt`** - Generates a SPICE subcircuit file for PROBE connections.

## Usage

### Device Sizing

```bash
generate_sizes_probe_subckt sizes.json output_spice_file.cir
```

### Connecting Pins to RBUS and SBUS

```bash
generate_pins_to_RBUS_SBUS_subckt circuit.json output_spice_file.cir
```

### Switch Matrix Configuration

```bash
generate_switch_matrix_probe_subckt circuit.json output_spice_file.cir
```

## Circuit Description

Create a `.json` file to describe the circuit connectivity that the on-chip switch matrix needs to implement. 

All terminals of the devices are connected to pins of the chip as listed below. 

```
{
    "VSS": 1.0,
    "EN": 2.0,
    "CLK": 3.0,
    "DATA_SBUS6": 4.0,
    "SBUS5": 5.0,
    "SBUS4": 6.0,
    "SBUS3": 7.0,
    "SBUS2": 8.0,
    "SBUS1": 9.0,
    "DCC1_P_D_L_CC": 10.0,
    "DCC1_P_D_R_CS": 11.0,
    "DCC1_P_D_R_CC": 12.0,
    "VDD": 13.0,
    "DINV1_INP_L": 14.0,
    "DINV1_INN_L": 15.0,
    "DINV1_OUT_L": 16.0,
    "DINV1_INP_R": 17.0,
    "DINV1_INN_R": 18.0,
    "DINV1_OUT_R": 19.0,
    "DINV2_INP_L": 20.0,
    "DINV2_INN_L": 21.0,
    "DINV2_OUT_L": 22.0,
    "DINV2_INP_R": 23.0,
    "DINV2_INN_R": 24.0,
    "DINV2_OUT_R": 25.0,
    "DCC4_P_G_L_CC": 26.0,
    "DCC4_P_G_L_CS": 27.0,
    "DCC4_P_G_R_CC": 28.0,
    "DCC4_P_G_R_CS": 29.0,
    "DCC4_P_D_L_CC": 30.0,
    "DCC4_P_D_L_CS": 31.0,
    "DCC4_P_D_R_CC": 32.0,
    "DCC4_P_D_R_CS": 33.0,
    "OTA_P_INP": 34.0,
    "OTA_P_INN": 35.0,
    "OTA_P_OUT": 36.0,
    "CC_N_G_CC": 37.0,
    "CC_N_G_CS": 38.0,
    "CC_N_D_CC": 39.0,
    "CC_N_D_CS": 40.0,
    "DCC2_N_G_L_CC": 41.0,
    "DCC2_N_G_L_CS": 42.0,
    "DCC2_N_G_R_CC": 43.0,
    "DCC2_N_G_R_CS": 44.0,
    "DCC2_N_D_L_CC": 45.0,
    "DCC2_N_D_L_CS": 46.0,
    "DCC2_N_D_R_CC": 47.0,
    "DCC2_N_D_R_CS": 48.0,
    "DCC3_N_G_L_CC": 49.0,
    "DCC3_N_G_L_CS": 50.0,
    "DCC3_N_G_R_CC": 51.0,
    "DCC3_N_G_R_CS": 52.0,
    "DCC3_N_D_L_CC": 53.0,
    "DCC3_N_D_L_CS": 54.0,
    "DCC3_N_D_R_CC": 55.0,
    "DCC3_N_D_R_CS": 56.0,
    "DCC3_P_G_L_CS": 57.0,
    "DCC3_P_G_L_CC": 58.0,
    "DCC3_P_G_R_CS": 59.0,
    "DCC3_P_G_R_CC": 60.0,
    "DCC3_P_D_L_CS": 61.0,
    "DCC3_P_D_L_CC": 62.0,
    "DCC3_P_D_R_CS": 63.0,
    "DCC3_P_D_R_CC": 64.0,
    "DCC1_N_G_L_CC": 65.0,
    "DCC1_N_G_L_CS": 66.0,
    "DCC1_N_G_R_CC": 67.0,
    "DCC1_N_G_R_CS": 68.0,
    "DCC1_N_D_L_CC": 69.0,
    "DCC1_N_D_L_CS": 70.0,
    "DCC1_N_D_R_CC": 71.0,
    "DCC1_N_D_R_CS": 72.0,
    "DCC2_P_G_L_CS": 73.0,
    "DCC2_P_G_L_CC": 74.0,
    "DCC2_P_G_R_CS": 75.0,
    "DCC2_P_G_R_CC": 76.0,
    "DCC2_P_D_L_CS": 77.0,
    "DCC2_P_D_L_CC": 78.0,
    "DCC2_P_D_R_CS": 79.0,
    "DCC2_P_D_R_CC": 80.0,
    "OTA_N_INP": 81.0,
    "OTA_N_INN": 82.0,
    "OTA_N_OUT": 83.0,
    "CC_P_G_CS": 84.0,
    "CC_P_G_CC": 85.0,
    "CC_P_D_CS": 86.0,
    "CC_P_D_CC": 87.0,
    "DCC4_N_G_L_CC": 88.0,
    "DCC4_N_G_L_CS": 89.0,
    "DCC4_N_G_R_CC": 90.0,
    "DCC4_N_G_R_CS": 91.0,
    "DCC4_N_D_L_CC": 92.0,
    "DCC4_N_D_L_CS": 93.0,
    "DCC4_N_D_R_CC": 94.0,
    "DCC4_N_D_R_CS": 95.0,
    "DCC1_P_G_L_CS": 96.0,
    "DCC1_P_G_L_CC": 97.0,
    "DCC1_P_G_R_CS": 98.0,
    "DCC1_P_G_R_CC": 99.0,
    "DCC1_P_D_L_CS": 100.0
}
```

### Regular-Bus Connections

There are 8 regular buses, "RBUS1" thru "RBUS8"; the `.json` circuit file describes which device terminals connect to each
```
{
    "RBUS1": ["DINV2_INP_L", "DINV2_INN_L"],
    "RBUS2": ["DINV2_OUT_L", "DINV2_INP_R", "DINV2_INN_R"],
    "RBUS3": ["DINV2_OUT_R", "DINV1_INP_L", "DINV1_INN_L"],
    "RBUS4": ["DINV1_OUT_L", "DINV1_INP_R", "DINV1_INN_R"], 
}
```
### Switched-Bus Connections

There are 6 switched buses, "SBUS1 thru "SBUS6"; these buses can make a permanent connection to a terminal "ON", or a clocked connection using non-overlapping clock phases "PHI1" or "PHI2".
```
{
    "RBUS1": ["CC_N_G_CC", "CC_P_G_CC"],
    "RBUS2": ["CC_N_D_CC", "CC_P_D_CC"],
    "RBUS7": ["VSS", "CC_P_G_CS"],
    "RBUS8": ["VDD", "CC_N_G_CS"],
    "SBUS1": [
        {"terminal": "DINV1_INP_L", "connection": "ON"},
        {"terminal": "DINV1_INN_L", "connection": "ON"},
        {"terminal": "CC_N_D_CC", "connection": "PHI1"}
    ],
    "SBUS2": [
        {"terminal": "DINV1_INP_R", "connection": "ON"},
        {"terminal": "DINV1_INN_R", "connection": "ON"},
        {"terminal": "DINV1_OUT_L", "connection": "PHI2"}
    ],
    "SBUS3": [
        {"terminal": "DINV2_INP_L", "connection": "ON"},
        {"terminal": "DINV2_INN_L", "connection": "ON"},
        {"terminal": "DINV1_OUT_R", "connection": "PHI1"}
    ],
    "SBUS4": [
        {"terminal": "DINV2_INP_R", "connection": "ON"},
        {"terminal": "DINV2_INN_R", "connection": "ON"},
        {"terminal": "DINV2_OUT_L", "connection": "PHI2"}
    ]
}
```

One `circuit.json` file contains the whole circuit connections description for the RBUSes and the SBUSes as shown above. 

### Transistor Sizing

Create a separate `.json` file with the sizing for all the devices; here is an empty file:
```
{
    "CC_N": [],
    "CC_P": [],
    "DCC1_N_L": [],
    "DCC1_N_R": [],
    "DCC1_P_L": [],
    "DCC1_P_R": [],
    "DCC2_N_L": [],
    "DCC2_N_R": [],
    "DCC2_P_L": [],
    "DCC2_P_R": [],
    "DCC3_N_L": [],
    "DCC3_N_R": [],
    "DCC3_P_L": [],
    "DCC3_P_R": [],
    "DCC4_N_L": [],
    "DCC4_N_R": [],
    "DCC4_P_L": [],
    "DCC4_P_R": [],
    "DINV1_L": [],
    "DINV1_R": [],
    "DINV2_L": [],
    "DINV2_R": [],
    "OTA_N": [],
    "OTA_P": []
}
``` 
Fill in the sizes `0, 1, 2, ... 31` for the respective devices in the file. If you omit a device the size will be set to `0`. Here is an example of a sizing file: 
```
{
    "CC_N": [1],
    "CC_P": [1],
    "DCC1_N_L": [5],
    "DCC1_N_R": [5],
    "DCC1_P_L": [5],
    "DCC1_P_R": [5],
    "DCC2_N_L": [7],
    "DCC2_N_R": [7],
    "DCC2_P_L": [7],
    "DCC2_P_R": [7],
    "DCC3_N_L": [9],
    "DCC3_N_R": [9],
    "DCC3_P_L": [9],
    "DCC3_P_R": [9],
    "DCC4_N_L": [11],
    "DCC4_N_R": [11],
    "DCC4_P_L": [11],
    "DCC4_P_R": [11],
    "DINV1_L": [13],
    "DINV1_R": [13],
    "DINV2_L": [15],
    "DINV2_R": [15],
    "OTA_N": [1],
    "OTA_P": [1]
}
```

## Examples

Example JSON files are provided in the `examples` directory:

- `INV_string_5_RBUS.json` - Example circuit description using RBUS connections
- `INV_string_clocked_RBUS_SBUS.json` - Example with both RBUS and SBUS connections
- `all_transistors_4x_sizes.json` - Example device sizing file

## License

This project is licensed under the MIT License.
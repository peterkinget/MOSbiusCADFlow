# MOSBiusTools

* Contains python modules and command-line scripts to interface with the Mobius chip. 

* Currently available from TestPyPI as [MOSbiusTools](https://test.pypi.org/project/MOSbiusTools)
  - we advise to create a virtual environment to install the tools
  - install using `pip3 install -i https://test.pypi.org/simple MOSbiusTools`
  - installs the `MOSbiusTools` module and two executable scripts described below.




## connections_to_bitstream

*  `connections_to_bitstream` converts a connections.json file into a bitstream to program the MOSbius chip.

* run `connections_to_bitstream -h` and you get a brief description of
  script usage. 
  
* There is a blank `connections.json` file provided and some [examples](./MOSbiusTools/scripts/examples_connections/). 

## cir_to_connections

*  `cir_to_connections` converts an LTSpice netlist (`.cir`)
  into a `connections.json` file that the `connections_to_bitstream`
  script can convert into a bitstream file. 

* Run `cir_to_connections -h` and you get a brief description of
  script usage. 
  
* There are some example `.cir` files provided in
  [examples](./MOSbiusTools/scripts/examples_cir). 

## Basic Steps to Create Bitstream Files

### From LTspice Schematic
* create an LTspice schematic using the [LTspice Library](../LTspice)
* save your design as a `.cir` file, e.g. `my_circuit.cir`. You obtain a `.cir`
  netlist for your LTSpice circuit by right clicking on the schematic,
  then 'View SPICE Netlist', then 'Save As'. 
* create a `connections.json` file:
  - `cir_to_connections -i my_circuit.cir -o connections_my_circuit.json -d`
  - the `-d` is not required but will provide some output to review the conversion process.
  - you can choose your own filename for the json file, but a .json is recommended.
* convert the `connections_my_circuit.json` to a bitstream file with `connections_to_bitstream` -- see next topic.

### From Connections Json File
* prepare connections file:
  - You can create a connections file in your text editor by starting from [connections.json](./MOSbiusTools/scripts/examples_connections/connections.json); for each *BUS* list the pcb pin numbers that need to be connected to it [(OTA example)](./MOSbiusTools/scripts/examples_connections/connections_Miller_OTA_pin.json); let's assume you save it as `connections_my_circuit.json`. 
  - Or, you can use the `cir_to_connections` script described above.
* convert connections file to bitstream files:
  - `connections_to_bitstream -i connections_my_circuit.json -o my_circuit_bitstream.txt -d`
  - `-d` is not required but will provide output so you can review the conversion.
  - you can choose your won filename for the output file, but a `.txt` extension is recommended; besides `my_circuit_bitstream.txt`, `my_circuit_bitstream_clk.txt` will also be generated.
  - the bitstream files can be used with the ADALM2000 to generate the digital programming waveforms (CLK and DATA).
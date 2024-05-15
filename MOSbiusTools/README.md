# MOSBiusTools

* Contains python modules and scripts to interface with the Mobius chip. 

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

*  `cir_to_connections` converts an LTSpice netlist
  into a `connections.json` file that the `connections_to_bitstream`
  script can convert into a bitstream file. 

* Run `cir_to_connections -h` and you get a brief description of
  script usage. 
  
* There are some example `.cir` files provided in
  [examples](./MOSbiusTools/scripts/examples_cir). You obtain a `.cir`
  netlist for your LTSpice circuit by right clicking on the schematic,
  then 'View SPICE Netlist', then 'Save As'. 

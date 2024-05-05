* Contains python modules developed by Cade in order to interface
with the Mobius chip. 

## connections_to_bitstream

*  [connections_to_bitstream](./connections_to_bitstream) contains a
  python script `connections_to_bitstream.py` developed by PK to converted a connections.json file
  into a bitstream to program the Mobius chip.

* run `./connections_to_bitstream.py -h` and you get a brief description of
  script usage. 
  
* There is a blank `connections.json` file provided and some [examples](./connections_to_bitstream/examples). 

## cir_to_connections

*  [cir_to_connections](./cir_to_connections) contains a python script
  `cir_to_connections.py` developed by PK to convert an LTSpice netlist
  into a `connections.json` file that the `connections_to_bitstream.py`
  script can convert into a bitstream file. It uses the `BitStream`
  object programmed by Cade. `Bitstream` is located in [](generation_modules/src)

* run `./cir_to_connections.py -h` and you get a brief description of
  script usage. 
  
* There are some example `.cir` files provided and some
  [examples](./cir_to_connections/example_cir). You obtain a `.cir`
  netlist for your LTSpice circuit by right clicking on the schematic,
  then 'View SPICE Netlist', then 'Save As'. 

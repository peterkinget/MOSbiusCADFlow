# MOSbius_LTspice_Library
 This is a cleaned up LTspice library for the MOSbius chip based on Prof. Peter Kinget's v4 library.
 https://github.com/peterkinget/MOSbiusCADFlow

The major changes are the transistor symbols. I modified the symbols so that they are consistent to what we use in textbooks and Cadence Virtuoso. 
The pin number annotations correspond to the numbering on the breakout PCB.
![](./screenshots/template_all_transistors.png)

# How to use
Copy `Template_MOSbius_transistors.asc` file and build the schematic by modifying it. Attach bus labels to different nets for the tool to recognize them.
I also created `Template_MOSbius_four_amps.asc` if you want to start with multiple Miller OTAs.
Add Spice directives such as `.tran 0 10u` and run some simulations.

# TODO
- Explore better ways to organize the library (LTspice prefer a flat hierarchy, which isn't very elegant)
- Add Chip_ID properties to the symbols for potential multi-chip setups.
- Adjust the MOSFET models to better match the measurement results (particularly Vth).
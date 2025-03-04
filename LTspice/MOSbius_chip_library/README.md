# MOSbius_LTspice_Library

## Symbol Library Update (Peter Kinget, Feb 2025 & March 2025)

This library incorporates the symbols created by Jianxun Zhu available from https://github.com/jianxun/MOSbius_LTspice_Library. 

### How to use 
Instructions on how to use this library are available from [MOSbius.org](https://mosbius.org/4_chapter_simulations/LTspice_simulations.html). 

March 2025: 
- renamed the folders to less cumbersome name
- there we some flips between A&B type blocks and their symbols, which have been corrected now.
- A and B labels have been added to the various transistors to more
  easily map them to simulation files
- `MOSbius_chip_name_dictionary.json` added as a template to be used with `LTspice_OP`
  from the [MOS_OP](https://github.com/peterkinget/) tools. 
  
--- 
## Original README.md (Jianxun Zhu, Jan 2025)

 This is a cleaned up LTspice library for the MOSbius chip based on Prof. Peter Kinget's v4 library.
 https://github.com/peterkinget/MOSbiusCADFlow

The major changes are the transistor symbols. I modified the symbols so that they are consistent to what we use in textbooks and Cadence Virtuoso. 
The pin number annotations correspond to the numbering on the breakout PCB.
![](./screenshots/template_all_transistors.png)

### How to use
Copy `Template_MOSbius_transistors.asc` file and build the schematic by modifying it. Attach bus labels to different nets for the tool to recognize them.
I also created `Template_MOSbius_four_amps.asc` if you want to start with multiple Miller OTAs.
Add Spice directives such as `.tran 0 10u` and run some simulations.

### TODO
- Explore better ways to organize the library (LTspice prefer a flat hierarchy, which isn't very elegant)
- Add Chip_ID properties to the symbols for potential multi-chip setups.
- Adjust the MOSFET models to better match the measurement results (particularly Vth).

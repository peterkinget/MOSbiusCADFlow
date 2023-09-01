# Author: Cade Gleekel
# Created: 7/6/2023
# Description: Bitstream Class for Mobius Chip digital configuration file generation.

"""
public class attributes (
    bitmatrix,
    bitstream,
    active_buslist,
    active_pinlists,
    instance_netlist,
    hexstring,
    vddbus_flag,
    vssbus_flag
)

public class methods (
    manualInput,
    netlistInput,
    generateBitstream,
    getPowerBuses,
    compareStream,
    compareFile,
    writeBitFile,
    writeHexFile


"""


class BitStream:
    #  private class dictionary mapping subcircuit port order indices to output pin numbers
    _subckt_pindict = {
        "nmos_currentmirror_array": [19, 20, 21, 22, 23, 24, 25],
        "nmos_currentmirror": [26, 27],
        "dp_nmos_1x_a": [36, 35, 37],
        "dp_nmos_1x_b": [39, 40, 38],
        "dp_nmos_4x_a": [45, 46, 44, 47],
        "dp_nmos_4x_b": [42, 41, 43, 47],
        "cs_nmos_4x_a": [28, 29],
        "cs_nmos_4x_b": [30, 31],
        "ota_nmos": [19, 32, 33, 34],
        "pmos_currentmirror_array": [68, 67, 66, 65, 64, 63],
        "pmos_currentmirror": [62, 61],
        "dp_pmos_1x_a": [12, 13, 14],
        "dp_pmos_1x_b": [17, 16, 15],
        "dp_pmos_4x_a": [6, 7, 8, 5],
        "dp_pmos_4x_b": [9, 10, 11, 5],
        "cs_pmos_4x_a": [57, 58],
        "cs_pmos_4x_b": [59, 60],
        "ota_pmos": [68, 56, 55, 54],
        "inverter_a": [53, 52, 51],
        "inverter_b": [48, 50, 49],
        "chip_vdd": [1],
        "chip_vss": [18],
    }

    # private class dictionary mapping binary 8-bit values to 2-digit hex values
    _hexdict = {
        "0000": "0",
        "0001": "1",
        "0010": "2",
        "0011": "3",
        "0100": "4",
        "0101": "5",
        "0110": "6",
        "0111": "7",
        "1000": "8",
        "1001": "9",
        "1010": "A",
        "1011": "B",
        "1100": "C",
        "1101": "D",
        "1110": "E",
        "1111": "F",
    }

    #  class constructor method (an input method must be called to complete object construction)
    def __init__(self):
        self.bitmatrix = None  # list of lists of ints, each list of ints represents a bus, each int represents a pin state
        self.bitstream = None  # list of ints, each int represents a pin state
        self.active_buslist = (
            None  # list of ints, each int represents an active bus number
        )
        self.active_pinlists = None  # list of lists of ints, each list of ints represents the active pins on a bus
        self.instance_netlist = None  # list of lists of strings, each list of strings represents a subcircuit instance
        self.hexstring = None  # string of hex digits, each hex digit represents 4 bits of the bitstream
        self.vddbus_flag = False  # boolean, true if VDD bus is present in the netlist
        self.vssbus_flag = False  # boolean, true if VSS bus is present in the netlist
        self._power_buses = [
            0,
            0,
        ]  # list of ints, each int represents a power bus number (0 indicates no bus)
        self._input_flag = False  # boolean, true if input lists have been generated

    #  public method to generate bsGen input lists from manual input (by setting active_buslist and active_pinlists attributes)
    def manualInput(self):
        inputs = (
            []
        )  # list of lists of strings, one for each bus, each list of strings contains the active pin numbers of the bus
        print(
            "input each active bu number seperated by a space (return to complete entry)"
        )
        abuses = input("active buses: ").split()
        print(
            "\n"
            + "input each active pin number on the bus seperated by a space (return to complete entry)"
        )
        for i in range(len(abuses)):
            abpins = input("Bus" + abuses[i] + " pins: ").split()
            inputs.append(abpins)

        self.active_buslist = abuses
        self.active_pinlists = inputs
        self._input_flag = True
        # return inputs, abuses

    #  public method to generate bsGen input lists from netlist file located in netlist_catalog (by setting active_buslist and active_pinlists attributes)
    def netlistInput(self, nfpath):
        netlist = self._readNetlist(nfpath)
        ab_members = [[] for i in range(10)]
        ab_numbers = []

        for line in netlist:
            subckt_key = line[-1]
            icount = 0  # line item count

            for item in line[1:-1]:
                ab = self._getActiveBus(item)
                ab_str = str(ab)
                if ab != 0:
                    self._ifPowerBus(subckt_key, ab)
                    ap = self._getActivePin(subckt_key, icount)
                    ap_str = str(ap)
                    # update active bus and pin lists
                    ab_members[ab - 1].append(ap)
                    ab_numbers.append(ab)
                icount += 1
        # check for power bus shorts
        try:
            self._checkPowerBuses()
        except ValueError as err:
            print(f"Error: {err}")

        # remove duplicates/inactive lists and sort low to high
        ab_numbers = list(dict.fromkeys(ab_numbers))
        ab_numbers.sort(key=int)
        ab_members = [sorted(x) for x in ab_members if x != []]  # remove empty lists

        self.instance_netlist = netlist
        self.active_buslist = ab_numbers
        self.active_pinlists = ab_members
        self._input_flag = True

    #  public method to generate output bits from active bus and pin lists (by setting bitmatrix and bitstream attributes)
    def generateBitstream(self):
        self._checkInput()
        ab_pins = self.active_pinlists
        ab = self.active_buslist
        # initialize the output list with 10 rows of 68 '0's
        bitmatrix = [[0] * 68 for _ in range(10)]
        for bi, bus in enumerate(ab):
            ri = 10 - int(bus)  # output row index
            for pin in ab_pins[bi]:
                ci = 68 - int(pin)  # output column index
                bitmatrix[ri][ci] = 1  # set the bit to 1

        bitmatrix = self._rmDigitalPins(bitmatrix)
        self.bitmatrix = bitmatrix
        self.bitstream = self._bsFlatten()
        return self.bitstream

    # public method returns vss and vdd bus numbers as a list (0 indicates no bus)
    def getPowerBuses(self):
        return self._power_buses

    #  public method to compare the output bitstream to another bitstream list (prints results, returns true if match)
    def compareStream(self, cstream: list):
        self._checkInput()
        if len(self.bitstream) != len(cstream):
            print("bitstreams are not the same length")
            return False
        for i in range(len(self.bitstream)):
            bus_num = 10 - (i // 65)
            if self.bitstream[i] != cstream[i]:
                bus_num = 10 - (i // 65)
                pin_num = 65 - (i % 65)
                if pin_num > 1:
                    pin_num += 3
                print(
                    "bitstream does not match at: bus "
                    + str(bus_num)
                    + ", pin "
                    + str(pin_num)
                )
                print("output bit: " + str(self.bitstream[i]))
                print("compare bit: " + str(cstream[i]))
                return False
        print("bitstreams match")
        return True

    #  public method to compare the output bits file to another file located at path cfpath (prints results, returns true if match)
    def compareFile(self, cfpath: str):
        self._checkInput()
        with open(cfpath, "r") as f:
            compare_lines = f.readlines()
        f.close()
        for i in range(len(self.bitmatrix)):
            cline = [int(c) for c in compare_lines[i].strip()]
            if self.bitmatrix[i] != cline:
                bitmatrix_line = "".join(map(str, self.bitmatrix[i]))
                bus_str = "BUS " + str(10 - i)
                print("line " + str(i) + " (" + bus_str + ")" + " does not match")
                print("output bits" + " (" + bus_str + "): " + bitmatrix_line)
                print("compare bits" + " (" + bus_str + "): " + compare_lines[i])
                return False
        print("files match")
        return True

    #  public method to write the output bitmatrix as a .txt file to a specified path
    def writeBitFile(self, output_path: str):
        self._checkInput()
        bitlines = []
        for bus in self.bitmatrix:
            bus_str = list(map(str, bus))
            bus_str = "".join(bus_str)
            bus_str += "\n"
            bitlines.append(bus_str)

        with open(output_path, "w") as fid:
            fid.writelines(bitlines)
            fid.close()

    # public method to write the output hexstring as a .txt file to a specified path
    def writeHexFile(self, output_path: str):
        self._checkInput()
        self._bsToHex()
        with open(output_path, "w") as fid:
            fid.write(self.hexstring)
            fid.close()

    # stream in all zeros to reset the chip
    def zeroStream(self):
        self._checkInput()
        zero_stream = [0] * 650
        return zero_stream
    
    #  private helper method returns a stripped netlist that only contains the lines that define instance port connections
    def _readNetlist(self, nfp):
        with open(nfp, "r") as f:
            lines = f.readlines()
        f.close()
        # create a list of strings for all instance def lines in netlist, ignore rest
        netlist_stripped = []
        for line in lines[1:]:
            if line[0] == "*" or line[0] == "\n":
                return netlist_stripped
            netlist_stripped.append(line.split())

        return netlist_stripped

    #  private helper method identifies and returns active bus numbers from subckt instance port connections (returns 0 if not active bus)
    def _getActiveBus(self, item):
        if item[0:3] == "BUS":
            if item[3] == "0":
                return int(item[4:])
            else:
                return int(item[3:])
        else:
            return 0

    #  private helper method returns the active pin # on the bus
    def _getActivePin(self, key, pidx):
        ap = BitStream._subckt_pindict[key][pidx]
        return ap

    # private helper method checks if power buses are present in the netlist
    def _ifPowerBus(self, key, ab):
        if key == "chip_vss":
            self._power_buses[0] = ab
        elif key == "chip_vdd":
            self._power_buses[1] = ab
        return

    # private helper method checks if power buses are shorted together
    def _checkPowerBuses(self):
        if self._power_buses[0] != 0 and self._power_buses[1] != 0:
            if self._power_buses[0] == self._power_buses[1]:
                raise ValueError("VDD and VSS are shorted together")
            else:
                self.vddbus_flag = True
                self.vssbus_flag = True
        elif self._power_buses[0] != 0:
            self.vssbus_flag = True
        elif self._power_buses[1] != 0:
            self.vddbus_flag = True
        return

    #  private helper method checks if input lists have been generated
    def _checkInput(self):
        if self._input_flag == False:
            raise ValueError(
                "Error: no input lists have been generated, please run manualInput() or netlistInput()"
            )
        return

    #  private method to flatten the bitstream output into a list of ints for ADALM2000 compatibility
    def _bsFlatten(self):
        bs_flat = [pin for bus in self.bitmatrix for pin in bus]
        return bs_flat

    #  private helper method removes digital pins from the output bitstream lines
    def _rmDigitalPins(self, bitmatrix):
        for bus in bitmatrix:
            for i in range(3):
                bus.pop(68 - 4)

        return bitmatrix

    # private helper method to convert a binary list of integers (self.bitstream) to a hex string (returns self.hexstring)
    def _bsToHex(self):
        self._checkInput()
        # create a copy of self.bitstream
        bitstream = self.bitstream.copy()
        bitstring = "".join(map(str, bitstream))
        bitstring += "0" * (4 - (len(bitstring) % 4))
        hexstring = ""
        for i in range(0, len(bitstring), 4):
            hx_key = bitstring[i : i + 4]
            # print(hx_key)
            hexstring += BitStream._hexdict[hx_key]
        # add a space every 2 hex digits
        hexstring = " ".join(hexstring[i : i + 2] for i in range(0, len(hexstring), 2))
        self.hexstring = hexstring
        # print(len(self.hexstring))

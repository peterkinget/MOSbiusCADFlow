"""
This script generates a stream of digital signals to be outputted to a device. 
It uses the libm2k library to interface with the device and generate the signals. 
The script defines a SamplingParams class to compute the sampling parameters,
and several functions to generate the clock, data, and enable signals. 
The generate_streamout function combines these signals into a single buffer to be outputted to the device. 
The script also includes code to plot the generated signals using matplotlib.

Functions:
    generate_clock_signal(channel, samples_per_period):
        Generates a clock signal for the given channel and number of samples per period.
    generate_data_signal(channel, bitstream, samples_per_period):
        Generates a data signal for the given channel, bitstream, and number of samples per period.
    generate_enable_signal(channel, samples_per_period):
        Generates an enable signal for the given channel and number of samples per period.
    generate_streamout(digital, channels, bitstream, sampling_params: SamplingParams):
        Generates a stream of digital signals to be outputted to a device.
        Uses the generate_clock_signal, generate_data_signal, and generate_enable_signal functions.
    SamplingParams:
        A class for computing sampling parameters.
        Attributes:
            samples_per_period (int): The number of samples per period.
            sampling_frequency (int): The sampling frequency.
            buffer_size (int): The number of samples in the buffer.
        Methods:
            compute_sampling_frequency(samples_per_period):
                Computes the sampling frequency.
            compute_samples_per_period(sampling_frequency):
                Computes the number of samples per period.
            set_buffer_size():
                Sets the buffer size.
"""
import numpy as np



DIGITAL_CH_ENABLE = 0
DIGITAL_CH_CLK = 1
DIGITAL_CH_DATA = 2


NUM_BITS = 650
NUM_BITS_PADDING = 5  # padding clock cycles for the start and end of the buffer



class SamplingParams:
    def __init__(self, clock_frequency: int = 500000, samples_per_period: int = 0, sampling_frequency: int = 0):
        self.clock_frequency = clock_frequency
        self.samples_per_period = samples_per_period
        self.sampling_frequency = sampling_frequency
        self.buffer_size = None

        if self.samples_per_period == 0 and self.sampling_frequency == 0:
            raise ValueError(
                "Must specify either samples_per_period or sampling_frequency"
            )

        elif self.samples_per_period != 0 and self.sampling_frequency != 0:
            if self.sampling_frequency / self.samples_per_period != self.clock_frequency:
                raise ValueError(
                    "Sampling frequency and samples per period are not compatible with clock frequency ({} kHz)".format(
                        self.clock_frequency // 1000
                    )
                )
            else:
                pass

        elif self.samples_per_period != 0:
            if self.samples_per_period % 4 != 0:
                print("total samples must be a multiple of 4: adjusting samples per period...")
                self.samples_per_period += (
                    4 - self.samples_per_period % 4
                )  # round up to the nearest multiple of 4
            self.sampling_frequency = int(np.ceil(self.samples_per_period * self.clock_frequency))


        else:
            self.samples_per_period = int(np.ceil(self.sampling_frequency / self.clock_frequency))
            
        self.buffer_size = self.set_buffer_size()

    def set_buffer_size(self):
        buff_size = (NUM_BITS + 2 * NUM_BITS_PADDING) * self.samples_per_period
        if buff_size % 4 != 0:
            raise ValueError(
                "ValueError: TotalSamplesError: buffer size is not a multiple of 4: cannot resolve conflict"
            )
        return buff_size



def generate_clock_signal(channel, samples_per_period):
    duty_cycle = 0.5
    padding_lst_clk = [0] * int(2 * NUM_BITS_PADDING)
    clk_signal = [(i + 1) % 2 for i in range(1300)]
    clk_signal = padding_lst_clk + clk_signal + padding_lst_clk
    clk_signal = np.repeat(clk_signal, (samples_per_period // 2))
    # clk_signal = np.arange(samples_per_period) < (duty_cycle * samples_per_period)
    buffer_clk = list(
        map(lambda s: int(s) << channel, clk_signal)
    )  # shift the signal to the correct channel
    # buffer_clk = np.tile(buffer_clk, int(NUM_BITS)).tolist() # repeat the clock signal BUFFER_SIZE times
    # buffer_clk = padding_lst + buffer_clk + padding_lst
    return np.array(buffer_clk)


def generate_data_signal(channel, bitstream, samples_per_period):
    padding_lst = [0] * NUM_BITS_PADDING
    bitstream = padding_lst + bitstream + padding_lst
    data_signal = np.repeat(bitstream, samples_per_period)  # repeat each bit in the bitstream samples_per_period times
    buffer_data = list(map(lambda s: int(s) << channel, data_signal))
    return np.array(buffer_data)


def generate_enable_signal(channel, samples_per_period):
    padding_lst = [0] * NUM_BITS_PADDING
    enable_signal = padding_lst + ([1] * NUM_BITS) + padding_lst
    enable_signal = np.repeat(enable_signal, samples_per_period)
    buffer_enable = list(map(lambda s: int(s) << channel, enable_signal))
    return np.array(buffer_enable)


def generate_buffer(channels, bitstream, sampling_params: SamplingParams):
    samples_per_period = sampling_params.samples_per_period
    channel_enable, channel_clk, channel_data = channels
    clock_samples = generate_clock_signal(channel_clk, samples_per_period)
    data_samples = generate_data_signal(channel_data, bitstream, samples_per_period)
    enable_samples = generate_enable_signal(channel_enable, samples_per_period)
    buffer = (clock_samples + data_samples + enable_samples).tolist()
    return buffer


# def main():
#     mota_stream_tst = BitStream("mota_stream_tst")
#     mota_stream_tst.netlistInput("netlist_catalog/mota_schem_nl.txt")
#     mota_stream_tst.generateBits()
#     teststream = mota_stream_tst.bitstream

#     channels = [DIGITAL_CH_ENABLE, DIGITAL_CH_CLK, DIGITAL_CH_DATA]
#     sampling_params = SamplingParams(samples_per_period)
#     buffer = generate_streamout(0, channels, teststream, sampling_params)

#     ctx = libm2k.m2kOpen("usb:1.6.5")
#     led_state = ctx.setLed(False)
#     if ctx is None:
#         raise ConnectionError(
#             "Connection Error: No ADALM2000 device available/connected to your PC."
#         )

#     digital = ctx.getDigital()
#     digital.reset()

#     ctx.calibrateADC()
#     ctx.calibrateDAC()

#     print("configuring digital channels...")
#     digital.setOutputMode(DIGITAL_CH_ENABLE, libm2k.DIO_PUSHPULL)
#     digital.setDirection(DIGITAL_CH_ENABLE, libm2k.DIO_OUTPUT)
#     digital.setValueRaw(DIGITAL_CH_ENABLE, libm2k.LOW)
#     digital.enableChannel(DIGITAL_CH_ENABLE, True)
#     digital.setOutputMode(DIGITAL_CH_CLK, libm2k.DIO_PUSHPULL)
#     digital.setDirection(DIGITAL_CH_CLK, libm2k.DIO_OUTPUT)
#     digital.setValueRaw(DIGITAL_CH_CLK, libm2k.LOW)
#     digital.enableChannel(DIGITAL_CH_CLK, True)
#     digital.setOutputMode(DIGITAL_CH_DATA, libm2k.DIO_PUSHPULL)
#     digital.setDirection(DIGITAL_CH_DATA, libm2k.DIO_OUTPUT)
#     digital.setValueRaw(DIGITAL_CH_DATA, libm2k.LOW)
#     digital.enableChannel(DIGITAL_CH_DATA, True)

#     digital_ch_read = [3, 4, 5]
#     digital.setDirection(digital_ch_read[DIGITAL_CH_ENABLE], libm2k.DIO_INPUT)
#     digital.enableChannel(digital_ch_read[DIGITAL_CH_ENABLE], False)
#     digital.setDirection(digital_ch_read[DIGITAL_CH_CLK], libm2k.DIO_INPUT)
#     digital.enableChannel(digital_ch_read[DIGITAL_CH_CLK], False)
#     digital.setDirection(digital_ch_read[DIGITAL_CH_DATA], libm2k.DIO_INPUT)
#     digital.enableChannel(digital_ch_read[DIGITAL_CH_DATA], False)

#     digital.setCyclic(False)
#     digital.setSampleRateOut(sampling_params.sampling_frequency)
#     digital.setSampleRateIn(sampling_params.sampling_frequency)

#     trig = digital.getTrigger()
#     trig.reset()
#     trig.setDigitalDelay(0)
#     trig.setDigitalSource(libm2k.SRC_NONE)
#     trig.setDigitalCondition(DIGITAL_CH_ENABLE, libm2k.RISING_EDGE_DIGITAL)
#     if trig.hasExternalTriggerOut():
#         trig.setAnalogExternalOutSelect(libm2k.SELECT_DIGITAL_IN)
#     print("channels configured")
#     print(
#         "ENABLE channelS [w, rd]: {}".format(
#             [DIGITAL_CH_ENABLE, digital_ch_read[DIGITAL_CH_ENABLE]]
#         )
#     )
#     print(
#         "CLOCK channelS [w, rd]: {}".format(
#             [DIGITAL_CH_CLK, digital_ch_read[DIGITAL_CH_CLK]]
#         )
#     )
#     print(
#         "DATA channelS [w, rd]: {}".format(
#             [DIGITAL_CH_DATA, digital_ch_read[DIGITAL_CH_DATA]]
#         )
#     )

#     print("starting acquisition...")
#     digital.startAcquisition(sampling_params.buffer_size)
#     digital.push(buffer)
#     digital_data = digital.getSamples(sampling_params.buffer_size)
#     digital.stopAcquisition()
#     # print(buffer)
#     # print(digital_data)
#     print("acquisition complete")
#     time.sleep(0.1)
#     libm2k.contextClose(ctx)
#     OFFSET = 1.5
#     print("plotting data...")
#     digital_enable_read = list(
#         map(
#             lambda s: ((0x0001 << digital_ch_read[DIGITAL_CH_ENABLE]) & int(s))
#             >> digital_ch_read[DIGITAL_CH_ENABLE],
#             digital_data,
#         )
#     )
#     digital_clk_read = list(
#         map(
#             lambda s: ((0x0001 << digital_ch_read[DIGITAL_CH_CLK]) & int(s))
#             >> digital_ch_read[DIGITAL_CH_CLK],
#             digital_data,
#         )
#     )
#     digital_data_read = list(
#         map(
#             lambda s: ((0x0001 << digital_ch_read[DIGITAL_CH_DATA]) & int(s))
#             >> digital_ch_read[DIGITAL_CH_DATA],
#             digital_data,
#         )
#     )
#     # dio_enable = [(s >> DIGITAL_CH_ENABLE) & 1 for s in buffer]
#     # dio_clk = [(s >> DIGITAL_CH_CLK) & 1 for s in buffer]
#     # dio_data = [(s >> DIGITAL_CH_DATA) & 1 for s in buffer]
#     # print(digital_data_read)
#     time.sleep(0.1)
#     libm2k.contextClose(ctx)
#     OFFSET = 1.5
#     plt.plot(np.array(digital_clk_read) + OFFSET, label="CLOCK", color="#1f77b4")
#     plt.plot(np.array(digital_data_read), label="DATA", color="magenta")
#     plt.plot(np.array(digital_enable_read) + 2 * OFFSET, label="ENABLE", color="red")
#     plt.legend(loc="best")
#     plt.xlabel("Sample")
#     plt.tight_layout(h_pad=0.5)
#     plt.grid(True)
#     plt.show()

#     # time.sleep(0.1)
#     # libm2k.contextClose(ctx)


# if __name__ == "__main__":
#     main()

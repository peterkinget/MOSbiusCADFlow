# This program generates DATA, CLK, and ENABLE signals on the ADALM2000's digital outputs
# to configure the mobius chip according to the 650 bit DATA specified in the variable "bitstream"

# This configuration assumes the following serial protocol:
# 1. when the enable signal is high, the shift register is enabled and the switch matrix is disabled (and vice versa)
# 2. a new bit is loaded into the shift register on the rising edge of every clock cycle

# The application will generate a bitstream on DIO2, a clock signal on DIO1, and an enable signal on DIO0 of the ADALM2000(M2K)

import libm2k
import matplotlib.pyplot as plt
import numpy as np
import time
from BitStream import BitStream

DIGITAL_CH_ENABLE = 0
DIGITAL_CH_CLK = 1
DIGITAL_CH_DATA = 2

CLK_FREQUENCY = 500000

NUM_BITS = 650
BUFFER_SIZE = 650 + (650 % 4) + 100  # 650 bits + padding to nearest multiple of 4


def compute_sampling_frequency(samples_per_period):
    if samples_per_period < 2:
        raise ValueError(
            "ValueError: NyquistSamplingError: number of samples per period must be greater than or equal to 2."
        )
    period = 1 / CLK_FREQUENCY
    sampling_frequency = int(np.ceil(samples_per_period / period))
    return sampling_frequency


def compute_samples_per_period(sampling_frequency):
    period = 1 / CLK_FREQUENCY
    global samples_per_period
    samples_per_period = int(np.ceil(period * sampling_frequency))
    return samples_per_period


def generate_streamout(digital, channels, sampling_frequency, bitstream):
    channel_enable = channels[0]
    channel_clk = channels[1]
    channel_data = channels[2]

    nb_zero_pad = BUFFER_SIZE - NUM_BITS
    zero_pad_half = int(nb_zero_pad / 2)
    zero_pad_half_lst = [0] * zero_pad_half

    def generate_clock_signal(digital, channel):
        duty_cycle = 0.5
        clk_signal = (
            np.arange(samples_per_period) < duty_cycle * samples_per_period
        )  # generate a square wave with a duty cycle of 50%
        print(clk_signal)
        buffer_clk = list(
            map(lambda s: int(s) << channel, clk_signal)
        )  # shift the signal to the correct channel
        buffer_clk = np.tile(
            buffer_clk, int(BUFFER_SIZE)
        )  # repeat the clock signal BUFFER_SIZE times
        buffer_clk = buffer_clk.tolist()
        return buffer_clk

    def generate_data_signal(digital, channel, bitstream):
        bitstream = zero_pad_half_lst + bitstream + zero_pad_half_lst
        print(bitstream)
        data_signal = np.repeat(
            bitstream, samples_per_period
        )  # repeat each bit at consecutive indices samples_per_period times
        buffer_data = list(
            map(lambda s: int(s) << channel, data_signal)
        )  # shift the signal to the correct channel
        return buffer_data

    def generate_enable_signal(digital, channel):
        enable_signal = zero_pad_half_lst + [1] * 650 + zero_pad_half_lst
        enable_signal = np.repeat(enable_signal, samples_per_period)
        print(enable_signal)
        buffer_enable = list(map(lambda s: int(s) << channel, enable_signal))
        return buffer_enable

    clock_samples = np.array(generate_clock_signal(digital, channel_clk))
    data_samples = np.array(generate_data_signal(digital, channel_data, bitstream))
    enable_samples = np.array(generate_enable_signal(digital, channel_enable))

    buffer = clock_samples + data_samples + enable_samples
    buffer = buffer.tolist()
    # digital.push(buffer)


mota_stream_tst = BitStream("mota_stream_tst")
mota_stream_tst.netlistInput(
    "C:/Users/Cglee/Onedrive/Desktop/MOBIUS/mobius_2023/DDFlow2/netlist_catalog/mota_schem_nl.txt"
)
mota_stream_tst.generateBits()
teststream = mota_stream_tst.bitstream
print(teststream)

sampling_frequency_out = compute_sampling_frequency(40)
samples_per_period = compute_samples_per_period(sampling_frequency_out)
channels = [DIGITAL_CH_ENABLE, DIGITAL_CH_CLK, DIGITAL_CH_DATA]
buffer = generate_streamout(0, channels, sampling_frequency_out, teststream)
print(buffer)

dio_enable = list(
    map(
        lambda s: (((0x0001 << DIGITAL_CH_ENABLE) & int(s)) >> DIGITAL_CH_ENABLE),
        buffer,
    )
)
dio_clk = list(
    map(lambda s: ((0x0001 << DIGITAL_CH_CLK) & int(s)) >> DIGITAL_CH_CLK, buffer)
)
dio_data = list(
    map(lambda s: ((0x0001 << DIGITAL_CH_DATA) & int(s)) >> DIGITAL_CH_DATA, buffer)
)

OFFSET = 4
plt.plot(np.array(dio_enable), label="ENABLE")
plt.plot(np.array(dio_clk) + OFFSET, label="CLOCK")
plt.plot(np.array(dio_data) + 2 * OFFSET, label="CLOCK")

plt.legend(loc="lower right")
plt.grid(True)
plt.show()

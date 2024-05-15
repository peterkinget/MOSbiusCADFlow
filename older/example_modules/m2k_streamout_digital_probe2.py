import libm2k
import matplotlib.pyplot as plt
import time
import numpy as np
import sys

sys.path.append("../generation_modules/src")

from BitStream import BitStream
from m2k_streamout_utils2 import optimize_params, generate_buffer

# sampling constraints

MAX_SAMPLE_RATE = 100000000  # 100 MS/s (m2k digital sampling rate)
MAX_BIT_RATE = 500000  # 500 kbps / 500 kHz (bitstream bit rate = shift register clock frequency)
MAX_SIM_TIME = 1  # 1 second (stream time)

# digital output channels

DCH_W_ENABLE = 0
DCH_W_CLK = 1
DCH_W_DATA = 2

# digital input channels

DCH_RD_ENABLE = 3
DCH_RD_CLK = 4
DCH_RD_DATA = 5

# generate mota bitstream from netlist

mota_example = BitStream("mota_example")
mota_example.netlistInput("netlist_catalog/mota_schem_nl.txt")
mota_example.generateBits()
mota_bitstream = mota_example.bitstream

# generate digital output for m2k streamout from bitstream

channels = [DCH_W_ENABLE, DCH_W_CLK, DCH_W_DATA]
mota_sampling_params = optimize_params(MAX_SAMPLE_RATE, MAX_BIT_RATE, MAX_SIM_TIME)
buffer = generate_buffer(channels, mota_bitstream, mota_sampling_params)
digital_sampling_freq = mota_sampling_params.sampling_frequency
bit_rate = mota_sampling_params.clock_frequency
samples_per_period = mota_sampling_params.samples_per_period
buffer_size = mota_sampling_params.buffer_size

print("\nstreamout parameters:")
print("digital IO sampling frequency: {} MHz".format(digital_sampling_freq / 1000000))
print("clock frequency / bit rate {} kHz".format(bit_rate / 1000))
print("samples per period: {} ".format(samples_per_period))
print("buffer size: {} samples".format(buffer_size))
print("stream length: {} ms\n".format(buffer_size / digital_sampling_freq * 1000))

# connect to m2k and configure digital channels

pause = 0.5
ctx = libm2k.m2kOpen()
time.sleep(pause)
if ctx is None:
    raise ConnectionError(
        "Connection Error: No ADALM2000 device available/connected to your PC."
    )

uri = ctx.getUri()
print("connected to ADALM2000 device: ["'"{}"'"]\n".format(uri))

digital = ctx.getDigital()
digital.reset()
time.sleep(pause)
print("disconnect all analog IO channels before calibration!")
time.sleep(pause)
can_calibrate = input("ready to calibrate ([y]/n)?")

if can_calibrate != "y":
    libm2k.contextClose(ctx, True)
    raise ConnectionError(
        "CalibrationError: analog IO channels not disconnected. Streamout terminated."
    )

ctx.calibrateADC()
ctx.calibrateDAC()
time.sleep(pause)
print("\nconfiguring digital channels...")

digital.setOutputMode(DCH_W_ENABLE, libm2k.DIO_PUSHPULL)
digital.setDirection(DCH_W_ENABLE, libm2k.DIO_OUTPUT)
digital.setValueRaw(DCH_W_ENABLE, libm2k.LOW)
digital.enableChannel(DCH_W_ENABLE, True)
digital.setOutputMode(DCH_W_CLK, libm2k.DIO_PUSHPULL)
digital.setDirection(DCH_W_CLK, libm2k.DIO_OUTPUT)
digital.setValueRaw(DCH_W_CLK, libm2k.LOW)
digital.enableChannel(DCH_W_CLK, True)
digital.setOutputMode(DCH_W_DATA, libm2k.DIO_PUSHPULL)
digital.setDirection(DCH_W_DATA, libm2k.DIO_OUTPUT)
digital.setValueRaw(DCH_W_DATA, libm2k.LOW)
digital.enableChannel(DCH_W_DATA, True)

digital.setDirection(DCH_RD_ENABLE, libm2k.DIO_INPUT)
digital.enableChannel(DCH_RD_ENABLE, False)
digital.setDirection(DCH_RD_CLK, libm2k.DIO_INPUT)
digital.enableChannel(DCH_RD_CLK, False)
digital.setDirection(DCH_RD_DATA, libm2k.DIO_INPUT)
digital.enableChannel(DCH_RD_DATA, False)

digital.setCyclic(False)
digital.setSampleRateOut(digital_sampling_freq)
digital.setSampleRateIn(digital_sampling_freq)

# configure trigger

trig = digital.getTrigger()
trig.reset()
trig.setDigitalDelay(0)
trig.setDigitalSource(libm2k.SRC_NONE)
trig.setDigitalCondition(DCH_W_ENABLE, libm2k.RISING_EDGE_DIGITAL)
if trig.hasExternalTriggerOut():
    trig.setAnalogExternalOutSelect(libm2k.SELECT_DIGITAL_IN)
    
time.sleep(pause)

print("ENABLE IO channels [Wr, Rd]: {}".format([DCH_W_ENABLE, DCH_RD_ENABLE]))
print("CLOCK IO channels [Wr, Rd]: {}".format([DCH_W_CLK, DCH_RD_CLK]))
print("DATA  IO channels [Wr, Rd]: {}".format([DCH_W_DATA, DCH_RD_DATA]))

# start acquisition

time.sleep(pause)

print("\nstarting acquisition...")

digital.startAcquisition(buffer_size)
digital.push(buffer)
digital_data = digital.getSamples(buffer_size)
digital.stopAcquisition()

print("acquisition complete -- > context closed")

libm2k.contextClose(ctx, True)

time.sleep(pause)

# extract and plot data

time.sleep(pause)

print("\nextracting data...")

digital_enable_read = list(
    map(lambda s: ((0x0001 << DCH_RD_ENABLE) & int(s)) >> DCH_RD_ENABLE, digital_data)
)
digital_clk_read = list(
    map(lambda s: ((0x0001 << DCH_RD_CLK) & int(s)) >> DCH_RD_CLK, digital_data)
)
digital_data_read = list(
    map(lambda s: ((0x0001 << DCH_RD_DATA) & int(s)) >> DCH_RD_DATA, digital_data)
)

print("\nplotting input channels...")

OFFSET = 1.5
time_step = (1 / digital_sampling_freq) *1000 # in ms
stop_time = buffer_size * time_step
time_axis = np.arange(0, stop_time, time_step, dtype=float)

plt.plot(time_axis, np.array(digital_data_read), label="DATA", color="magenta")
plt.plot(time_axis, np.array(digital_clk_read) + OFFSET, label="CLOCK", color="#1f77b4")
plt.plot(time_axis, np.array(digital_enable_read) + 2 * OFFSET, label="ENABLE", color="red")

plt.legend(loc="lower left", reverse = True)
plt.xlabel("Time (ms)")
plt.grid(True)
plt.tight_layout(h_pad=0.5)
plt.show()

print("plot closed")

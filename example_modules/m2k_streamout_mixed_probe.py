import libm2k
import matplotlib.pyplot as plt
import time
import numpy as np

import sys
sys.path.append("generation_modules/src")

from BitStream import BitStream
from m2k_streamout_utils2 import generate_buffer, get_available_sampling_params

# sampling constraints

MAX_SAMPLE_RATE = 100000000  # 100 MS/s (m2k max sampling rate)
MAX_BIT_RATE = 500000  # 500 kbps / 500 kHz (bitstream bit rate = shift register clock frequency)
MAX_SIM_TIME = 1  # 1 second (stream time)

# digital output channels

DCH_W_ENABLE = 13
DCH_W_CLK = 12
DCH_W_DATA = 11

# digital input channels

DCH_RD_ENABLE = 2
DCH_RD_CLK = 1
DCH_RD_DATA = 0

# analog input channels

ACH_RD_0 = 0
ACH_RD_1 = 1

# generate mota bitstream from netlist

cm_swmxtst = BitStream()
cm_swmxtst.netlistInput("circuit_data/netlist_catalog/test_schem_inv_nl.txt")
cm_swmxtst.generateBitstream()
cm_bitstream = cm_swmxtst.bitstream


# generate digital output for m2k streamout from bitstream

channels = [DCH_W_ENABLE, DCH_W_CLK, DCH_W_DATA]
# fclk = 500000
# fsample = 25000000
# samples_per_period, buffer_size = generate_sample_params(fclk, fsample)
# buffer = generate_buffer(channels, cm_bitstream, samples_per_period)
# digital_sampling_freq = fsample
# bit_rate = fclk


# print("\nstreamout parameters:")
# print("digital IO sampling frequency: {} MHz".format(digital_sampling_freq / 1000000))
# print("clock frequency / bit rate {} kHz".format(bit_rate / 1000))
# print("samples per period: {} ".format(samples_per_period))
# print("buffer size: {} samples".format(buffer_size))
# print("stream length: {} ms\n".format(buffer_size / digital_sampling_freq * 1000))

# connect to m2k and configure digital channels
pause = 0.2

ctx = libm2k.m2kOpen()
time.sleep(pause)
libm2k.contextClose(ctx, True)
time.sleep(pause)
ctx = libm2k.m2kOpen()
time.sleep(pause)

if ctx is None:
    raise ConnectionError(
        "Connection Error: No ADALM2000 device available/connected to your PC."
    )

uri = ctx.getUri()
print("connected to ADALM2000 device: ["'"{}"'"]\n".format(uri))

if ctx.hasMixedSignal() is False:
    print("Error: Firmware does not support mixed signal mode.")
    exit(1)

digital = ctx.getDigital()
analog_in = ctx.getAnalogIn()
ps = ctx.getPowerSupply()
ps.reset()
ps.enableChannel(0, True)
ps.pushChannel(0, 2.5)

digital.reset()
analog_in.reset()

# time.sleep(30)
print("disconnect all analog IO channels before calibration!")
time.sleep(pause)
can_calibrate = input("analog IO disconnected ([y]/n)?")

if can_calibrate != "y":
    libm2k.contextClose(ctx, True)
    raise ConnectionError(
        "CalibrationError: analog IO channels not disconnected. Streamout terminated."
    )

ctx.calibrateADC()
ctx.calibrateDAC()

input("press enter to continue...")
time.sleep(pause)
print("\nconfiguring digital channels...")
for i in range(3):
    
    digital.setOutputMode(DCH_W_ENABLE+i, libm2k.DIO_OPENDRAIN)
    digital.setDirection(DCH_W_ENABLE+i, libm2k.DIO_OUTPUT)
    digital.setValueRaw(DCH_W_ENABLE+i, libm2k.HIGH)
    digital.enableChannel(DCH_W_ENABLE+i, True)
    
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
# digital.setSampleRateOut(digital_sampling_freq)
# digital.setSampleRateIn(digital_sampling_freq)

# configure analog input channels

analog_in.enableChannel(ACH_RD_0, True)
analog_in.enableChannel(ACH_RD_1, True)
# analog_in.setSampleRate(MAX_SAMPLE_RATE)
# analog_in.setOversamplingRatio(MAX_SAMPLE_RATE // digital_sampling_freq)

# configure trigger
# atrig = analog_in.getTrigger()
# atrig.reset()

# atrig.setAnalogSource(ACH_RD_0)
# atrig.setAnalogMode(ACH_RD_0, libm2k.ANALOG)
# atrig.setAnalogLevel(ACH_RD_0, 1)
# atrig.setAnalogCondition(ACH_RD_0, libm2k.RISING_EDGE_ANALOG)
# atrig.setDigitalCondition(DCH_RD_ENABLE, libm2k.SRC_NONE)

dtrig = digital.getTrigger()
dtrig.reset()
dtrig.setDigitalDelay(0)
dtrig.setDigitalSource(libm2k.SRC_NONE)
dtrig.setDigitalCondition(DCH_W_ENABLE, libm2k.FALLING_EDGE_DIGITAL)
if dtrig.hasExternalTriggerOut():
    dtrig.setAnalogExternalOutSelect(libm2k.SELECT_DIGITAL_IN)
    
time.sleep(pause)

print("ENABLE IO channels [Wr, Rd]: {}".format([DCH_W_ENABLE, DCH_RD_ENABLE]))
print("CLOCK IO channels [Wr, Rd]: {}".format([DCH_W_CLK, DCH_RD_CLK]))
print("DATA  IO channels [Wr, Rd]: {}".format([DCH_W_DATA, DCH_RD_DATA]))
params_list = []
for i, p in enumerate(get_available_sampling_params(digital, 32000)):
    print((p, i))
    params_list.append((p[0], p[1], p[2], p[3]))
digital_sampling_freq, bit_rate, samples_per_period, buffer_size = params_list[int(input("select sampling params index: "))]
# start acquisition

# print(digital.getSampleRateOut(), digital.getSampleRateIn())
# if digital.getSampleRateOut() != digital_sampling_freq:
#     samples_per_period, buffer_size = generate_sample_params(500000, digital.getSampleRateOut())
#     buffer = generate_buffer(channels, cm_bitstream, samples_per_period)
#     digital_sampling_freq = fsample
#     bit_rate = fclk
print(analog_in.getAvailableSampleRates())
analog_sampling_freq = analog_in.setSampleRate(int(input("select analog sampling frequency: ")))
oversampling_ratio =   int(analog_sampling_freq // digital_sampling_freq)    
digital.setSampleRateOut(digital_sampling_freq)
digital.setSampleRateIn(digital_sampling_freq)
analog_in.setSampleRate(analog_sampling_freq)
analog_in.setOversamplingRatio(oversampling_ratio)
buffer = generate_buffer(channels, cm_bitstream, samples_per_period)
print("\nstreamout parameters:")
print("digital IO sampling frequency: {} MHz".format(digital_sampling_freq / 1000000))
print("clock frequency / bit rate {} kHz".format(bit_rate / 1000))
print("samples per period: {} ".format(samples_per_period))
print("buffer size: {} samples".format(buffer_size))
print("stream length: {} ms\n".format(buffer_size / digital_sampling_freq * 1000))

print("\nstarting acquisition...")

ctx.startMixedSignalAcquisition(buffer_size)
digital.push(buffer)
# digital.setValueRaw(DCH_W_ENABLE, libm2k.HIGH)
digital_data, analog_data = [], []
digital_data.extend(digital.getSamples(buffer_size))
analog_data.extend(analog_in.getSamples(buffer_size))
ctx.stopMixedSignalAcquisition()

# libm2k.contextClose(ctx, True)

print("acquisition complete -- > context closed")

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
print(len(time_axis), len(analog_data[0]), len(analog_data[1]))

plt.plot(time_axis, np.array(digital_data_read) + 6, label="DATA-DRD", color="magenta")
plt.plot(time_axis, np.array(digital_clk_read) + 7, label="CLOCK-DRD", color="#1f77b4")
plt.plot(time_axis, np.array(digital_enable_read) + 8, label="ENABLE-DRD", color="red")
plt.plot(time_axis, np.array(analog_data[1])+2.5, label="DATA-ARD", color="blue")
plt.plot(time_axis, np.array(analog_data[0]), label="CLOCK-ARD", color="green")


plt.legend(loc="lower left", reverse = True)
plt.xlabel("Time (ms)")
plt.grid(True)
plt.tight_layout(h_pad=0.5)
plt.show()

print("plot closed")

import numpy as np
from typing import List




DIGITAL_CH_ENABLE = 0
DIGITAL_CH_CLK = 1
DIGITAL_CH_DATA = 2


NUM_BITS = 650
NUM_BITS_PADDING = 0  # padding clock cycles for the start and end of the buffer



class SamplingParams:
    def __init__(self, clock_frequency: int = 500000, samples_per_period: int = 0, sampling_frequency: int = 0):
        self.clock_frequency = clock_frequency
        self.samples_per_period = samples_per_period
        self.sampling_frequency = sampling_frequency
        self.buffer_size = None
        self.num_symm_padding_bits = NUM_BITS_PADDING

        if self.samples_per_period == 0 and self.sampling_frequency == 0:
            raise ValueError(
                "Must specify either samples_per_period or sampling_frequency"
            )

        elif self.samples_per_period != 0 and self.sampling_frequency != 0:
            # self.clock_frequency = self.sampling_frequency / self.samples_per_period
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
                self.samples_per_period -= self.samples_per_period % 4
                self.samples_per_period += (
                    4 - self.samples_per_period % 4
                )  # round up to the nearest multiple of 4
            self.sampling_frequency = int(np.ceil(self.samples_per_period * self.clock_frequency))

        else:
            self.samples_per_period = int(np.ceil(self.sampling_frequency / self.clock_frequency))
            
        self.buffer_size = self.set_buffer_size()

    def set_buffer_size(self):
        buff_size = (NUM_BITS + 2 * NUM_BITS_PADDING) * self.samples_per_period
        if buff_size > 64000:
            raise ValueError(
                "ValueError: TotalSamplesError: buffer size exceeds maximum memory depth of 32000 samples"
            )
        if buff_size % 4 != 0:
            raise ValueError(
                "ValueError: TotalSamplesError: buffer size is not a multiple of 4: cannot resolve conflict"
            )
        return buff_size




def generate_clock_signal(channel, samples_per_period):
    duty_cycle = 0.5
    padding_lst_clk = [0] * int(2 * NUM_BITS_PADDING)
    clk_signal = [(i + 1) % 2 for i in range(NUM_BITS * 2)] # generate 1,0 pattern for each bit to represent clock period
    clk_signal = ([0] * 2) + clk_signal + ([0] * 2) # trigger start with 1, end with 0 (each for a full clock period)
    
    clk_signal = np.repeat(clk_signal, (samples_per_period // 2)) # extend each value from its current index in the list
    # clk_signal = np.arange(samples_per_period) < (duty_cycle * samples_per_period)
    buffer_clk = list(
        map(lambda s: int(s) << channel, clk_signal)
    )  # shift the signal to the correct channel
    # buffer_clk = np.tile(buffer_clk, int(NUM_BITS)).tolist() # repeat the clock signal BUFFER_SIZE times
    # buffer_clk = padding_lst + buffer_clk + padding_lst
    return np.array(buffer_clk)


def generate_data_signal(channel, bitstream, samples_per_period):
    padding_lst = [0] * NUM_BITS_PADDING
    bitstream = [0] + bitstream + [0]
    data_signal = np.repeat(bitstream, samples_per_period)  # repeat each bit in the bitstream samples_per_period times
    buffer_data = list(map(lambda s: int(s) << channel, data_signal))
    return np.array(buffer_data)


def generate_enable_signal(channel, samples_per_period):
    padding_lst = [0] * NUM_BITS_PADDING
    enable_signal = [0] + ([0] * NUM_BITS) + [1]
    enable_signal = np.repeat(enable_signal, samples_per_period)
    buffer_enable1 = list(map(lambda s: int(s) << channel, enable_signal))
    buffer_enable2 = list(map(lambda s: int(s) << channel+1, enable_signal))
    buffer_enable3 = list(map(lambda s: int(s) << channel+2, enable_signal))
    buffer_enable = np.array(buffer_enable1) + np.array(buffer_enable2) + np.array(buffer_enable3)
    
    return buffer_enable

def generate_trigger_signal(channel, samples_per_period):
    trigger_signal = [1] + ([0] * NUM_BITS) + [1]
    trigger_signal = np.repeat(trigger_signal, samples_per_period)
    buffer_trigger = list(map(lambda s: int(s) << channel, trigger_signal))
    return np.array(buffer_trigger)


def generate_buffer(channels: List[int], bitstream: List[int], samples_per_period: int):
    samples_per_period = samples_per_period
    channel_enable, channel_clk, channel_data, channel_trigger = channels
    clock_samples = generate_clock_signal(channel_clk, samples_per_period)
    data_samples = generate_data_signal(channel_data, bitstream, samples_per_period)
    enable_samples = generate_enable_signal(channel_enable, samples_per_period)
    trigger_samples = generate_trigger_signal(channel_trigger, samples_per_period)
    buffer = (clock_samples + data_samples + enable_samples).tolist()
    return buffer

def optimize_params(max_sampling_frequency: int, max_clock_frequency: int, max_sim_time: int):
    min_samples_per_period = 2
    min_clock_frequency = NUM_BITS / max_sim_time
    # Calculate the maximum possible samples per period
    max_samples_per_period = int(np.floor(max_sampling_frequency / max_clock_frequency))

    # Calculate the minimum possible sampling frequency
    min_sampling_frequency = int(np.ceil(min_samples_per_period * min_clock_frequency))

    # Calculate the optimal samples per period and sampling frequency
    samples_per_period = max_samples_per_period
    sampling_frequency = max_sampling_frequency
    while samples_per_period > min_samples_per_period and sampling_frequency > min_sampling_frequency:
        clock_frequency = sampling_frequency / samples_per_period
        if clock_frequency < min_clock_frequency:
            break
        try:
            params = SamplingParams(clock_frequency=clock_frequency, samples_per_period=samples_per_period)
            return params
        except ValueError:
            pass
        samples_per_period -= 4
        sampling_frequency = int(np.ceil(samples_per_period * max_clock_frequency // 1))

    # If no valid parameters are found, raise an exception
    raise ValueError("Cannot find valid parameters")

def generate_sample_params(fclock: int, fsample: int):
    samples_per_period = int(np.ceil(fsample / fclock))
    buff_size = (NUM_BITS + 2) * samples_per_period
    if buff_size > 64000:
        print("Warning: buffer size exceeds maximum memory depth of 32000 samples by {} samples".format(buff_size - 32000))
        # raise ValueError(
        #     "ValueError: TotalSamplesError: buffer size exceeds maximum memory depth of 32000 samples"
        # )
    if buff_size % 4 != 0:
        raise ValueError(
            "ValueError: TotalSamplesError: buffer size is not a multiple of 4: cannot resolve conflict"
        )
        
    return(samples_per_period, buff_size)

def get_available_sampling_params(ctx_digital, mem_depth_max):
    fs_list = []
    base_list = [int(100e6), int(10e6), int(1e6)]
    for fb in base_list:
        fs_list.append(int(ctx_digital.setSampleRateOut(fb)))
        fs_list.append(int(ctx_digital.setSampleRateOut(fb // 2)))
        fs_list.append(int(ctx_digital.setSampleRateOut(fb // 4)))
    for fs in fs_list:
        n=4
        while n <= mem_depth_max // 652:
            total_samples = n * 652
            fclk = fs / n
            if total_samples % 4 == 0 and fclk == int(fclk):
                stream_time = (total_samples / fs) * 1000 # in ms
                yield(fs, int(fclk), n, total_samples, stream_time)
            n += 2
    
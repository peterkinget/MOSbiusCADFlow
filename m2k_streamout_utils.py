import numpy as np
from typing import List, Tuple, Union
import libm2k

MAX_SAMPLE_RATE = 100000000  # 100 MS/s (m2k max digital/ADC sampling rate)
MAX_BIT_RATE = 500000  # 500 kbps / 500 kHz (bit rate = clock frequency)
MAX_SIM_TIME = 1  # 1 second (stream time)

NUM_BITS = 650
NUM_BITS_PADDING = 5  # padding clock cycles for the start and end of the buffer


class SamplingParams:
    def __init__(
        self,
        clock_frequency: int = 500000,
        samples_per_period: int = 0,
        sampling_frequency: int = 0,
    ):
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
            if (
                self.sampling_frequency / self.samples_per_period
                != self.clock_frequency
            ):
                raise ValueError(
                    "Sampling frequency and samples per period are not compatible with clock frequency ({} kHz)".format(
                        self.clock_frequency // 1000
                    )
                )
            else:
                pass

        elif self.samples_per_period != 0:
            if self.samples_per_period % 4 != 0:
                print(
                    "total samples must be a multiple of 4: adjusting samples per period..."
                )
                self.samples_per_period += (
                    4 - self.samples_per_period % 4
                )  # round up to the nearest multiple of 4
            self.sampling_frequency = int(
                np.ceil(self.samples_per_period * self.clock_frequency)
            )

        else:
            self.samples_per_period = int(
                np.ceil(self.sampling_frequency / self.clock_frequency)
            )

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


class StreamOutUtils:
    # set three class variables (MAX_SAMPLE_RATE, MAX_BIT_RATE, MAX_SIM_TIME)
    MAX_SAMPLE_RATE = MAX_SAMPLE_RATE
    MAX_BIT_RATE = MAX_BIT_RATE
    MAX_SIM_TIME = MAX_SIM_TIME

    @staticmethod
    def generate_clock_signal(channel, samples_per_period):
        duty_cycle = 0.5
        padding_lst_clk = [0] * int(2 * NUM_BITS_PADDING)
        clk_signal = [(i + 1) % 2 for i in range(1300)]
        clk_signal = padding_lst_clk + clk_signal + padding_lst_clk
        clk_signal = np.repeat(clk_signal, (samples_per_period // 2))
        buffer_clk = list(
            map(lambda s: int(s) << channel, clk_signal)
        )  # shift the signal to the correct channel
        return np.array(buffer_clk)

    @staticmethod
    def generate_data_signal(channel, bitstream, samples_per_period):
        padding_lst = [0] * NUM_BITS_PADDING
        bitstream = padding_lst + bitstream + padding_lst
        data_signal = np.repeat(
            bitstream, samples_per_period
        )  # repeat each bit in the bitstream samples_per_period times
        buffer_data = list(map(lambda s: int(s) << channel, data_signal))
        return np.array(buffer_data)

    @staticmethod
    def generate_enable_signal(channel, samples_per_period):
        padding_lst = [0] * NUM_BITS_PADDING
        enable_signal = padding_lst + ([1] * NUM_BITS) + padding_lst
        enable_signal = np.repeat(enable_signal, samples_per_period)
        buffer_enable = list(map(lambda s: int(s) << channel, enable_signal))
        return np.array(buffer_enable)

    @staticmethod
    def generate_buffer(
        channels: List[int], bitstream: List[int], sampling_params: SamplingParams
    ):
        samples_per_period = sampling_params.samples_per_period
        channel_enable, channel_clk, channel_data = channels
        clock_samples = StreamOutUtils.generate_clock_signal(
            channel_clk, samples_per_period
        )
        data_samples = StreamOutUtils.generate_data_signal(
            channel_data, bitstream, samples_per_period
        )
        enable_samples = StreamOutUtils.generate_enable_signal(
            channel_enable, samples_per_period
        )
        buffer = (clock_samples + data_samples + enable_samples).tolist()
        return buffer

    @staticmethod
    def optimize_params(
        max_sampling_frequency: int, max_clock_frequency: int, max_sim_time: int
    ):
        min_samples_per_period = 2
        min_clock_frequency = NUM_BITS / max_sim_time
        # Calculate the maximum possible samples per period
        max_samples_per_period = int(
            np.floor(max_sampling_frequency / max_clock_frequency)
        )

        # Calculate the minimum possible sampling frequency
        min_sampling_frequency = int(
            np.ceil(min_samples_per_period * min_clock_frequency)
        )

        # Calculate the optimal samples per period and sampling frequency
        samples_per_period = max_samples_per_period
        sampling_frequency = max_sampling_frequency
        while (
            samples_per_period > min_samples_per_period
            and sampling_frequency > min_sampling_frequency
        ):
            clock_frequency = sampling_frequency / samples_per_period
            if clock_frequency < min_clock_frequency:
                break
            try:
                params = SamplingParams(
                    clock_frequency=clock_frequency,
                    samples_per_period=samples_per_period,
                )
                return params
            except ValueError:
                pass
            samples_per_period -= 4
            sampling_frequency = int(np.ceil(samples_per_period * max_clock_frequency))

        # If no valid parameters are found, raise an exception
        raise ValueError("Cannot find valid parameters")

    @staticmethod
    def generate_sampling_params(
        clock_frequency: int = 500000,
        samples_per_period: int = 0,
        sampling_frequency: int = 0,
    ) -> SamplingParams:
        try:
            params = SamplingParams(
                clock_frequency=clock_frequency,
                samples_per_period=samples_per_period,
                sampling_frequency=sampling_frequency,
            )
            return params
        except ValueError:
            return StreamOutUtils.optimize_params(
                max_sampling_frequency=MAX_SAMPLE_RATE,
                max_clock_frequency=MAX_BIT_RATE,
                max_sim_time=MAX_SIM_TIME,
            )

    @staticmethod
    def configure_streamout_channels(
        ctx_m2kdigital: libm2k.M2kDigital,
        digital_sampling_frequency: int,
        channels: Union[List[int], Tuple[int, int, int]] = [0, 1, 2],
    ):
        digital = ctx_m2kdigital

        digital_sampling_freq = digital_sampling_frequency

        ch_en, ch_clk, ch_d = channels

        digital.reset()

        digital.setOutputMode(ch_en, libm2k.DIO_PUSHPULL)
        digital.setDirection(ch_en, libm2k.DIO_OUTPUT)
        digital.setValueRaw(ch_en, libm2k.LOW)
        digital.enableChannel(ch_en, True)
        digital.setOutputMode(ch_clk, libm2k.DIO_PUSHPULL)
        digital.setDirection(ch_clk, libm2k.DIO_OUTPUT)
        digital.setValueRaw(ch_clk, libm2k.LOW)
        digital.enableChannel(ch_clk, True)
        digital.setOutputMode(ch_d, libm2k.DIO_PUSHPULL)
        digital.setDirection(ch_d, libm2k.DIO_OUTPUT)
        digital.setValueRaw(ch_d, libm2k.LOW)
        digital.enableChannel(ch_d, True)

        digital.setCyclic(False)
        digital.setSampleRateOut(digital_sampling_freq)

        print("digital sample-rate out = {}".format(digital_sampling_freq))
        print("enable ch = {}".format(ch_en))
        print("clock ch = {}".format(ch_clk))
        print("data ch = {}".format(ch_d))

    @staticmethod
    def setAll(
        ctx_m2kdigital: libm2k.M2kDigital,
        bitstream: List[int],
        channels: List[int],
        clock_frequency: int = 500000,
        samples_per_period: int = 0,
        sampling_frequency: int = 0,
    ):
        # generate sampling parameters
        sampling_params = StreamOutUtils.generate_sampling_params(
            clock_frequency=clock_frequency,
            samples_per_period=samples_per_period,
            sampling_frequency=sampling_frequency,
        )

        # generate buffer
        buffer = StreamOutUtils.generate_buffer(
            channels=channels, bitstream=bitstream, sampling_params=sampling_params
        )

        # configure streamout channels
        StreamOutUtils.configure_streamout_channels(
            ctx_m2kdigital=ctx_m2kdigital,
            digital_sampling_frequency=sampling_params.sampling_frequency,
            channels=channels,
        )
        return buffer, sampling_params

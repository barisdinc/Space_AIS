#!/usr/bin/env python
##################################################
# Gnuradio Python Flow Graph
# Title: Space AIS Receiver Simulation
# Author: Baris DINC
# Description: Simulation platform for testing doppler effects and collision on AIS signal reception with LEO satellites
# Generated: Sun Feb  2 19:38:45 2020
##################################################

from gnuradio import analog
from gnuradio import blocks
from gnuradio import digital
from gnuradio import eng_notation
from gnuradio import gr
from gnuradio import uhd
from gnuradio import wxgui
from gnuradio.eng_option import eng_option
from gnuradio.fft import window
from gnuradio.filter import firdes
from gnuradio.wxgui import waterfallsink2
from grc_gnuradio import blks2 as grc_blks2
from grc_gnuradio import wxgui as grc_wxgui
from optparse import OptionParser
import AISTX
import threading
import time
import wx

class Space_AIS_RX(grc_wxgui.top_block_gui):

    def __init__(self):
        grc_wxgui.top_block_gui.__init__(self, title="Space AIS Receiver Simulation")
        _icon_path = "/usr/share/icons/hicolor/32x32/apps/gnuradio-grc.png"
        self.SetIcon(wx.Icon(_icon_path, wx.BITMAP_TYPE_ANY))

        ##################################################
        # Variables
        ##################################################
        self.samp_rate = samp_rate = 326531
        self.send_interval_freq_0 = send_interval_freq_0 = 0.2
        self.send_interval_freq = send_interval_freq = 0.2
        self.func_doppler_0 = func_doppler_0 = 0
        self.func_doppler = func_doppler = 0
        self.func_burst_out_0 = func_burst_out_0 = 0
        self.func_burst_out = func_burst_out = 0
        self.doppler_sensitivity = doppler_sensitivity = 30000
        self.doppler_control_freq1 = doppler_control_freq1 = 0.1
        self.channel_select = channel_select = 0
        self.bit_rate = bit_rate = 9600
        self.ais_burst_duration = ais_burst_duration = samp_rate/5

        ##################################################
        # Blocks
        ##################################################
        self.probe_doppler_0 = blocks.probe_signal_i()
        self.probe_doppler = blocks.probe_signal_i()
        self.probe_burst = blocks.probe_signal_i()
        self.probe_burst_0 = blocks.probe_signal_i()
        def _func_doppler_0_probe():
        	while True:
        		val = self.probe_doppler_0.level()
        		try: self.set_func_doppler_0(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(samp_rate))
        _func_doppler_0_thread = threading.Thread(target=_func_doppler_0_probe)
        _func_doppler_0_thread.daemon = True
        _func_doppler_0_thread.start()
        def _func_doppler_probe():
        	while True:
        		val = self.probe_doppler.level()
        		try: self.set_func_doppler(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(samp_rate))
        _func_doppler_thread = threading.Thread(target=_func_doppler_probe)
        _func_doppler_thread.daemon = True
        _func_doppler_thread.start()
        def _func_burst_out_probe():
        	while True:
        		val = self.probe_burst.level()
        		try: self.set_func_burst_out(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(samp_rate))
        _func_burst_out_thread = threading.Thread(target=_func_burst_out_probe)
        _func_burst_out_thread.daemon = True
        _func_burst_out_thread.start()
        self.wxgui_waterfallsink2_0_0 = waterfallsink2.waterfall_sink_c(
        	self.GetWin(),
        	baseband_freq=161900000,
        	dynamic_range=100,
        	ref_level=0,
        	ref_scale=2.0,
        	sample_rate=samp_rate,
        	fft_size=512,
        	fft_rate=15,
        	average=False,
        	avg_alpha=None,
        	title="Frequency Waterfall",
        	size=(400,400),
        )
        self.Add(self.wxgui_waterfallsink2_0_0.win)
        self.uhd_usrp_sink_0 = uhd.usrp_sink(
        	device_addr="",
        	stream_args=uhd.stream_args(
        		cpu_format="fc32",
        		channels=range(1),
        	),
        )
        self.uhd_usrp_sink_0.set_samp_rate(samp_rate)
        self.uhd_usrp_sink_0.set_center_freq(uhd.tune_request_t(161900000, 19000000), 0)
        self.uhd_usrp_sink_0.set_gain(20 if(func_burst_out>0) else 0, 0)
        self.uhd_usrp_sink_0.set_antenna("TX/RX", 0)
        self.source_txtimer_0 = analog.sig_source_i(samp_rate, analog.GR_SQR_WAVE, doppler_control_freq1, 1, 0)
        self.source_txtimer = analog.sig_source_i(samp_rate, analog.GR_SQR_WAVE, doppler_control_freq1/4, 1, 0)
        def _func_burst_out_0_probe():
        	while True:
        		val = self.probe_burst_0.level()
        		try: self.set_func_burst_out_0(val)
        		except AttributeError, e: pass
        		time.sleep(1.0/(samp_rate))
        _func_burst_out_0_thread = threading.Thread(target=_func_burst_out_0_probe)
        _func_burst_out_0_thread.daemon = True
        _func_burst_out_0_thread.start()
        self.digital_gmsk_mod_0_0 = digital.gmsk_mod(
        	samples_per_symbol=int(samp_rate/bit_rate),
        	bt=0.4,
        	verbose=False,
        	log=False,
        )
        self.digital_gmsk_mod_0 = digital.gmsk_mod(
        	samples_per_symbol=int(samp_rate/bit_rate),
        	bt=0.4,
        	verbose=False,
        	log=False,
        )
        self.blocks_vco_c_0_0_0 = blocks.vco_c(samp_rate, doppler_sensitivity*0.5, 1)
        self.blocks_vco_c_0_0 = blocks.vco_c(samp_rate, doppler_sensitivity, 1)
        self.blocks_throttle_0_1_1_1 = blocks.throttle(gr.sizeof_int*1, samp_rate)
        self.blocks_throttle_0_1_1_0_0 = blocks.throttle(gr.sizeof_int*1, samp_rate)
        self.blocks_throttle_0_1_1_0 = blocks.throttle(gr.sizeof_int*1, samp_rate)
        self.blocks_throttle_0_1_1 = blocks.throttle(gr.sizeof_int*1, samp_rate)
        self.blocks_throttle_0_1_0_0 = blocks.throttle(gr.sizeof_float*1, samp_rate)
        self.blocks_throttle_0_1_0 = blocks.throttle(gr.sizeof_float*1, samp_rate)
        self.blocks_null_source_1_0_0_1 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0_0_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_null_source_1_0_0 = blocks.null_source(gr.sizeof_gr_complex*1)
        self.blocks_multiply_xx_2_0 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_2 = blocks.multiply_vcc(1)
        self.blocks_multiply_xx_1_0 = blocks.multiply_vii(1)
        self.blocks_multiply_xx_1 = blocks.multiply_vii(1)
        self.blocks_multiply_const_vxx_0_1 = blocks.multiply_const_vcc((0.9, ))
        self.blocks_multiply_const_vxx_0_0 = blocks.multiply_const_vii((-1, ))
        self.blocks_multiply_const_vxx_0 = blocks.multiply_const_vii((-1, ))
        self.blocks_delay_0_0 = blocks.delay(gr.sizeof_int*1, ais_burst_duration)
        self.blocks_delay_0 = blocks.delay(gr.sizeof_int*1, ais_burst_duration)
        self.blocks_add_xx_0 = blocks.add_vcc(1)
        self.blocks_add_const_vxx_0_0 = blocks.add_const_vii((1, ))
        self.blocks_add_const_vxx_0 = blocks.add_const_vii((1, ))
        self.blks2_selector_0_1_0_0_1 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0 if(func_burst_out>0) else 0,
        	output_index=0,
        )
        self.blks2_selector_0_1_0_0_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0 if(func_doppler_0>0) else 1,
        	output_index=0,
        )
        self.blks2_selector_0_1_0_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=1 if(func_doppler>0) else 0,
        	output_index=0,
        )
        self.blks2_selector_0_1_0_0 = grc_blks2.selector(
        	item_size=gr.sizeof_gr_complex*1,
        	num_inputs=2,
        	num_outputs=1,
        	input_index=0 if(func_burst_out>0) else 0,
        	output_index=0,
        )
        self.analog_sig_source_x_1_2_1 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, doppler_control_freq1*2, 1, 0)
        self.analog_sig_source_x_1_2_0_0 = analog.sig_source_c(samp_rate, analog.GR_COS_WAVE, 125000, 1, 0)
        self.analog_sig_source_x_1_2 = analog.sig_source_f(samp_rate, analog.GR_COS_WAVE, doppler_control_freq1, 1, 0)
        self.analog_sig_source_x_1_1_0_0 = analog.sig_source_i(samp_rate, analog.GR_SQR_WAVE, send_interval_freq_0, 1, 0)
        self.analog_sig_source_x_1_1_0 = analog.sig_source_i(samp_rate, analog.GR_SQR_WAVE, send_interval_freq, 1, 0)
        self.AISTX_Build_Frame_0_0 = AISTX.Build_Frame("000101000001101100011001110111011011110000000000000000000000011000111100111100100000101100100000101101000110011010001010010100010000000001000000000000000000000000000000", True, True)
        self.AISTX_Build_Frame_0 = AISTX.Build_Frame("000100000001101100011001110111011011110000000000000000000000011000111100111100100000101100100000101101000110011010001010010100010000000001000000000000000000000000000000", True, True)

        ##################################################
        # Connections
        ##################################################
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.uhd_usrp_sink_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_1, 0), (self.wxgui_waterfallsink2_0_0, 0))
        self.connect((self.source_txtimer, 0), (self.blocks_throttle_0_1_1_0, 0))
        self.connect((self.blocks_throttle_0_1_1_0, 0), (self.probe_doppler, 0))
        self.connect((self.source_txtimer_0, 0), (self.blocks_throttle_0_1_1_0_0, 0))
        self.connect((self.blocks_throttle_0_1_1_0_0, 0), (self.probe_doppler_0, 0))
        self.connect((self.AISTX_Build_Frame_0, 0), (self.digital_gmsk_mod_0, 0))
        self.connect((self.blocks_multiply_xx_1, 0), (self.probe_burst, 0))
        self.connect((self.blocks_throttle_0_1_1, 0), (self.blocks_multiply_xx_1, 0))
        self.connect((self.blocks_delay_0, 0), (self.blocks_multiply_xx_1, 1))
        self.connect((self.blocks_add_const_vxx_0, 0), (self.blocks_delay_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0, 0), (self.blocks_add_const_vxx_0, 0))
        self.connect((self.blocks_throttle_0_1_1, 0), (self.blocks_multiply_const_vxx_0, 0))
        self.connect((self.analog_sig_source_x_1_1_0, 0), (self.blocks_throttle_0_1_1, 0))
        self.connect((self.blocks_multiply_xx_1_0, 0), (self.probe_burst_0, 0))
        self.connect((self.blocks_throttle_0_1_1_1, 0), (self.blocks_multiply_xx_1_0, 0))
        self.connect((self.blocks_delay_0_0, 0), (self.blocks_multiply_xx_1_0, 1))
        self.connect((self.blocks_add_const_vxx_0_0, 0), (self.blocks_delay_0_0, 0))
        self.connect((self.blocks_multiply_const_vxx_0_0, 0), (self.blocks_add_const_vxx_0_0, 0))
        self.connect((self.blocks_throttle_0_1_1_1, 0), (self.blocks_multiply_const_vxx_0_0, 0))
        self.connect((self.analog_sig_source_x_1_1_0_0, 0), (self.blocks_throttle_0_1_1_1, 0))
        self.connect((self.blocks_null_source_1_0_0, 0), (self.blks2_selector_0_1_0_0, 1))
        self.connect((self.digital_gmsk_mod_0, 0), (self.blks2_selector_0_1_0_0, 0))
        self.connect((self.blocks_null_source_1_0_0_0, 0), (self.blks2_selector_0_1_0_0_0, 1))
        self.connect((self.blocks_vco_c_0_0, 0), (self.blks2_selector_0_1_0_0_0, 0))
        self.connect((self.analog_sig_source_x_1_2, 0), (self.blocks_throttle_0_1_0, 0))
        self.connect((self.blocks_throttle_0_1_0, 0), (self.blocks_vco_c_0_0, 0))
        self.connect((self.blks2_selector_0_1_0_0_0, 0), (self.blocks_multiply_xx_2, 2))
        self.connect((self.blks2_selector_0_1_0_0, 0), (self.blocks_multiply_xx_2, 1))
        self.connect((self.analog_sig_source_x_1_2_0_0, 0), (self.blocks_multiply_xx_2, 0))
        self.connect((self.AISTX_Build_Frame_0_0, 0), (self.digital_gmsk_mod_0_0, 0))
        self.connect((self.digital_gmsk_mod_0_0, 0), (self.blks2_selector_0_1_0_0_1, 0))
        self.connect((self.blocks_null_source_1_0_0_0_0, 0), (self.blks2_selector_0_1_0_0_0_0, 1))
        self.connect((self.blocks_vco_c_0_0_0, 0), (self.blks2_selector_0_1_0_0_0_0, 0))
        self.connect((self.analog_sig_source_x_1_2_1, 0), (self.blocks_throttle_0_1_0_0, 0))
        self.connect((self.blocks_throttle_0_1_0_0, 0), (self.blocks_vco_c_0_0_0, 0))
        self.connect((self.blocks_null_source_1_0_0_1, 0), (self.blks2_selector_0_1_0_0_1, 1))
        self.connect((self.blks2_selector_0_1_0_0_1, 0), (self.blocks_multiply_xx_2_0, 1))
        self.connect((self.blks2_selector_0_1_0_0_0_0, 0), (self.blocks_multiply_xx_2_0, 2))
        self.connect((self.analog_sig_source_x_1_2_0_0, 0), (self.blocks_multiply_xx_2_0, 0))
        self.connect((self.blocks_multiply_xx_2, 0), (self.blocks_add_xx_0, 0))
        self.connect((self.blocks_multiply_xx_2_0, 0), (self.blocks_add_xx_0, 1))
        self.connect((self.blocks_add_xx_0, 0), (self.blocks_multiply_const_vxx_0_1, 0))


# QT sink close method reimplementation

    def get_samp_rate(self):
        return self.samp_rate

    def set_samp_rate(self, samp_rate):
        self.samp_rate = samp_rate
        self.set_ais_burst_duration(self.samp_rate/5)
        self.wxgui_waterfallsink2_0_0.set_sample_rate(self.samp_rate)
        self.uhd_usrp_sink_0.set_samp_rate(self.samp_rate)
        self.blocks_throttle_0_1_1_0.set_sample_rate(self.samp_rate)
        self.source_txtimer.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0_1_1_0_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1_1_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0_1_1.set_sample_rate(self.samp_rate)
        self.blocks_throttle_0_1_1_1.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1_1_0_0.set_sampling_freq(self.samp_rate)
        self.source_txtimer_0.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0_1_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1_2.set_sampling_freq(self.samp_rate)
        self.analog_sig_source_x_1_2_1.set_sampling_freq(self.samp_rate)
        self.blocks_throttle_0_1_0_0.set_sample_rate(self.samp_rate)
        self.analog_sig_source_x_1_2_0_0.set_sampling_freq(self.samp_rate)

    def get_send_interval_freq_0(self):
        return self.send_interval_freq_0

    def set_send_interval_freq_0(self, send_interval_freq_0):
        self.send_interval_freq_0 = send_interval_freq_0
        self.analog_sig_source_x_1_1_0_0.set_frequency(self.send_interval_freq_0)

    def get_send_interval_freq(self):
        return self.send_interval_freq

    def set_send_interval_freq(self, send_interval_freq):
        self.send_interval_freq = send_interval_freq
        self.analog_sig_source_x_1_1_0.set_frequency(self.send_interval_freq)

    def get_func_doppler_0(self):
        return self.func_doppler_0

    def set_func_doppler_0(self, func_doppler_0):
        self.func_doppler_0 = func_doppler_0
        self.blks2_selector_0_1_0_0_0_0.set_input_index(int(0 if(self.func_doppler_0>0) else 1))

    def get_func_doppler(self):
        return self.func_doppler

    def set_func_doppler(self, func_doppler):
        self.func_doppler = func_doppler
        self.blks2_selector_0_1_0_0_0.set_input_index(int(1 if(self.func_doppler>0) else 0))

    def get_func_burst_out_0(self):
        return self.func_burst_out_0

    def set_func_burst_out_0(self, func_burst_out_0):
        self.func_burst_out_0 = func_burst_out_0

    def get_func_burst_out(self):
        return self.func_burst_out

    def set_func_burst_out(self, func_burst_out):
        self.func_burst_out = func_burst_out
        self.uhd_usrp_sink_0.set_gain(20 if(self.func_burst_out>0) else 0, 0)
        self.blks2_selector_0_1_0_0.set_input_index(int(0 if(self.func_burst_out>0) else 0))
        self.blks2_selector_0_1_0_0_1.set_input_index(int(0 if(self.func_burst_out>0) else 0))

    def get_doppler_sensitivity(self):
        return self.doppler_sensitivity

    def set_doppler_sensitivity(self, doppler_sensitivity):
        self.doppler_sensitivity = doppler_sensitivity

    def get_doppler_control_freq1(self):
        return self.doppler_control_freq1

    def set_doppler_control_freq1(self, doppler_control_freq1):
        self.doppler_control_freq1 = doppler_control_freq1
        self.source_txtimer.set_frequency(self.doppler_control_freq1/4)
        self.source_txtimer_0.set_frequency(self.doppler_control_freq1)
        self.analog_sig_source_x_1_2.set_frequency(self.doppler_control_freq1)
        self.analog_sig_source_x_1_2_1.set_frequency(self.doppler_control_freq1*2)

    def get_channel_select(self):
        return self.channel_select

    def set_channel_select(self, channel_select):
        self.channel_select = channel_select

    def get_bit_rate(self):
        return self.bit_rate

    def set_bit_rate(self, bit_rate):
        self.bit_rate = bit_rate

    def get_ais_burst_duration(self):
        return self.ais_burst_duration

    def set_ais_burst_duration(self, ais_burst_duration):
        self.ais_burst_duration = ais_burst_duration
        self.blocks_delay_0.set_dly(self.ais_burst_duration)
        self.blocks_delay_0_0.set_dly(self.ais_burst_duration)

if __name__ == '__main__':
    import ctypes
    import os
    if os.name == 'posix':
        try:
            x11 = ctypes.cdll.LoadLibrary('libX11.so')
            x11.XInitThreads()
        except:
            print "Warning: failed to XInitThreads()"
    parser = OptionParser(option_class=eng_option, usage="%prog: [options]")
    (options, args) = parser.parse_args()
    tb = Space_AIS_RX()
    tb.Start(True)
    tb.Wait()


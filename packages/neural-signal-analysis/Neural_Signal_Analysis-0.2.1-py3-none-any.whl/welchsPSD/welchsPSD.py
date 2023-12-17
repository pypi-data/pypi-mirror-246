"""
Welch's Power Spectral Density Analysis Module for EEG Data

This module provides functions to compute and visualize the Power Spectral Density (PSD) of EEG data using Welch's method. It is capable of processing both single-channel and multi-channel EEG data, making it suitable for various EEG analysis tasks.

Functions:
- calculate_psd(data, fs, nperseg): Calculates the Power Spectral Density of the provided data.
- plot_psd(frequencies, psd, channel_name): Plots the Power Spectral Density for a given channel.
- process_eeg_data(eeg_data, fs, nperseg): Processes EEG data to calculate and plot PSD for each channel.

Example Usage:
---------------
import numpy as np
from welchsPSD import process_eeg_data

# Sample EEG data (3 channels x 1000 data points)
eeg_data = np.random.rand(3, 1000)
fs = 250  # Sampling frequency in Hz

# Process EEG data and plot Power Spectral Density
process_eeg_data(eeg_data, fs)

Note:
-----
PSD is a key measure in EEG analysis for understanding the frequency content of EEG signals. Welch's method is a widely used approach for estimating PSD.
"""

import numpy as np
from scipy import signal
import matplotlib.pyplot as plt

def calculate_psd(data, fs, nperseg=1024):
    """
    Calculate Power Spectral Density using Welch's method.

    Parameters:
    data : array_like
        One-dimensional time series data.
    fs : float
        Sampling frequency of the data.
    nperseg : int, optional
        Length of each segment for Welch's method.

    Returns:
    frequencies : ndarray
        Array of sample frequencies.
    psd : ndarray
        Power spectral density of data.
    """
    frequencies, psd = signal.welch(data, fs, nperseg=nperseg)
    return frequencies, psd

def plot_psd(frequencies, psd, channel_name=None):
    """
    Plot the Power Spectral Density.

    Parameters:
    frequencies : ndarray
        Array of sample frequencies.
    psd : ndarray
        Power spectral density of data.
    channel_name : str, optional
        Name of the EEG channel (for title).
    """
    plt.figure()
    plt.semilogy(frequencies, psd)
    if channel_name:
        plt.title(f'PSD for Channel {channel_name}')
    plt.xlabel('Frequency [Hz]')
    plt.ylabel('PSD [V**2/Hz]')
    plt.grid(True)
    plt.show()

def process_eeg_data(eeg_data, fs, nperseg=1024):
    """
    Process EEG data to calculate and plot PSD for each channel.

    Parameters:
    eeg_data : ndarray
        EEG data array (channels x time series data).
    fs : float
        Sampling frequency of the EEG data.
    nperseg : int, optional
        Length of each segment for Welch's method.
    """
    for i in range(eeg_data.shape[0]):
        channel_data = eeg_data[i, :]
        frequencies, psd = calculate_psd(channel_data, fs, nperseg)
        plot_psd(frequencies, psd, channel_name=f'Channel {i+1}')


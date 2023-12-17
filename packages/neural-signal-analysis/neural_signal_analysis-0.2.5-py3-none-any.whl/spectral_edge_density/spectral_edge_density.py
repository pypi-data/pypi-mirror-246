"""
Spectral Edge Density Analysis Module

This module provides functions to compute and plot the spectral edge density of EEG data. It is capable of processing both single-channel and multi-channel EEG data.

Functions:
- compute_spectral_edge_density(data, fs, percentage): Computes the spectral edge density of the provided data.
- plot_spectral_edge_frequencies(edge_frequencies, channel_names): Plots the spectral edge frequencies for each channel.
- process_eeg_data(eeg_data, fs, percentage): Processes EEG data to calculate and plot spectral edge frequencies for each channel.

Example Usage:
---------------
import numpy as np
from spectral_edge_density import process_eeg_data

# Sample EEG data (3 channels x 1000 data points)
eeg_data = np.random.rand(3, 1000)
fs = 250  # Sampling frequency in Hz
percentage = 90  # Percentage threshold for spectral edge

# Process EEG data and plot spectral edge frequencies
process_eeg_data(eeg_data, fs, percentage)

Note:
-----
The spectral edge frequency is a measure used in EEG analysis to determine the frequency below which a certain percentage of the total power of the spectrum is contained.
"""

import numpy as np
import scipy.fft
import matplotlib.pyplot as plt

def compute_spectral_edge_density(data, fs, percentage):
    """
    Compute the spectral edge density of the provided time series data.

    Parameters:
    data : array_like
        One-dimensional time series data.
    fs : float
        Sampling frequency of the data.
    percentage : float
        Percentage threshold to define the spectral edge density.

    Returns:
    spectral_edge : float
        Spectral edge density based on the percentage of the total power.
    """
    fft_result = scipy.fft.fft(data)
    frequencies = scipy.fft.fftfreq(len(data), 1.0/fs)
    positive_frequencies = frequencies[frequencies >= 0]
    positive_fft_result = fft_result[frequencies >= 0]
    magnitude = np.abs(positive_fft_result)
    sorted_magnitude = np.sort(magnitude)[::-1]
    cumulative_sum = np.cumsum(sorted_magnitude)
    total_power = np.sum(magnitude)
    threshold = total_power * percentage / 100
    spectral_edge = positive_frequencies[np.argmax(cumulative_sum >= threshold)]
    return spectral_edge

def plot_spectral_edge_frequencies(edge_frequencies, channel_names):
    """
    Plot the spectral edge frequencies for each channel.

    Parameters:
    edge_frequencies : list or ndarray
        Spectral edge frequencies for each channel.
    channel_names : list
        Names of the channels.
    """
    plt.figure(figsize=(10, 5))
    plt.bar(channel_names, edge_frequencies)
    plt.title(f'Spectral Edge Frequency for Each Channel')
    plt.xlabel('Channel')
    plt.ylabel('Spectral Edge Frequency [Hz]')
    plt.xticks(rotation=90)
    plt.grid(True)
    plt.show()

def process_eeg_data(eeg_data, fs, percentage):
    """
    Process EEG data to calculate and plot spectral edge frequencies for each channel.

    Parameters:
    eeg_data : ndarray
        EEG data array (channels x time series data).
    fs : float
        Sampling frequency of the EEG data.
    percentage : float
        Percentage threshold to define the spectral edge frequency.
    """
    edge_frequencies = [compute_spectral_edge_density(channel_data, fs, percentage) for channel_data in eeg_data]
    channel_names = [f'Channel {i+1}' for i in range(eeg_data.shape[0])]
    plot_spectral_edge_frequencies(edge_frequencies, channel_names)


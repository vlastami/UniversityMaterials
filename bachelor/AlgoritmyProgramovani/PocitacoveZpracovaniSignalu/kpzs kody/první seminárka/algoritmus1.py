# algoritmus1.py
import numpy as np
from matplotlib import pyplot as plt
from scipy import signal as sps


def decg_peaks(ecg, time):
    d_ecg = np.diff(ecg)  # najít derivaci ekg signálu
    peaks_d_ecg, _ = sps.find_peaks(d_ecg)  # vrcholy

    # graf
    plt.figure()
    plt.plot(time[0:len(time) - 1], d_ecg, color='red')
    plt.plot(time[peaks_d_ecg], d_ecg[peaks_d_ecg], "x", color='g')
    plt.xlabel('Čas [s]')
    plt.ylabel('Derivace')
    plt.title('Vrcholy derivace EKG')
    plt.show()
    return d_ecg, peaks_d_ecg


def d_ecg_peaks(d_ecg, peaks_d_ecg, time, heightper, distanceper):
    meanpeaks_d_ecg = np.mean(d_ecg[peaks_d_ecg])  # najít průměr vrcholů
    max_d_ecg = np.max(d_ecg)  # najít max ekg signál
    threshold = np.mean([meanpeaks_d_ecg, max_d_ecg]) * heightper
    newpeaks_d_ecg, _ = sps.find_peaks(d_ecg, height=threshold)
    meandistance = np.mean(np.diff(newpeaks_d_ecg))
    Rwave_peaks_d_ecg, _ = sps.find_peaks(d_ecg, height=threshold, distance=meandistance * distanceper)

    # graf
    plt.figure()
    plt.plot(time[0:len(time) - 1], d_ecg, color='red')
    plt.plot(time[Rwave_peaks_d_ecg], d_ecg[Rwave_peaks_d_ecg], "x", color='g')
    thres = plt.axhline(threshold, color='black', label='threshold')
    plt.title('Vrcholy d_ECG')
    plt.ylabel('Derivace')
    plt.xlabel('Čas [s]')
    plt.legend()
    return Rwave_peaks_d_ecg # vrací R


def Rwave_peaks(ecg, d_ecg, Rwave_peaks_d_ecg, time):
    Rwave = np.empty([len(Rwave_peaks_d_ecg) - 1])
    for i in range(0, len(Rwave)):
        ecgrange = ecg[Rwave_peaks_d_ecg[i]:Rwave_peaks_d_ecg[i + 1]]  # pole obsahující EKG v rámci d_ecg_peaks
        percentage = np.round(len(ecgrange) * 0.2)
        maxvalue = np.array(
            list(np.where(ecgrange == np.max(ecgrange.iloc[0:int(percentage)]))))  # index s nejvyšší hodnotou ekg
        Rwave[i] = Rwave_peaks_d_ecg[i] + maxvalue[0, 0]

    Rwave = Rwave.astype(np.int64)
    Rwave_t = time[Rwave]

    # graf
    fig, ax1 = plt.subplots()
    ax1.plot(time[0:len(time) - 1], d_ecg, color='r', label='Derivace EKG')
    ax1.set_ylabel('Derivace')
    plt.xlabel('Time [s]')
    plt.title('Vrcholy R-vln')
    ax2 = ax1.twinx()
    ax2.plot(time, ecg, color='b', label='ECG')
    ax2.plot(time[Rwave], ecg[Rwave], "x", color='g')
    ax2.set_ylabel('Aktivace')
    ax1.legend()
    ax2.legend()
    return Rwave_t

import numpy as np
from scipy.interpolate import interp1d

def lorentzain(fi, fj, a, gamma):
    wave = (1 / np.pi) * (gamma / ((fi - fj) ** 2 + (gamma) ** 2))
    return a * wave

def T1_spectra(fMax, step):
    badFreqNum = np.random.randint(5)
    fList = np.linspace(3.75, fMax, step)
    gamma = 1e-3 + (2e-2 - 1e-3) * np.random.random()
    T1 = np.random.normal(np.random.randint(20, 50), 5, step)
    for _ in range(badFreqNum):
        a = np.random.random() * 0.6
        badFreq = 3.75 + (fMax - 3.75) * np.random.random()
        T1 -= lorentzain(fList, badFreq, a, gamma)
    for T in range(len(T1)):
        T1[T] = np.max([1, T1[T]])
    return 1e-3 / T1


def f_phi_spectra(fMax, phi):
    d = 0
    return fMax * np.sqrt(
        np.abs(np.cos(np.pi * phi)) * np.sqrt(1 + d**2 * np.tan(np.pi * phi) ** 2)
    )


def phi2f(phi, fMax, step):
    phiList = np.linspace(0, 0.5, step)
    fList = f_phi_spectra(fMax, phiList)
    func_interp = interp1d(phiList, fList, kind='cubic')
    if isinstance(phi, (int, float)):
        return float(func_interp(phi))
    else:
        return func_interp(phi)


def f2phi(f, fq_max, Ec, d):
    alpha = (f + Ec) / (Ec + fq_max)
    beta = (alpha**4 - d**2) / (1 - d**2)
    # print(beta)
    beta = np.sqrt(beta)
    # add a clip function
    phi = np.arccos(beta)
    return phi

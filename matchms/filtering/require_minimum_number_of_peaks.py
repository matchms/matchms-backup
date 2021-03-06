from math import ceil
from ..typing import SpectrumType


def require_minimum_number_of_peaks(spectrum_in: SpectrumType, n_required=10, ratio_required=None) -> SpectrumType:
    """Spectrum will be set to None when it has fewer peaks than required.

    Args:
    ----
    spectrum_in: matchms.Spectrum()
        Input spectrum.
    n_required: int
        Number of minimum required peaks. Spectra with fewer peaks will be set
        to 'None'.
    ratio_required: float, optional
        Set desired ratio between minimum number of peaks and parent mass.
        Default is None.
    """
    if spectrum_in is None:
        return None

    spectrum = spectrum_in.clone()

    parent_mass = spectrum.get("parent_mass", None)
    if parent_mass and ratio_required:
        n_required_by_mass = int(ceil(ratio_required * parent_mass))
        threshold = max(n_required, n_required_by_mass)
    else:
        threshold = n_required

    if spectrum.peaks.intensities.size < threshold:
        return None

    return spectrum

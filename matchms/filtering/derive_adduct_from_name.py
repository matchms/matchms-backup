from ..typing import SpectrumType
from ..utils import looks_like_adduct


def derive_adduct_from_name(spectrum_in: SpectrumType, remove_adduct_from_name=True) -> SpectrumType:
    """Find adduct in compound name and add to metadata (if not present yet).

    Method to interpret the given compound name to find the adduct.
    Args:
    ----
    spectrum_in: SpectrumType
        Input spectrum.
    remove_adduct_from_name: bool
        Remove found adducts from compound name if set to True. Default is True.
    """
    if spectrum_in is None:
        return None

    spectrum = spectrum_in.clone()

    # Get compound name
    if spectrum.get("compound_name", None):
        name = spectrum.get("compound_name")
    else:
        assert spectrum.get("name", None) is not None, ("Found 'name' but not 'compound_name' in metadata",
                                                        "Apply 'add_compound_name' filter first.")
        print("No compound name found in metadata.")
        return spectrum

    # Detect adduct in compound name
    adduct_from_name = None
    name_split = name.split(" ")
    for name_part in name_split[::-1][:2]:
        if looks_like_adduct(name_part):
            adduct_from_name = name_part
            break

    # Remove found adduct from compound name (if remove_adduct_from_name=True)
    if adduct_from_name and remove_adduct_from_name:
        name_adduct_removed = " ".join([x for x in name_split if x != adduct_from_name])
        spectrum.set("compound_name", name_adduct_removed)
        print("Removed adduct {} from compound name.".format(adduct_from_name))

    # Add found adduct to metadata (if not present yet)
    if adduct_from_name and not looks_like_adduct(spectrum.get("adduct")):
        spectrum.set("adduct", adduct_from_name.strip().replace("*", ""))
        print("Added adduct {} to metadata.".format(adduct_from_name))

    return spectrum

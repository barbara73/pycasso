"""
Test black out
"""
from src.pycassodicom.black_out import delete_dicom, blacken_pixels


def test_blacken_pixels_returns_same_ds(transfer_syntax_ds):
    """Same data set returned, if no burned-in annotation suspected."""
    assert blacken_pixels(transfer_syntax_ds) == transfer_syntax_ds


def test_blacken_pixels_returns_changed_photometric_interpretation(us_dataset):
    """Data set changed, when manufacturer is PHILIPS and modality is US."""
    ds = blacken_pixels(us_dataset)
    assert ds.PhotometricInterpretation == 'MONOCHROME2'


def test_return_unchanged_ds_if_attribute_is_missing(ge_dataset):
    """Return unchanged data set if an attribute (dicom tag) is missing."""
    black_ds = blacken_pixels(ge_dataset)
    assert black_ds.PhotometricInterpretation == 'RGB'


def test_delete_dicom_returns_true_when_nb_frames_is_none(us_dataset):
    """If one condition is different, then image will not be deleted."""
    us_dataset.NumberOfFrames = None
    assert delete_dicom(us_dataset) is True


def test_delete_dicom_returns_false(us_dataset):
    """Return false, if you want to keep image that is correct (PRIMARY)."""
    assert delete_dicom(us_dataset) is False


def test_delete_dicom_returns_true(ct_dataset):
    """Return true to delete image that contains INVALID."""
    assert delete_dicom(ct_dataset) is True

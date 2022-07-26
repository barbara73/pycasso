"""
Test black out
"""
from src.pycassodicom.black_out import delete_dicom, blacken_pixels


def test_blacken_pixels_returns_same_ds(transfer_syntax_ds):
    assert blacken_pixels(transfer_syntax_ds) == transfer_syntax_ds


def test_blacken_pixels_returns_blackened_image_ds_for_agfa(agfa_dataset):
    black_ds = blacken_pixels(agfa_dataset)
    assert black_ds.PhotometricInterpretation == 'YBR_FULL'


def test_delete_dicom_returns_none(a_dataset):
    a_dataset.Manufacturer = 'SIEMENS'
    assert delete_dicom(a_dataset) is None


def test_delete_dicom_returns_not_none(a_dataset):
    a_dataset.Manufacturer = 'Agfa'
    assert delete_dicom(a_dataset) is a_dataset

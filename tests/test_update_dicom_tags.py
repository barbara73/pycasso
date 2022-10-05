from src.pycassodicom.update_dicom_tags import update_ds


def test_update_ds(transfer_syntax_ds):
    """Test if update dataset gives correct output."""
    ds = update_ds(transfer_syntax_ds)
    assert ds.file_meta.TransferSyntaxUID == '1.2.840.10008.1.2.1'
    assert ds.BurnedInAnnotation == 'NO'
    assert ds.PatientIdentityRemoved == 'YES'
    assert len(ds.DeidentificationMethodCodeSequence) == 8

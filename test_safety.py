import storage

def test_data_file_is_redirected_to_temporary_directory(tmp_path):
    assert storage.DATA_FILE.parent == tmp_path
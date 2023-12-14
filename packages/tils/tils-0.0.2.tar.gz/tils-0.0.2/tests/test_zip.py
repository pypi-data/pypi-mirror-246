from tils.zip import download_zip
from os import path
from tempfile import TemporaryDirectory

def test_download_zip():

    # create a temporary directory for testing space
    with TemporaryDirectory() as tmpdirname:
        unzipped_dir = str(tmpdirname)

        # download and unzip the zip file
        archive_url = "https://github.com/fortunate-one/utils/archive/master.zip"
        download_zip(archive_url, unzipped_dir)

        # assert that the zip file was downloaded and unzipped
        assert path.isdir(unzipped_dir)
        read_me_path = path.join(unzipped_dir, "utils-main", "README.md")
        assert path.isfile(read_me_path)
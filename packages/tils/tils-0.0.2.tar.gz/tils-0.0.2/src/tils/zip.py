from os import path
from os import makedirs, remove
from zipfile import ZipFile
from urllib.request import urlretrieve
from tempfile import mkdtemp

from tils.uri import uri_validator

def download_zip(url: str, parent_dir: str) -> None:
    """
    Download and unzip file to a directory. Will also automatically delete the temporary zipped file.

    Args:
        url (str): The URL to download the zip file from.
        parent_dir (str): The parent directory to unzip the file to.

    Returns:
        None
    """

    # Check if url is a string and a valid URL
    if not isinstance(url, str):
        raise ValueError("url must be a string")
    if not uri_validator(url):
        raise ValueError("url must be a valid URL")

    # Check if parent_dir is a string and a valid directory
    if not isinstance(parent_dir, str):
        raise ValueError("parent_dir must be a string")
    if not path.isdir(parent_dir):
        makedirs(parent_dir)

    # Create a temporary directory
    temp_dir = mkdtemp()

    # get the file name from the url and create the path to the temp zip file
    file_name = url.split('/')[-1]
    zip_file_path = path.join(temp_dir, file_name)

    # Download the zip file
    urlretrieve(url, zip_file_path)

    # Unzip the file
    with ZipFile(zip_file_path, 'r') as zip_ref:
        zip_ref.extractall(parent_dir)

    # Delete the temporary directory
    remove(zip_file_path)
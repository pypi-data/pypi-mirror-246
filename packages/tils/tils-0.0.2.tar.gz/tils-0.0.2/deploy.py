from dotenv import load_dotenv
from os import getenv, system

load_dotenv()

user = getenv("PYPI-USER")
password = getenv("PYPI-TOKEN")

#TODO validate dist folder is empty and that the package is not building a version that is already on pypi

# build package
system("python -m build")

# upload package
system(f"twine upload --username {user} --password {password} dist/*")

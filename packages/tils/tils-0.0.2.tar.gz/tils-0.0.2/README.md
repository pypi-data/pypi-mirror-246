# Tils

Collection of Python utility functions

## Deployment to PyPi

Create a `.env` file with the following content (add pypi token within quotes).

```bash
PYPI-USER = "__token__"
PYPI-TOKEN = ""
```

Create a virtual environment and install the dependencies.

Linux

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Run deployment script.

```bash
python deploy.py
```

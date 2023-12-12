# DIH: Docker Image Handler
Help to save and load docker image.

![cover](./assets/load-docker-image.png)

# Requirements
* `python 3.10`
* [virtualenv](./assets/install-venv.md)
* `mkvirtualenv dih`
* `pip install -r requirements.txt`

# Usage
* Load Docker Tarball Files:
    ```bash
    python3 src/main.py load -f ./archives/ -c ./sample-compose.yml 
    ```
* Save Docker Image into specific folder
    ```bash
    python3 src/main.py save -f ./archives/ -inc innodisk -exc none
    ```

# Testing
* `pytest -v`
* `pytest --doctest-modules --junitxml=junit/test-results.xml --cov=. --cov-report=xml --cov-report=html`

# Distribute
```bash
python setup.py sdist bdist_wheel
pip3 install dist/dih-*.whl
```
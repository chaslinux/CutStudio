# Running CutStudio

Open a terminal and navigate to the project directory:

cd ~/Code/CutStudio

Activate the Python virtual environment:

source .venv/bin/activate

Launch CutStudio:

python -m cutstudio.main

## Running Automated Tests

To run the complete test suite:

python -m pytest -q

To run tests with more detailed output:

python -m pytest -v

## Development Environment

CutStudio uses Python, PySide6, and pytest.

Always activate the project's virtual environment before launching the application or running tests.

See HANDOFF.md for development environment setup and additional project development instructions.

# What is CutStudio

I recently discovered that Brother discontinued the web version
of CanvasWorkspace (ScanNCut), leaving Windows and macOS as the
remaining supported desktop platforms.

This left my partner, who uses Linux, without the software she
was accustomed to using with her Brother ScanNCut SDX125.

We specifically purchased the cutter because, at the time,
Brother appeared to be taking a more consumer-friendly approach
than some other companies in the cutting machine market.

Unfortunately, we're increasingly seeing some of the same
problems elsewhere in the industry: subscription pressure,
features disappearing, and user interfaces being redesigned
in ways that remove functionality rather than improve it.

CutStudio is my attempt to provide another option.

## What CutStudio is NOT

This is not a clone of Brother's software. It's my intention to make a functional program to do some of the job of Brother's CanvasWorkspace, but it's not intended to be a clone. The purpose of this software is to give Linux (and perhaps other *nix users) software they can use to eventually use their cutter as expected again.

## Current Development Status

CutStudio is an early-stage vector design application. Development
is ongoing, and the application is not yet ready to replace
commercial cutting software.

Current functionality includes:

- Rectangle, ellipse, and text creation.
- Object selection and multi-selection.
- Object movement, resizing, and rotation.
- Shift-constrained aspect-ratio resizing.
- Rotation snapping.
- Object duplication and deletion.
- Undo and Redo.
- Multiple layers.
- Layer visibility and locking.
- Editable object position, dimensions, and rotation.
- Native CutStudio project saving and loading.
- Physical measurement support using millimetres.

The automated test suite currently contains 43 passing tests.

Some graphical interactions still require additional manual
verification.

## Screenshot (current state - very early development)

<img width="1423" height="953" alt="CutStudio" src="https://github.com/user-attachments/assets/f84c3c2e-4ea9-437b-8444-d9c152ab4bfe" />

## Future Development

Planned functionality includes:

- SVG importing and exporting.
- PDF and PNG exporting.
- Advanced vector path editing.
- Improved text editing.
- Object grouping and alignment.
- Cutting job preparation.
- Cutting machine profiles and communication.

Cutting machine communication has not yet been implemented.

## Cloning the repository

I keep my projects in subdirectories of `~/Code`

```bash
mkdir -p ~/Code
cd ~/Code
git clone https://github.com/chaslinux/CutStudio
cd ~/Code/CutStudio
```

## Install the development environment

The repository includes a development environment setup script
that installs required system packages, creates a Python virtual
environment, installs Python dependencies, runs the automated
tests, and launches CutStudio.

The development environment is currently tested on Linux Mint
22.3, based on Ubuntu 24.04.

```bash
cd ~/Code/CutStudio
./install-dev-environment.sh
```

## Running CutStudio

Open a terminal and navigate to the project directory:

```bash
cd ~/Code/CutStudio
source .venv/bin/activate
python -m cutstudio.main
```

## Running Automated Tests

To run the complete test suite:

```bash
python -m pytest -q
```

To run tests with more detailed output:

```bash
python -m pytest -v
```
## Development Environment

CutStudio uses Python, PySide6, and pytest.

Always activate the project's virtual environment before launching the application or running tests.

See HANDOFF.md for development environment setup and additional project development instructions.

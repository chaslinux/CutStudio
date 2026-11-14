# What is CutStudio

I recently discovered that Brother discontinued the web version of CanvasWorkSpace (ScanNCut), leaving only Windows and MacOS versions of the software. This left my partner, who uses Linux, without the software she was used to for her ScanNCut SDX125. We specifically bought the cutter because at the time Brother appeared to be doing less sketchy things than other companies in the cutter market. Fast forward a couple of years and we're starting to see the same sketchy behaviour as other companies: trying to force folks into subscriptions, removing features for bad UI redesigns, etc.

## What CutStudio is NOT

This is not a clone of Brother's software. It's my intention to make a functional program to do some of the job of Brother's CanvasWorkspace, but it's not intended to be a clone. The purpose of this software is to give Linux (and perhaps other *nix users) software they can use to eventually use their cutter as expected again.

## Screenshot (current state - very early development)

<img width="1423" height="953" alt="CutStudio" src="https://github.com/user-attachments/assets/f84c3c2e-4ea9-437b-8444-d9c152ab4bfe" />

## Cloning the repository

I put all my projects in a sudirectory of `~/Code`

```bash
mkdir -p ~/Code
cd ~/Code
git clone https://github.com/chaslinux/CutStudio
cd ~/Code/CutStudio
```

## Install the development environment

I've included a handy bash script for setting up the python development environment. This will eventually be removed/moved somewhere else, but before trying to run CutStudio you'll currently need to set up the development environment. I'm running Linux Mint 22.3 (which uses Ubuntu 24.04.x as a base, so it will likely work on any Ubuntu 24.04.* environment.

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

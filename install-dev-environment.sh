
# Install system dependencies
sudo apt update
sudo apt install -y python3 python3-pip python3-venv python3-dev build-essential \
    libgl1 libegl1 libxkbcommon-x11-0 libxcb-cursor0 \
    libxcb-icccm4 libxcb-image0 libxcb-keysyms1 libxcb-randr0 \
    libxcb-render-util0 libxcb-shape0 libxcb-xfixes0

# Enter project directory
cd ~/Code/CutStudio

# Create virtual environment
python3 -m venv .venv

# Activate environment
source .venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install project dependencies
pip install -r requirements.txt

# Run tests
python -m pytest -v

# Launch CutStudio
python -m cutstudio.main


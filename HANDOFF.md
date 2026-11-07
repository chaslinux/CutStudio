# CutStudio Development Handoff

## 1. Project Overview

**Project:** CutStudio

**Description:** Cross-platform vector design and vinyl cutting application.

**Primary language:** Python

**GUI framework:** PySide6 (Qt 6)

**Current development platform:** Linux Mint

**Desktop environment:** Cinnamon

**Current display session:** X11

**Python version:** Python 3.12

**Development environment:** Python virtual environment (`.venv`)

**Application entry point:** `python -m cutstudio.main`

---

## 2. Current Project Status

CutStudio currently has an initial working graphical application.

The application successfully launches and displays its main window using PySide6.

The current implementation is primarily contained in:

`cutstudio/main.py`

The application is still in its early foundation stage.

The next major objective is to transition from the initial prototype into a modular application architecture.

---

## 3. Confirmed Working Functionality

The following functionality exists in the current implementation:

- Main application window.
- Application menu bar.
- Main toolbar.
- Left drawing tools panel.
- Right properties and layers panel.
- Graphics scene.
- Graphics view.
- 12 × 12 inch cutting mat.
- One-inch grid.
- Mat boundary.
- Rectangle creation.
- Ellipse creation.
- Text creation.
- Object selection.
- Object movement.
- Rubber-band selection.
- Ctrl + mouse wheel zoom.
- Initial status bar.

The application currently uses QGraphicsView and QGraphicsScene.

Drawing objects are implemented using Qt graphics items.

---

## 4. Development Environment

The current development environment uses:

- Linux Mint.
- Cinnamon desktop environment.
- X11 display server.
- Python 3.12.
- PySide6.
- Virtual environment located at `.venv`.

Activate the environment:

```bash
cd ~/Code/CutStudio
source .venv/bin/activate```

Launch the applicaption

```python -m cutstudio.main```

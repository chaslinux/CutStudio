
---

## 3. ARCHITECTURE.md

Save as `docs/ARCHITECTURE.md`.

```markdown
# CutStudio Software Architecture

## 1. Overview

CutStudio is a Python-based desktop vector design application built using PySide6 and Qt 6.

The application is intended to support vector design, vinyl cutting, plotter workflows, and other fabrication applications.

The architecture should support:

- Cross-platform operation.
- Modular development.
- Testable components.
- Accurate physical measurements.
- Extensible drawing tools.
- Multiple export formats.
- Future hardware integration.

This document describes the intended architecture.

Some components are proposed and have not yet been implemented.

---

## 2. Architectural Principles

### Separation of Responsibilities

The graphical interface should not own all application logic.

Separate:

- User interface.
- Document data.
- Canvas rendering.
- Drawing tools.
- File operations.
- Machine communication.

### Document Independence

The document model should be independent of the graphical interface.

A design should be capable of being:

- Created.
- Modified.
- Saved.
- Loaded.
- Exported.
- Processed for cutting.

Without requiring the graphical interface to be active.

### Cross-Platform Compatibility

Avoid operating-system-specific assumptions.

Use Qt abstractions where possible.

Do not hardcode developer-specific paths or platform plugin locations.

### Testability

Important application logic should be testable independently of the GUI.

---

## 3. Proposed Directory Structure

```text
CutStudio/
│
├── cutstudio/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── app/
│   │   ├── __init__.py
│   │   └── application.py
│   │
│   ├── canvas/
│   │   ├── __init__.py
│   │   ├── canvas_view.py
│   │   ├── canvas_scene.py
│   │   └── grid.py
│   │
│   ├── tools/
│   │   ├── __init__.py
│   │   ├── base_tool.py
│   │   ├── selection_tool.py
│   │   ├── rectangle_tool.py
│   │   ├── ellipse_tool.py
│   │   ├── text_tool.py
│   │   └── path_tool.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   ├── document.py
│   │   ├── layer.py
│   │   └── objects.py
│   │
│   ├── panels/
│   │   ├── __init__.py
│   │   ├── tools_panel.py
│   │   ├── properties_panel.py
│   │   └── layers_panel.py
│   │
│   ├── ui/
│   │   ├── __init__.py
│   │   ├── main_window.py
│   │   ├── menu_bar.py
│   │   └── toolbar.py
│   │
│   ├── exporters/
│   │   ├── __init__.py
│   │   ├── svg_exporter.py
│   │   ├── pdf_exporter.py
│   │   └── png_exporter.py
│   │
│   ├── importers/
│   │   ├── __init__.py
│   │   └── svg_importer.py
│   │
│   ├── machine/
│   │   ├── __init__.py
│   │   ├── machine_profile.py
│   │   ├── machine_manager.py
│   │   └── cut_job.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── document_service.py
│       └── settings_service.py
│
├── tests/
│   ├── __init__.py
│   ├── test_document.py
│   ├── test_layers.py
│   └── test_canvas.py
│
├── docs/
│   ├── ARCHITECTURE.md
│   └── DEVELOPMENT.md
│
├── ROADMAP.md
├── HANDOFF.md
├── README.md
├── pyproject.toml
└── .gitignore

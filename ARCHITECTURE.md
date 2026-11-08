# CutStudio Software Architecture

## 1. Project Overview

CutStudio is a Python-based desktop vector design application built
using PySide6 and Qt 6.

The application is intended to support:

- Vector design.
- Vinyl cutting.
- Electronic cutting machines.
- Plotter workflows.
- Physical measurement and layout.
- Multiple document formats.
- Future machine integration.

The project is being developed on Linux Mint using Python 3.12.

The architecture is designed to support cross-platform development.

This document describes the actual architecture and distinguishes
implemented functionality from planned functionality.

---

## 2. Current Architecture

CutStudio currently uses three primary architectural areas:

1. Core document and data management.
2. Canvas rendering and interaction.
3. Main application interface.

### 2.1 Core

Location:

cutstudio/core/

The core package contains the document model and supporting
functionality.

Current modules:

- constants.py
- document.py
- layer.py
- objects.py
- project_file.py
- units.py

Responsibilities:

Document management:
- Create documents.
- Maintain document dimensions.
- Manage document layers.

Layer management:
- Maintain collections of objects.
- Support layer visibility.
- Support layer locking.
- Locate objects within layers.

Object management:
- Represent rectangles.
- Represent ellipses.
- Represent text.
- Maintain object dimensions.
- Maintain object positions.
- Maintain object rotation.
- Validate object properties.
- Generate unique object identifiers.

Project file management:
- Save projects.
- Load projects.
- Validate project file formats.
- Handle project version information.

Unit management:
- Convert millimetres to scene units.
- Convert scene units to millimetres.
- Convert inches to millimetres.

The core package should remain independent of the graphical interface
where practical.

### 2.2 User Interface

Location:

cutstudio/ui/

The UI package contains the graphical application.

Current modules:

- main_window.py

Responsibilities:

- Main application window.
- Menus.
- Toolbars.
- Drawing tool activation.
- Object creation.
- Object selection.
- Object duplication.
- Object deletion.
- Property editing.
- Layer management.
- Project operations.
- Save and load interaction.
- Unsaved-change handling.

The main window coordinates the document model and canvas renderer.

### 2.3 Canvas

Location:

cutstudio/ui/canvas/

Current modules:

- cutting_mat.py
- renderer.py

#### cutting_mat.py

Responsible for canvas interaction.

Current functionality:

- Display the cutting mat.
- Zoom.
- Object selection.
- Rubber-band selection.
- Object movement.
- Object resizing.
- Object rotation.
- Resize handle interaction.
- Rotation handle interaction.
- Shift-based rotation snapping.
- Geometry change notifications.

#### renderer.py

Responsible for translating document objects into Qt graphics items.

Current functionality:

- Create graphics items.
- Add objects to the scene.
- Maintain graphics item references.
- Synchronize graphics items with document objects.
- Rebuild the scene.
- Update object geometry.
- Manage resize handles.
- Manage layer visibility.
- Manage layer locking.
- Duplicate objects.
- Delete objects.

The renderer maintains the relationship between the document model
and the Qt graphics scene.

---

## 3. Actual Directory Structure

The current project structure is:

CutStudio/
|
|-- cutstudio/
|   |
|   |-- __init__.py
|   |-- main.py
|   |
|   |-- core/
|   |   |-- __init__.py
|   |   |-- constants.py
|   |   |-- document.py
|   |   |-- layer.py
|   |   |-- objects.py
|   |   |-- project_file.py
|   |   |-- units.py
|   |
|   |-- ui/
|       |-- __init__.py
|       |-- main_window.py
|       |
|       |-- canvas/
|           |-- __init__.py
|           |-- cutting_mat.py
|           |-- renderer.py
|
|-- tests/
|   |-- test_document.py
|   |-- test_duplication.py
|   |-- test_layers.py
|   |-- test_objects.py
|   |-- test_project_file.py
|   |-- test_renderer.py
|   |-- test_units.py
|
|-- documentation/
|
|-- resources/
|
|-- ARCHITECTURE.md
|-- HANDOFF.md
|-- README.md
|-- ROADMAP.md
|-- requirements.txt
|-- LICENSE
|-- .gitignore

---

## 4. Current Application Workflow

The current application follows this general workflow:

1. The user interacts with the main window.
2. The main window modifies the document model or requests
   canvas operations.
3. The renderer creates or updates Qt graphics items.
4. The cutting mat handles mouse and keyboard interaction.
5. Changes are synchronized back into the document model.
6. The project file module handles saving and loading.

The document model is the authoritative representation of the design.

The graphics scene is its visual representation.

---

## 5. Measurement System

CutStudio uses millimetres as its primary document measurement unit.

Qt graphics items operate using scene coordinates.

The units module provides conversions between these systems.

The application must preserve physical dimensions accurately.

Future cutting and export operations must use the document's physical
measurements rather than relying on screen pixel dimensions.

---

## 6. Current Testing Architecture

Location:

tests/

The project currently uses pytest.

Existing test modules:

- test_document.py
- test_duplication.py
- test_layers.py
- test_objects.py
- test_project_file.py
- test_renderer.py
- test_units.py

The tests currently cover:

- Document creation.
- Document dimensions.
- Layer creation and removal.
- Layer locking.
- Object creation.
- Object validation.
- Object identifiers.
- Object duplication.
- Project saving and loading.
- Renderer operations.
- Position synchronization.
- Unit conversions.

GUI interaction testing remains an area for future expansion.

---

## 7. Architectural Development Principles

### Separation of Responsibilities

Keep document logic separate from graphical interface logic.

Avoid placing document validation and file-format handling inside
the main window.

### Document Independence

The document model should not depend on Qt graphics items.

A document should remain usable by future importers, exporters,
cutting services, and other application components.

### Accurate Measurements

All physical object dimensions must remain accurate.

Unit conversions must be centralized rather than duplicated
throughout the application.

### Testability

New functionality should include appropriate automated tests.

Core functionality should be testable without requiring the
complete graphical application.

### Cross-Platform Compatibility

Use PySide6 and Qt abstractions wherever possible.

Avoid hardcoded operating-system-specific paths.

### Maintainability

Extend the existing architecture before introducing unnecessary
new packages or directory structures.

New modules should have clearly defined responsibilities.

---

## 8. Planned Architectural Expansion

The following areas are planned but are not yet implemented.

### Drawing Tools

Potential future modules:

- Selection tools.
- Freehand drawing.
- Path drawing.
- Polygon drawing.
- Bézier curves.
- Advanced shape tools.

### Import and Export

Planned functionality:

- SVG import.
- SVG export.
- PDF export.
- PNG export.
- Additional vector formats as required.

### Text Editing

Planned functionality:

- Font selection.
- Font size editing.
- Text alignment.
- Text manipulation.
- Text-to-path conversion.

### Machine Integration

Planned functionality:

- Machine profiles.
- Machine configuration.
- Cutting job preparation.
- Cutting job previews.
- Machine communication.
- Support for compatible cutting machines.

### Document Services

Potential future responsibilities:

- Document operations.
- Undo and redo.
- Application settings.
- Autosave.
- Document recovery.

### User Interface Expansion

Potential future modules:

- Dedicated properties panel.
- Dedicated layer panel.
- Additional drawing tool panels.
- Machine configuration interface.

These modules should only be introduced when their responsibilities
justify separation from the existing main window.

---

## 9. Development Priorities

Development should proceed incrementally.

Priority should be given to:

1. Reliable document operations.
2. Object manipulation.
3. Accurate physical dimensions.
4. Undo and redo.
5. Reliable project saving and loading.
6. Improved drawing and editing tools.
7. Vector import and export.
8. Cutting job preparation.
9. Machine integration.

New functionality must not compromise existing document integrity.

---

## 10. Architecture Maintenance

This document must be updated whenever significant architectural
changes are made.

Documentation must reflect the actual implementation.

Do not describe planned functionality as implemented functionality.

Do not introduce imaginary directory structures into the
description of the current application.

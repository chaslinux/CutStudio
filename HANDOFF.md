# CutStudio Development Handoff

Last updated: November 8, 2026

## 1. Project Overview

Project: CutStudio

Description: Cross-platform vector design and vinyl cutting application.

Primary language: Python 3.12

GUI framework: PySide6 / Qt 6

Development operating system: Linux Mint

Desktop environment: Cinnamon

Display server: X11

Development environment: Python virtual environment (.venv)

Project location:

    ~/Code/CutStudio

Application entry point:

    python -m cutstudio.main

Development objective:

Develop a modular vector design and vinyl cutting application inspired by Brother ScanNCut Canvas.

The application should eventually support vector design, editing, document management, importing, exporting, and communication with cutting machines.

## 2. Development Environment

The current development environment uses:

- Linux Mint
- Cinnamon desktop environment
- X11
- Python 3.12
- PySide6
- Git
- pytest
- Xed text editor
- Python virtual environment located in .venv

Activate the development environment:

    cd ~/Code/CutStudio
    source .venv/bin/activate

Launch the application:

    python -m cutstudio.main

Run the test suite:

    python -m pytest -v

Check Git status:

    git status

Inspect outstanding changes:

    git diff

Inspect the change summary:

    git diff --stat

## 3. Current Project Structure

The project has moved beyond its original prototype structure.

Current implementation includes:

    CutStudio/
    |
    +-- cutstudio/
    |   +-- __init__.py
    |   +-- main.py
    |   +-- core/
    |   +-- ui/
    |       +-- main_window.py
    |       +-- canvas/
    |           +-- renderer.py
    |           +-- cutting_mat.py
    |
    +-- tests/
    +-- documentation/
    +-- resources/
    +-- .venv/
    +-- ARCHITECTURE.md
    +-- HANDOFF.md
    +-- README.md
    +-- ROADMAP.md
    +-- LICENSE
    +-- requirements.txt

This is a partial structural overview. Inspect the actual filesystem before documenting additional modules.

## 4. Current Application Architecture

The application uses Qt's graphics framework.

Principal graphics components:

- QGraphicsView
- QGraphicsScene
- QGraphicsRectItem
- QGraphicsEllipseItem
- QGraphicsTextItem

The architecture separates document objects from their graphical representations.

### Core

The cutstudio/core/ directory contains document-related functionality, including:

- Document management
- Layers
- Vector objects
- Object types
- Physical measurement conversions
- Project file operations

### User Interface

The cutstudio/ui/ directory contains the main application interface.

The main window provides:

- Menus
- Toolbar
- Drawing tools
- Properties panel
- Layer management
- Status bar
- Project operations

### Canvas

The cutstudio/ui/canvas/ directory contains the canvas implementation.

renderer.py handles graphical representations of document objects.

cutting_mat.py handles canvas interaction, including:

- Mouse interaction
- Object selection
- Object movement
- Object resizing
- Object rotation
- Resize and rotation handles
- Synchronization between graphics items and document objects

## 5. Confirmed Working Functionality

The following functionality has been implemented and verified during development.

### Application Interface

- Main application window
- Menu bar
- Main toolbar
- Drawing tools
- Properties panel
- Layer panel
- Status bar
- Graphics scene
- Graphics view
- Cutting mat
- Grid display

### Drawing

- Rectangle creation
- Ellipse creation
- Text creation

Rectangle and ellipse objects can be created using their toolbar controls.

### Selection and Movement

- Object selection
- Object movement
- Rubber-band selection
- Multiple object selection
- Selection handles
- Object position synchronization

### Object Duplication

- Duplicate selected objects
- Ctrl+D keyboard shortcut
- Multiple object duplication
- New object IDs for duplicates
- Five-millimetre default duplication offset
- Original objects remain unchanged

### Object Deletion

- Delete selected objects
- Multiple object deletion
- Locked-layer protection

### Resizing

Rectangle and ellipse objects support eight resize handles:

- Northwest
- North
- Northeast
- East
- Southeast
- South
- Southwest
- West

The resize handles remain functional after object rotation.

The resize implementation maintains the opposite edge or corner as the stationary anchor.

When resizing using a single horizontal or vertical handle, the untouched dimension is preserved.

Outstanding feature:

Holding Shift while resizing should constrain the object's aspect ratio.

This has not yet been implemented or verified.

### Rotation

- Rotation handle
- Mouse-driven rotation
- Rotation around object's center
- Rotation property editing
- Rotation preserved in document model
- Shift-assisted rotation snapping

Holding Shift during rotation snaps to 15-degree increments.

### Properties Panel

Editable properties include:

- X position
- Y position
- Width
- Height
- Rotation

Properties are displayed in millimetres and degrees.

Text width and height are currently not directly editable.

### Layers

- Multiple layers
- Active layer selection
- Layer visibility
- Layer locking
- Locked layers prevent object movement and editing
- Locked layers prevent drawing new objects

### Project Management

- Create a new project
- Open an existing project
- Save a project
- Save a project under a new filename
- Project persistence
- Document loading
- Document saving
- Project file validation
- Unsaved-change detection

Project files use the .cutstudio extension.

Saving and reopening an existing project has been tested.

Saving changes and reopening the changed project has also been tested.

Creating a new project replaces the current document after the unsaved-changes workflow.

Outstanding verification:

The user reported that the new-project unsaved-changes workflow did not provide a working cancellation option.

The current source code contains Save, Discard, and Cancel choices in confirm_unsaved_changes().

The actual interface behaviour needs to be reproduced and tested before considering this resolved.

## 6. Automated Testing

As of November 8, 2026, the test suite reported:

    37 passed in 0.18s

The existing tests cover:

- Document creation
- Layer operations
- Object creation
- Object validation
- Object duplication
- Project file saving
- Project file loading
- Renderer operations
- Layer visibility
- Layer locking
- Position synchronization
- Measurement conversions

Run the test suite after every significant code change:

    python -m pytest -v

A passing test suite does not automatically establish that every graphical interaction works correctly.

Mouse-driven operations, keyboard shortcuts, and visual behaviour must also be tested in the running application.

## 7. Outstanding Work and Known Issues

### High Priority

1. Implement Shift-constrained proportional resizing.
2. Verify the unsaved-changes Cancel behaviour.
3. Confirm resizing and rotation at different zoom levels.
4. Verify that object movement, resizing, and rotation are correctly marked as document modifications.
5. Add automated tests for canvas interaction where practical.

### Medium Priority

- Improve object selection behaviour
- Improve properties panel functionality
- Improve keyboard shortcut handling
- Improve document management
- Improve editing workflows
- Expand automated testing

### Future Development

Potential future capabilities include:

- SVG importing
- SVG exporting
- PDF exporting
- PNG exporting
- Additional vector shapes
- Path editing
- More advanced text editing
- Object alignment
- Object distribution
- Grouping and ungrouping
- Additional measurement and layout tools
- Cutting machine profiles
- Machine communication
- Cutting job preparation

These are development objectives, not claims of existing functionality.

## 8. Important Source Files

### Main Window

    cutstudio/ui/main_window.py

Contains:

- Main application interface
- Menus
- Toolbar
- Properties panel
- Layer management
- Project operations
- Drawing operations
- Duplication
- Deletion

### Canvas Renderer

    cutstudio/ui/canvas/renderer.py

Contains:

- Graphics item creation
- Object rendering
- Resize handle creation
- Graphics-to-document synchronization
- Layer visibility
- Layer locking
- Object duplication and deletion support

### Cutting Mat

    cutstudio/ui/canvas/cutting_mat.py

Contains:

- Canvas mouse interaction
- Object resizing
- Object rotation
- Rotation snapping
- Resize handle detection
- Geometry synchronization
- Modification notifications

### Core

    cutstudio/core/

Contains the document model and supporting application logic.

Inspect the directory before modifying core functionality.

## 9. Development Workflow

Before making changes:

    cd ~/Code/CutStudio
    source .venv/bin/activate
    git status

Inspect the relevant source files before editing.

Prefer small, controlled modifications rather than replacing entire files unnecessarily.

After modifications:

    python -m pytest -v

Launch the application:

    python -m cutstudio.main

Test the affected functionality manually.

Review changes:

    git diff

Do not commit changes until the user has reviewed and approved them.

## 10. Documentation Requirements

These requirements are mandatory for all future documentation work and handoffs.

### Markdown Source Requirements

- Provide documentation as raw Markdown source.
- Do not render documentation as rich-text or formatted prose.
- Preserve literal Markdown characters.
- Use actual Markdown heading markers such as #, ##, and ###.
- Use literal Markdown list markers such as -.
- Use literal task markers such as [ ] and [x].
- Use fenced code blocks with their original backticks.
- Preserve Markdown tables where appropriate.
- Documents must be directly copyable into Xed, vi, vim, or another plain-text editor.

### Document Revision Requirements

- When revising an existing Markdown document, provide the complete revised document.
- Do not provide abbreviated replacements.
- Do not omit relevant existing information without explaining why.
- Do not invent implemented functionality.
- Clearly distinguish completed, tested, untested, and planned functionality.
- Keep documentation synchronized with actual source code.

### Development Communication Requirements

- Give complete commands that can be copied directly into the terminal.
- Identify the correct project directory.
- Identify the correct source file before requesting modifications.
- Provide exact insertion or replacement locations.
- Prefer Python scripts or clearly identified editing instructions when larger replacements are necessary.
- Avoid ambiguous instructions that could damage working code.
- Do not assume that an earlier proposed architecture matches the current implementation.

## 11. Current Development Priorities

1. Complete and verify project documentation.
2. Update ARCHITECTURE.md to reflect the actual implementation.
3. Update ROADMAP.md to distinguish completed and planned functionality.
4. Populate README.md.
5. Implement Shift-constrained proportional resizing.
6. Resolve and test the unsaved-changes cancellation issue.
7. Continue improving the ScanNCut-inspired editing workflow.

Documentation should be completed before moving into the next feature-development phase.

## 12. Current Development State

CutStudio is a functioning early-stage vector design application.

It has progressed beyond its original prototype and now includes:

- A document model
- Layers
- Object editing
- Duplication
- Rotation
- Resizing
- Project persistence

The existing automated test suite has 37 passing tests.

The immediate goal is to establish accurate documentation and then continue development without regressing existing functionality.

Important:

Always inspect the current source code before assuming that a feature is implemented or that a proposed change is still necessary.

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
- Middle-mouse drag panning
- Scrollbar-based canvas navigation
- Ctrl + mouse wheel zoom
- Zoom to Fit

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
- Zoom to Fit toolbar control
- Zoom to Fit keyboard shortcut (Ctrl+0)

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

Aspect-ratio constrained resizing:

- Holding Shift while resizing preserves the original aspect ratio.
- Supported by all eight resize handles.
- Works with rotated rectangles and ellipses.
- Edge resizing adjusts both dimensions proportionally.
- Opposite edges and corners remain anchored.
- Normal unrestricted resizing remains available without Shift.

Manually tested and verified.

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

### Unsaved-Change Protection

The unsaved-changes workflow has been manually verified.

Confirmed behaviour:

- New Project → Cancel preserves the existing project.
- New Project → Discard creates a new blank project.
- Application Close → Cancel keeps the application open.
- Application Close → Discard closes without saving.
- Application Close → Save saves successfully before closing.
- Application Close → cancelling Save As keeps the application open.
- Closing an unmodified project requires no confirmation.

MainWindow implements closeEvent() and reuses confirm_unsaved_changes().

All tested behaviours work as expected.

## 6. Automated Testing

As of November 16, 2026, the test suite reported:

    48 passed in 0.16s

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

1. Verify the unsaved-changes Cancel behaviour.
2. Confirm Shift-constrained resizing and rotation at different zoom levels.
3. Verify that object movement, resizing, and rotation are correctly marked as document modifications.
4. Add automated tests for canvas interaction where practical.

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
- Zoom to Fit functionality
- Automatic canvas fitting with a 3% margin around the cutting mat

Middle-mouse panning is supported when the cutting mat
extends beyond the viewport and Qt provides a scrollable area.

The physical document dimensions are independent of canvas
zoom and navigation.

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
2. Verify the unsaved-changes cancellation workflow.
3. Verify resizing and rotation at different zoom levels.
4. Verify document modification tracking for canvas operations.
5. Improve the ScanNCut-inspired editing workflow.

The primary project documentation has been updated. Remaining
development priorities focus on GUI verification, interaction
reliability, and continued editing workflow improvements.

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

The existing automated test suite has 48 passing tests.

Six dedicated tests cover Undo and Redo history.

Shift-constrained proportional resizing and Undo/Redo have been
implemented. GUI-level verification remains necessary.

The immediate goal is to verify outstanding graphical interactions
and continue development without regressing existing functionality.

Important:

Always inspect the current source code before assuming that a feature is implemented or that a proposed change is still necessary.


## 13. Undo and Redo

Undo and Redo functionality has been implemented.

### Implementation

- History is managed by `cutstudio/core/history.py`.
- `UndoHistory` stores independent document snapshots.
- Snapshots use Python deepcopy.
- Undo restores the previous document state.
- Redo restores the next available document state.
- New edits after Undo discard redo history.
- Identical states are not recorded.
- The default history limit is 100 operations.
- History resets when creating or opening a project.

### User Interface

The Edit menu provides Undo and Redo actions with standard
keyboard shortcuts.

Actions are enabled or disabled according to available history.

Restoring a snapshot rebuilds the canvas and refreshes the
layer and property panels.

### Recorded Operations

- Rectangle creation
- Ellipse creation
- Text creation
- Object duplication
- Object deletion
- Property changes
- Object movement
- Resizing
- Rotation
- Layer visibility changes
- Layer locking changes

### Automated Testing

Six dedicated history tests cover initialization, recording,
undo, redo, branching, history limits, and clearing history.

The complete test suite currently reports 48 passing tests.

GUI-level verification remains necessary.

## Development Testing

### Running the Test Suite

Always run tests from the CutStudio project root with the virtual environment activated:

    cd ~/Code/CutStudio
    source .venv/bin/activate
    python -m pytest -v

**Important:** Prefer `python -m pytest` over `pytest` directly.

Running `pytest -v` may result in:

    ModuleNotFoundError: No module named 'cutstudio'

This is an environment/import-path issue, not necessarily an application defect.

### Test Suite Results

The complete automated test suite currently passes.

- Total tests: 51
- Passed: 51
- Failed: 0
- Test framework: pytest 9.2.0
- Python: 3.12.3
- GUI framework: PySide6

Run the complete test suite using:

    python -m pytest -v

#### MainWindow GUI Testing

MainWindow tests run using Qt's offscreen platform.

The test fixture resets `document_modified` before closing the
window to prevent modal unsaved-changes dialogs from blocking
automated test cleanup.

Run MainWindow tests using:

    python -m pytest -v tests/test_main_window.py

Current result: 3 passed.

#### Test Environment Notes

Use `python -m pytest` rather than `pytest` to ensure the
project package is correctly resolved in the development
environment.

### Current Test Status

Latest verified result:

    48 passed in 0.22s

All eight test modules pass:

- test_document.py
- test_duplication.py
- test_history.py
- test_layers.py
- test_objects.py
- test_project_file.py
- test_renderer.py
- test_units.py


## Clipboard Operations (Copy, Cut and Paste)

### Implementation status

Copy, Cut and Paste functionality has been added to the MainWindow.

Files modified:
- `cutstudio/ui/main_window.py`
- `tests/test_main_window.py`

### Keyboard shortcuts

The following shortcuts have been registered:

| Shortcut | Operation |
|---|---|
| Ctrl+C | Copy selected objects |
| Ctrl+X | Cut selected objects |
| Ctrl+V | Paste copied objects |
| Ctrl+D | Duplicate selected objects |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |

Copy, Cut and Paste actions are registered in the Edit menu.

### Current implementation

- Copy stores independent copies of selected objects in an in-memory clipboard.
- Multiple objects can be copied simultaneously.
- Paste creates new objects with unique object IDs.
- Pasted objects are offset by 5 mm in both X and Y directions.
- Paste inserts objects into the active layer.
- Paste rejects locked layers.
- Cut copies selected objects before deleting them.
- Paste and Cut operations support Undo/Redo through the existing history system.
- Repeated Paste operations create independent objects.

The clipboard currently exists only in memory. It is not yet integrated with the operating system clipboard.

### Clipboard testing

Ten new automated tests were added to `tests/test_main_window.py`.

Tests cover:

1. Copying multiple selected objects.
2. Ensuring copied objects are independent of originals.
3. Pasting with new object IDs.
4. Pasting multiple objects.
5. Repeated Paste operations.
6. Paste Undo/Redo.
7. Cutting selected objects.
8. Cut Undo.
9. Cutting and subsequently pasting.
10. Rejecting Paste into locked layers.

### Test results

Command:

`python -m pytest -v -s tests/test_main_window.py -k "copy or paste or cut"`

Result:

- 10 passed
- 3 deselected
- 0 failed

The previous regression baseline was 51 passing tests.

**Important:** The complete test suite has not yet been rerun after adding the clipboard tests. The expected total is 61 tests.

### Next steps

1. Run the complete regression suite:

   `python -m pytest -q`

2. Test Ctrl+C, Ctrl+X and Ctrl+V manually in the CutStudio GUI.

3. Verify that keyboard shortcuts work when the canvas has focus.

4. Verify that Copy and Paste work with multiple selected objects.

5. Verify that Cut, Paste, Undo and Redo work correctly together.

6. Check clipboard behavior when switching between layers.

7. Consider implementing clipboard interoperability with other applications in a future development step.

8. Review the implementation before committing the clipboard changes.

### Current development position

The project has working object creation, selection, duplication, deletion, layer management, document history, Undo/Redo and now initial internal clipboard functionality.

The next immediate task is completing regression testing and manually verifying the clipboard keyboard shortcuts.


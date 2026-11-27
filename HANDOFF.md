# CutStudio Development Handoff

Last updated: November 25, 2026

## 1. Project Overview

Project: CutStudio

Description: Cross-platform vector design and vinyl cutting application.

Primary language: Python 3.12

GUI framework: PySide6 / Qt 6

Primary development operating system: Linux Mint 22.3

Desktop environment: Cinnamon

Display server: X11

Development environment: Python virtual environment (.venv)

Project location:

    ~/Code/CutStudio

Application entry point:

    python -m cutstudio.main

CutStudio is a modular vector design and vinyl cutting application inspired by Brother ScanNCut Canvas.

The long-term objective is to provide vector design, editing, document management, file import and export, and communication with cutting machines.

The project is particularly intended to provide an accessible vector design and cutting environment for Linux users.

Development is ongoing.

## 2. Development Environment

### Primary Development Environment

- Linux Mint 22.3
- Cinnamon desktop environment
- X11
- Python 3.12
- PySide6 / Qt 6
- Git
- pytest
- Xed text editor
- Python virtual environment located in `.venv`

### Temporary Development Environment

A temporary development and compatibility-testing environment uses:

- Ubuntu 26.04
- Wayland

CutStudio has launched successfully in this environment.

Linux Mint 22.3 with X11 remains the primary development target.

Wayland compatibility should continue to be considered during future GUI development and testing.

### Starting Development

Activate the development environment:

    cd ~/Code/CutStudio
    source .venv/bin/activate

Launch the application:

    python -m cutstudio.main

Run the complete test suite:

    python -m pytest -q

Run tests with verbose output:

    python -m pytest -v

Check Git status:

    git status --short

Inspect outstanding changes:

    git diff

Inspect the change summary:

    git diff --stat

Check whitespace errors:

    git diff --check

Always run commands from the project root with the virtual environment activated.

Prefer `python -m pytest` rather than invoking `pytest` directly to ensure that the project package is correctly resolved.

## 3. Project Structure

The project has progressed beyond its original prototype structure.

The following is a partial structural overview:

    CutStudio/
    |
    +-- cutstudio/
    |   +-- __init__.py
    |   +-- main.py
    |   +-- core/

    |   |   +-- history.py
    |   |   +-- mat.py
    |   |   +-- project_file.py
    |   |
    |   +-- ui/
    |       +-- main_window.py
    |       +-- canvas/

    |       |   +-- renderer.py
    |       |   +-- cutting_mat.py
    |       |   +-- rulers.py
    |       |
    |       +-- rulers/
    |       +-- mat_settings_dialog.py
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

This is not a complete filesystem listing.

Inspect the actual filesystem before documenting additional modules or assuming that the structure remains unchanged.

## 4. Current Application Architecture

The application uses Qt's graphics framework.

Principal graphics components include:

- QGraphicsView
- QGraphicsScene
- QGraphicsRectItem
- QGraphicsEllipseItem
- QGraphicsTextItem

The architecture separates document objects from their graphical representations.

### Core

The `cutstudio/core/` directory contains document-related functionality, including:

- Document management.
- Layer management.
- Vector objects.
- Object types.
- Physical measurement conversions.
- Undo and Redo history.
- Cutting mat configuration.
- Native project file operations.

### User Interface

The `cutstudio/ui/` directory contains the main application interface.

The main window provides:

- Menus.
- Toolbar.
- Drawing tools.
- Properties panel.
- Layer management.
- Status bar.
- Project operations.
- Zoom controls.
- Mat configuration access.

### Canvas

The `cutstudio/ui/canvas/` directory contains the canvas implementation.

`renderer.py` handles graphical representations of document objects.

`cutting_mat.py` handles canvas interaction, including:

- Mouse interaction.
- Object selection.
- Object movement.
- Object resizing.
- Object rotation.
- Resize and rotation handles.
- Synchronization between graphics items and document objects.
- Middle-mouse drag panning.
- Scrollbar-based canvas navigation.
- Ctrl + mouse wheel zoom.
- Toolbar zoom operations.
- Zoom to Fit.
- Zoom change notifications.

`rulers.py` provides measurement ruler functionality.

## Canvas Coordinate System

The canvas uses a consistent physical measurement model.

- Document object positions are stored in millimetres.
- Document object dimensions are stored in millimetres.
- Scene coordinates use 96 units per inch.
- Conversion between millimetres and scene units is handled by the core unit conversion functions.
- The cutting mat origin is at the top-left: X = 0, Y = 0.
- X increases to the right.
- Y increases downward.

Object X/Y coordinates represent the geometric object origin, not the visible stroke boundary.

The geometric path determines the object's dimensions and position. Stroke thickness is a visual property and must not silently alter reported object geometry.

## Grid and Snapping

The canvas supports configurable grid spacing and major grid lines.

Current implementation:

- Grid visibility is controlled independently from snapping.
- Grid visibility defaults to enabled.
- Snap to Grid defaults to disabled.
- Default grid spacing is 6.35 mm (1/4 inch).
- Grid spacing can be configured in inches or millimetres.
- Grid spacing presets are provided.
- Major grid line intervals are configurable.
- Available major intervals include 2, 4, 5, and 10 minor grid intervals.
- Major grid lines are visually distinguished from minor grid lines.
- Grid settings are configured through the View menu.

Implementation files:

- `cutstudio/ui/canvas/cutting_mat.py`
- `cutstudio/ui/grid_settings_dialog.py`
- `cutstudio/ui/main_window.py`

Snapping functionality includes:

- Grid snapping for selected objects.
- Group snapping that preserves relative positions of multiple selected objects.
- Geometry-based snapping using `_item_geometric_scene_bounds()` (`item.sceneTransform().mapRect(item.rect())` for shapes and `item.boundingRect()` for text), eliminating visual stroke expansion from snap calculations.
- Grid-based resizing.
- Configurable grid spacing used by snapping calculations.

Important implementation details:

- Scene coordinates use 96 units per inch.
- Physical grid spacing is converted into scene units.
- Grid display and snapping use the same configured spacing.
- Object coordinates remain stored in millimetres.

Further manual GUI verification is required for rotated objects, resizing, and multi-object selections.

### Physical Measurements

The application uses millimetres for physical document measurements and object properties.

Canvas zoom and navigation are independent of physical document dimensions.

Three concepts must remain separate:

1. Physical cutting mat dimensions.
2. Document dimensions.
3. Machine-specific usable cutting area.

Machine-specific usable cutting-area restrictions have not yet been implemented.

## 5. Confirmed Working Functionality

The following functionality has been implemented and verified during development.

### Application Interface

- Main application window.
- Menu bar.
- Main toolbar.
- Drawing tools.
- Properties panel.
- Layer panel.
- Status bar.
- Graphics scene.
- Graphics view.
- Cutting mat.
- Grid display.
- Configurable grid spacing.
- Inch and millimetre grid units.
- Grid spacing presets.
- Configurable major grid line intervals.
- Visually differentiated major and minor grid lines.
- Grid snapping controls.
- Zoom controls.
- Zoom to Fit toolbar control.
- Zoom to Fit keyboard shortcut (Ctrl+0).
- Zoom percentage display.
- Permanent cutting mat dimension display.

### Drawing

- Rectangle creation (25.0 × 25.0 mm default dimensions).
- Ellipse creation (25.0 × 25.0 mm default dimensions).
- Text creation.

Rectangle and ellipse objects can be created using their toolbar controls.

### Selection and Movement

- Object selection.
- Object movement.
- Rubber-band selection.
- Multiple object selection.
- Selection handles.
- Object position synchronization.

### Object Duplication

- Duplicate selected objects.
- Ctrl+D keyboard shortcut.
- Multiple object duplication.
- New object IDs for duplicates.
- Five-millimetre default duplication offset.
- Original objects remain unchanged.
- Duplicate operations support Undo and Redo.

### Object Deletion

- Delete selected objects.
- Multiple object deletion.
- Locked-layer protection.
- Deletion supports Undo and Redo.

### Resizing

Rectangle and ellipse objects support eight resize handles:

- Northwest.
- North.
- Northeast.
- East.
- Southeast.
- South.
- Southwest.
- West.

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

The proportional resizing implementation has been manually tested.

### Rotation

- Rotation handle.
- Mouse-driven rotation.
- Rotation around object's centre.
- Rotation property editing.
- Rotation preserved in document model.
- Shift-assisted rotation snapping.
- Improved rotation handle positioning.
- Rotation handle connecting line.
- Improved mouse hit detection.

Holding Shift during rotation snaps to 15-degree increments.

The rotation handle positioning implementation uses floating-point viewport transformations to prevent visible jumping during slow object rotation.

The rotation handle maintains a 30-screen-pixel offset.

### Properties Panel

Editable properties include:

- X position.
- Y position.
- Width.
- Height.
- Rotation.

Properties are displayed in millimetres and degrees.

Text width and height are currently not directly editable.

### Layers

- Multiple layers.
- Active layer selection.
- Layer visibility.
- Layer locking.
- Locked layers prevent object movement and editing.
- Locked layers prevent drawing new objects.
- Layer visibility and locking changes support Undo and Redo.

Layer creation, deletion, and reordering remain future development priorities.

### Project Management

- Create a new project.
- Open an existing project.
- Save a project.
- Save a project under a new filename.
- Project persistence.
- Document loading.
- Document saving.
- Project file validation.
- Unsaved-change detection.

Project files use the `.cutstudio` extension.

Saving and reopening existing projects has been tested.

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

`MainWindow` implements `closeEvent()` and reuses `confirm_unsaved_changes()`.

### Undo and Redo

Undo and Redo functionality has been implemented.

Implementation:

- History is managed by `cutstudio/core/history.py`.
- `UndoHistory` stores independent document snapshots.
- Snapshots use Python deepcopy.
- Undo restores the previous document state.
- Redo restores the next available document state.
- New edits after Undo discard redo history.
- Identical states are not recorded.
- The default history limit is 100 operations.
- History resets when creating or opening a project.

The Edit menu provides Undo and Redo actions with standard keyboard shortcuts.

Actions are enabled or disabled according to available history.

Restoring a snapshot rebuilds the canvas and refreshes the layer and property panels.

Recorded operations include:

- Rectangle creation.
- Ellipse creation.
- Text creation.
- Object duplication.
- Object deletion.
- Property changes.
- Object movement.
- Resizing.
- Rotation.
- Layer visibility changes.
- Layer locking changes.
- Cut operations.
- Paste operations.

### Clipboard Operations

Copy, Cut and Paste functionality has been implemented in `MainWindow`.

Keyboard shortcuts:

| Shortcut | Operation |
|---|---|
| Ctrl+C | Copy selected objects |
| Ctrl+X | Cut selected objects |
| Ctrl+V | Paste copied objects |
| Ctrl+D | Duplicate selected objects |
| Ctrl+Z | Undo |
| Ctrl+Y | Redo |
| Delete | Delete selected objects |

Copy, Cut and Paste actions are registered in the Edit menu.

Implementation:

- Copy stores independent copies of selected objects in an in-memory clipboard.
- Multiple objects can be copied simultaneously.
- Paste creates new objects with unique object IDs.
- Pasted objects are offset by 5 mm in both X and Y directions.
- Paste inserts objects into the active layer.
- Paste rejects locked layers.
- Cut copies selected objects before deleting them.
- Paste and Cut operations support Undo and Redo through the existing history system.
- Repeated Paste operations create independent objects.

The clipboard currently exists only in memory. It is not yet integrated with the operating system clipboard.

Ten dedicated automated tests cover clipboard functionality.

Manual GUI verification of clipboard operations remains an important part of ongoing development.

## 6. Cutting Mat Configuration

Configurable physical cutting mat dimensions have been implemented.

### Built-in Presets

- 12 × 12 inches.
- 12 × 24 inches.
- 12 × 36 inches.
- 12 × 48 inches.

Custom dimensions are also supported.

### User Interface

Mat settings are accessible through:

    Machine → Mat Settings

Implementation:

- `cutstudio/core/mat.py`
- `cutstudio/ui/mat_settings_dialog.py`

### Project Persistence

Implementation:

- `cutstudio/core/project_file.py`

Mat configuration is saved with native CutStudio projects.

When loading projects:

- Existing mat configuration is restored.
- Older projects without mat configuration receive the default configuration.
- Invalid mat configuration is rejected.
- Document dimensions remain independent of mat dimensions.

### Important Distinction

Three concepts must remain separate:

1. Physical cutting mat dimensions.
2. Document dimensions.
3. Usable cutting area.

Machine-specific usable cutting-area restrictions have not yet been implemented.

### Verification

The following functionality has been implemented:

- Built-in mat presets.
- Custom mat dimensions.
- Mat configuration persistence.
- Restoration of mat configuration when opening projects.
- Default configuration for older projects.
- Mat configuration validation.

Manual verification of mat settings and project persistence was completed during the November 17 development session.

## 7. Canvas Navigation and Measurement

### Zoom Controls

Dedicated Zoom In and Zoom Out controls have been implemented.

The main toolbar provides:

- Zoom In.
- Zoom Out.
- Zoom to Fit.

Keyboard shortcuts:

- Qt standard Zoom In shortcut.
- Qt standard Zoom Out shortcut.
- Ctrl+0 for Zoom to Fit.

The exact Zoom In and Zoom Out key combinations may depend on keyboard layout and platform.

The shared zoom implementation is located in:

    cutstudio/ui/canvas/cutting_mat.py

The `_zoom_by()` method handles zoom transformations for toolbar and mouse-wheel operations.

Current zoom limits:

- Minimum interactive zoom: 10%.
- Maximum interactive zoom: 500%.

Toolbar zoom operations use the viewport centre as their anchor.

Ctrl + mouse wheel zoom uses the mouse position as its anchor.

### Zoom Percentage

`CuttingMat` exposes the `zoom_changed` signal.

The signal reports the current horizontal view scale as a percentage.

`MainWindow` connects this signal to `update_zoom_label()`, which updates a permanent status bar label.

The zoom percentage reflects the actual canvas view transformation rather than the cutting mat dimensions.

### Horizontal and Vertical Measurement Rulers

Horizontal and vertical measurement rulers have been implemented.

Functionality:

- Horizontal ruler.
- Vertical ruler.
- Rulers positioned alongside the canvas viewport.
- Ruler markings synchronized with canvas scrolling.
- Ruler markings synchronized with canvas zoom.
- Inch-based measurements.
- Quarter-inch subdivisions.

Implementation files:

- `cutstudio/ui/canvas/rulers.py`
- `cutstudio/ui/rulers/`

Modified integration files include:

- `cutstudio/ui/canvas/cutting_mat.py`
- `cutstudio/ui/main_window.py`

### Ruler Text Positioning Fix

The horizontal ruler previously exhibited clipping of measurement numbers.

The problem was corrected using `QFontMetrics` to position text using font ascent rather than relying on fixed-height text rectangles.

The vertical ruler implementation remained unchanged.

### Manual Verification

Completed during the November 17 development session:

- Horizontal ruler display.
- Horizontal ruler label positioning.
- Vertical ruler display.
- Mat settings behaviour.
- Cutting mat status display.
- Temporary status message behaviour.

Further verification of ruler alignment and measurement accuracy at different zoom levels and scroll positions remains worthwhile.

### Cutting Mat Status Bar Fix

Cutting mat information previously disappeared when temporary status messages were displayed.

The implementation now uses:

- A permanent `QLabel` for mat dimensions.
- A permanent status widget for zoom percentage.

Mat dimensions update when cutting mat configuration changes.

Accepting unchanged mat settings leaves existing information untouched.

Temporary status messages no longer replace mat information.

Manual verification of these behaviours was completed.

### Configurable Grid

The canvas supports configurable grid spacing and major grid intervals.

Grid settings are accessed through:

    View → Grid Spacing...

The Grid Settings dialog provides:

- Inches and millimetres as display units.
- Preset grid spacing options.
- Major grid interval selection.
- Automatic conversion between inches and millimetres.

Default configuration:

- Grid spacing: 6.35 mm (1/4 inch).
- Major interval: 4 minor grid intervals.
- Major line spacing: 25.4 mm (1 inch).
- Grid visible: enabled.
- Snap to Grid: disabled.

Grid rendering distinguishes major lines from minor lines.

Grid spacing and snapping use the same underlying physical measurement.

Implementation:

- `cutstudio/ui/grid_settings_dialog.py`
- `cutstudio/ui/canvas/cutting_mat.py`
- `cutstudio/ui/main_window.py`

Automated tests cover grid defaults, spacing conversions, preset intervals, and invalid settings.

Further GUI verification should confirm visual clarity at different zoom levels and correct snapping behaviour.

## 8. Automated Testing


### Latest Verified Test Result

    155 passed

Latest verification date:

    November 25, 2026

Command:

    python -m pytest -q

The complete automated test suite passed following implementation of exact `25.0 × 25.0 mm` default rectangle and ellipse creation and stroke-independent geometric snapping (`_item_geometric_scene_bounds()`), along with associated regression tests.

The complete test suite was verified with 155 passing tests.


### Test Coverage

The automated test suite includes coverage for:

- Document creation and management.
- Object creation and validation.
- Default rectangle and ellipse physical dimensions (25.0 × 25.0 mm).
- Object manipulation.
- Object duplication.
- Object deletion.
- Undo and Redo.
- Copy, Cut and Paste.
- Layer management.
- Project saving and loading.
- Project file validation.
- Cutting mat configuration.
- Mat configuration validation.
- Legacy project compatibility.
- Document and mat dimension independence.
- Canvas interaction.
- Stroke-independent geometric snapping (including rotated objects).
- Rendering.
- Main window integration.
- Measurement conversions.
- Ruler and status bar behaviour.
- Grid settings defaults.
- Grid spacing presets.
- Inch-to-millimetre conversion.
- Millimetre grid spacing.
- Major grid interval configuration.
- Grid settings validation.

### Latest Regression Tests

The geometry and snapping regression tests are located in:

- `tests/test_cutting_mat.py`
- `tests/test_main_window.py`

They verify:

- Default rectangle and ellipse creation produces exact `25.0 × 25.0 mm` dimensions.
- Group and single-object snapping ignore visual stroke width expansion (`QPen`).
- Rotated object snapping aligns the geometric scene bounding box without stroke offset.
- Multi-object group snapping preserves relative object positions while excluding locked objects.

### Testing Requirements

Always run the complete test suite after significant application changes.

A passing automated test suite does not automatically establish that graphical interactions work correctly.

Mouse-driven operations, keyboard shortcuts, layout behaviour, visual alignment, and rendering must also be tested in the running application.

### Running Tests

From the project root:

    cd ~/Code/CutStudio
    source .venv/bin/activate
    python -m pytest -q

For verbose output:

    python -m pytest -v

Always report the actual test result rather than relying on a historical result in this document.

## 9. Important Source Files

### Main Window

    cutstudio/ui/main_window.py

Contains:

- Main application interface.
- Menus.
- Toolbar.
- Properties panel.
- Layer management.
- Project operations.
- Drawing operations (25.0 × 25.0 mm default rectangle and ellipse creation).
- Duplication.
- Deletion.
- Clipboard operations.
- Undo and Redo integration.
- Zoom controls.
- Status bar.
- Ruler integration.
- Mat settings integration.

### Canvas Renderer

    cutstudio/ui/canvas/renderer.py

Contains:

- Graphics item creation.
- Object rendering.
- Resize handle creation.
- Graphics-to-document synchronization.
- Layer visibility.
- Layer locking.
- Object duplication and deletion support.

### Cutting Mat

    cutstudio/ui/canvas/cutting_mat.py

Contains:

- Canvas mouse interaction.
- Object selection.
- Object resizing.
- Object rotation.
- Rotation snapping.
- Resize handle detection.
- Geometry synchronization.
- Stroke-independent geometric snapping (`_item_geometric_scene_bounds()`).
- Modification notifications.
- Zoom In and Zoom Out.
- Zoom to Fit.
- Zoom change notifications.
- Automatic canvas fitting with a 3% margin around the cutting mat.

Middle-mouse panning is supported when the cutting mat extends beyond the viewport and Qt provides a scrollable area.

The physical document dimensions are independent of canvas zoom and navigation.

### Grid Settings Dialog

    cutstudio/ui/grid_settings_dialog.py

Contains the configurable grid settings interface.

Provides:

- Inches and millimetres selection.
- Grid spacing presets.
- Major grid interval selection.
- Physical measurement conversion.
- Grid configuration retrieval.

### Grid Settings Tests

    tests/test_grid_settings_dialog.py

Contains automated tests for grid configuration, measurement conversion, preset selection, and validation.

### Measurement Rulers

    cutstudio/ui/canvas/rulers.py

Contains the measurement ruler implementation.

Additional ruler integration files are located in:

    cutstudio/ui/rulers/

Inspect the actual directory contents before modifying ruler functionality.

### Cutting Mat Configuration

    cutstudio/core/mat.py

Contains cutting mat configuration functionality.

### Mat Settings Dialog

    cutstudio/ui/mat_settings_dialog.py

Contains the user interface for configuring cutting mat dimensions.

### Project Persistence

    cutstudio/core/project_file.py

Contains native project saving and loading functionality, including cutting mat configuration persistence and compatibility with older project files.

### History

    cutstudio/core/history.py

Contains Undo and Redo history management.

### Core

    cutstudio/core/

Contains the document model and supporting application logic.

Inspect the directory before modifying core functionality.

## 10. Outstanding Work and Development Priorities

The following items are development objectives, not claims of existing functionality.

### High Priority: Canvas and Navigation

1. Complete manual verification of configurable grid appearance.
2. Verify grid visibility at different zoom levels.
3. Verify major and minor grid line visibility and contrast.
4. Verify grid spacing accuracy in inches and millimetres.
5. Verify grid snapping with individual objects.
6. Verify group snapping with multiple selected objects.
7. Verify snapping behaviour with rotated objects.
8. Verify resizing with grid snapping enabled.
9. Perform manual GUI verification of `25.0 × 25.0 mm` default shapes and stroke-independent geometric snapping.
10. Implement object-to-object snapping.
11. Implement alignment guides.
12. Improve canvas rendering performance.

### Object Editing

- Implement grouping and ungrouping.
- Implement object alignment.
- Implement object distribution.
- Improve multi-object manipulation.
- Improve selection feedback.
- Improve editing workflows.

### Properties and Layers

- Implement fill colour editing.
- Implement stroke colour editing.
- Implement stroke width editing.
- Implement font selection.
- Implement font size editing.
- Implement layer creation.
- Implement layer deletion.
- Implement layer reordering.

### Document Management

- Implement autosave.
- Implement crash recovery.
- Implement recent project list.

### Vector Editing

- Implement path objects.
- Implement freehand drawing.
- Implement Bézier curves.
- Implement node editing.
- Implement path joining.
- Implement path splitting.
- Implement boolean operations.
- Implement improved text editing.
- Implement text-to-path conversion.
- Implement compound paths.

### File Import and Export

- Implement SVG export.
- Implement SVG import.
- Implement PDF export.
- Implement PNG export.
- Preserve physical dimensions during export.
- Preserve object positions and rotations.
- Preserve layers where supported.

### Cutting Machine Integration

- Establish cutter communication architecture.
- Research supported machine protocols.
- Implement machine configuration profiles.
- Implement cutting preview.
- Implement cut job preparation.
- Implement cutter communication.
- Implement job status reporting.
- Implement machine-specific usable cutting areas.
- Implement Brother ScanNCut SDX125 machine profile.
- Verify SVG compatibility with Brother ScanNCut workflows.

## Geometry and Measurement — Status and Requirements

### Resolved on November 25, 2026

1. Default rectangle and ellipse dimensions in `cutstudio/ui/main_window.py` were updated from `100 * 25.4 / 96` (`~26.46 mm`) to exact `25.0 × 25.0 mm`.
2. `_snap_selected_group()` in `cutstudio/ui/canvas/cutting_mat.py` was updated to use `_item_geometric_scene_bounds()` (`item.sceneTransform().mapRect(item.rect())` for shapes and `item.boundingRect()` for text) instead of `item.sceneBoundingRect()`, eliminating the `0.26 mm` (`1 px` half-stroke) coordinate offset during snapping.
3. The underlying 96-units-per-inch coordinate conversion was preserved unchanged.

### Remaining Verification

- Perform manual GUI verification in the running application (`python -m cutstudio.main`) for default rectangle/ellipse dimensions (`25.00 × 25.00 mm`), rotated-object snapping, and resizing with snapping enabled.

### Intended Professional Behaviour

CutStudio should follow established vector-design and cutting-software conventions:

- Exact physical dimensions.
- Predictable millimetre-based positioning.
- Geometry-based coordinates.
- Independent visual stroke properties.
- Reliable grid snapping.
- No unexpected movement when toggling snapping.
- Consistent exported vector geometry.

## 11. Immediate Next Steps

The geometry and stroke-independent snapping fixes have been implemented and verified with automated tests (`155 passed`).

Recommended next steps:

1. Perform manual GUI verification in CutStudio (`python -m cutstudio.main`) of `25.0 × 25.0 mm` default shapes and stroke-independent snapping.
2. Review `git diff` and commit the geometry and snapping changes once verified.
3. Begin implementation of object alignment and distribution tools (`Align Left`, `Align Right`, `Align Top`, `Align Bottom`, `Align Horizontal Centre`, `Align Vertical Centre`, `Distribute Evenly Horizontally`, `Distribute Evenly Vertically`) with Undo/Redo support.
4. Continue manual verification of grid visibility, contrast, and rotated-object snapping.
5. Begin development of object-to-object snapping and alignment guides.

Maintain the existing physical measurement model and 96-units-per-inch scene coordinate system.

Do not introduce changes to coordinate conversion without first investigating their impact on existing geometry, rulers, rendering, and project persistence.

## 12. Git and Repository Management

### Latest Committed History

Latest recorded commit on `main` / `origin/main`:

    bd866c9 Update ROADMAP.md to match progress made up to November 23, 2026.

Preceding recent commits:

    0278bb6 Strengthen project persistence validation
    13938cb Improve undo redo history and selection restoration
    82802d8 Fix undo redo layer state and selection restoration

### Repository State at Last Inspection (November 25, 2026)

Uncommitted tracked modifications (4 files changed, 95 insertions, 12 deletions):

- `cutstudio/ui/canvas/cutting_mat.py`
- `cutstudio/ui/main_window.py`
- `tests/test_cutting_mat.py`
- `tests/test_main_window.py`

Untracked backup files:

- `backups/`
- `cutstudio/core/project_file.py.bak`
- `cutstudio/ui/main_window.py.before_selection_fix`

The backup files must be preserved unless explicitly approved for removal after inspection, and should not be committed automatically.

Latest verified automated test result:

    155 passed

### Important Git Instructions

Always inspect the actual working tree before making changes.

Use:

    git status --short

Inspect differences:

    git diff

Inspect tracked changes:

    git diff --stat

Check whitespace errors:

    git diff --check

Do not assume that previously recorded modifications still exist.

Do not discard application source changes when restoring documentation.

Do not restore, reset, or overwrite files without first inspecting their current contents and Git status.

Do not commit changes until the user has reviewed and approved them.

## 13. Documentation Requirements

These requirements are mandatory for future documentation work and development handoffs.

### Markdown Source Requirements

- Provide documentation as raw Markdown source.
- Do not render documentation as rich-text or formatted prose.
- Preserve literal Markdown characters.
- Use actual Markdown heading markers such as `#`, `##`, and `###`.
- Use literal Markdown list markers such as `-`.
- Use literal task markers such as `[ ]` and `[x]`.
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
- Consolidate development handoffs into the normal `HANDOFF.md`.
- Avoid maintaining separate dated handoff documents as competing sources of truth.
- Preserve relevant historical information where it helps explain implementation decisions or compatibility requirements.
- Update the Last updated date when making substantive documentation changes.

### Development Communication Requirements

- Give complete commands that can be copied directly into the terminal.
- Identify the correct project directory.
- Identify the correct source file before requesting modifications.
- Provide exact insertion or replacement locations.
- Prefer small, controlled modifications rather than unnecessary whole-file replacements.
- Do not use Python heredocs to update Markdown documentation.
- Avoid ambiguous instructions that could damage working code.
- Do not assume that an earlier proposed architecture matches the current implementation.
- Inspect relevant source files before proposing changes.

## 14. Development Policy

- Preserve existing functionality.
- Avoid unnecessary architectural changes.
- Do not rewrite established documentation unnecessarily when updating development status.
- Update the handoff document when significant features are completed.
- Only report functionality as complete when verified.
- Include automated tests for significant functionality.
- Supplement automated testing with manual GUI verification.
- Keep physical mat dimensions separate from document dimensions and usable cutting areas.
- Verify application behaviour in the primary Linux Mint environment.
- Consider Wayland compatibility during GUI development.
- Always inspect current source code before assuming a feature is implemented or a proposed change is still necessary.


## 15. Current Development State

CutStudio is a functioning early-stage vector design application.

The application has progressed substantially beyond its original prototype.

Implemented functionality includes:

- Modular document architecture.
- Qt graphics-based canvas.
- Rectangle, ellipse, and text objects (`25.0 × 25.0 mm` default rectangle and ellipse dimensions).
- Object selection and multi-selection.
- Object movement, resizing, and rotation.
- Eight resize handles.
- Shift-constrained aspect-ratio resizing.
- Rotation snapping in 15-degree increments.
- Object duplication and deletion.
- Copy, Cut, and Paste.
- Undo and Redo history.
- Editable object properties.
- Layer visibility and locking.
- Native project saving and loading.
- Configurable physical cutting mat dimensions.
- Built-in cutting mat presets.
- Custom cutting mat dimensions.
- Cutting mat configuration persistence.
- Zoom controls and Zoom to Fit.
- Horizontal and vertical measurement rulers.
- Canvas panning.
- Physical measurement support using millimetres.
- Permanent zoom percentage display.
- Permanent cutting mat dimension display.
- Configurable grid spacing.
- Grid spacing presets in inches and millimetres.
- Configurable major grid line intervals.
- Improved grid line contrast.
- Independent grid visibility control.
- Snap to Grid for object movement using geometric scene bounds (independent of visual stroke expansion).
- Snap to Grid for object resizing.


### Grid and Snapping

Implemented functionality:

- Configurable grid spacing.
- Inches and millimetres display units.
- Preset grid spacing options.
- Configurable major grid intervals.
- Major and minor grid line rendering.
- Grid visibility control.
- Snap to Grid support using geometric bounds (`_item_geometric_scene_bounds()`).
- Grid-aligned resizing.
- Multi-object group snapping that preserves relative positions.

Default configuration:

- Grid spacing: 6.35 mm (1/4 inch).
- Major interval: 4 minor grid intervals.
- Major line spacing: 25.4 mm (1 inch).
- Grid visible: enabled.
- Snap to Grid: disabled.

Additional automated regression tests cover grid configuration, validation, group snapping, stroke-independent snapping, rotated-object snapping, and `25.0 × 25.0 mm` default object creation.

Further manual GUI verification is recommended for visual clarity at different zoom levels and snapping behaviour with rotated objects and multi-object selections.

### Automated Testing

Latest verified automated test result:

    155 passed

Verification date:

    November 25, 2026

The complete automated test suite passes.

Git whitespace checking also passes.

### Latest Git Commit

Commit:

    bd866c9

Message:

    Update ROADMAP.md to match progress made up to November 23, 2026.

Branch:

    main

Uncommitted changes in working tree:

- `cutstudio/ui/canvas/cutting_mat.py`
- `cutstudio/ui/main_window.py`
- `tests/test_cutting_mat.py`
- `tests/test_main_window.py`

Untracked backup files exist in `backups/` and as `.bak` / `.before_selection_fix` files; do not accidentally include backup files in future commits.

### Current Development Priorities

The configurable grid, geometric snapping, and `25.0 × 25.0 mm` default shape dimension fixes are implemented and passing automated tests (`155 passed`).

The immediate next objective is to perform manual GUI verification, commit these changes, and implement object alignment and positioning tools.

Proposed functionality:

- Align Left.
- Align Right.
- Align Top.
- Align Bottom.
- Align Horizontal Centre.
- Align Vertical Centre.
- Distribute Evenly Horizontally.
- Distribute Evenly Vertically.

Alignment operations should work with multiple selected objects and preserve object dimensions and rotations.

Before implementing these features:

- Inspect the current renderer and object model.
- Review selection handling.
- Review undo/redo integration.
- Add automated tests.
- Verify functionality manually in the GUI.

Always inspect the current source code and Git working tree before making development decisions.

## Latest Development Update — November 23, 2026

### Completed

- Canvas horizontal and vertical rulers.
- Canvas zoom controls, zoom-to-fit and scale limits.
- Ruler updates following scrolling and resizing.
- Grid spacing configurable in inches and millimetres.
- Configurable major grid intervals.
- Group snapping preserves relative object positions.
- Layer visibility and locking.
- Locked layers prevent object modification.
- Resize and rotation protection for locked-layer objects.
- Multi-object duplication across layers.
- Duplication rejects locked-layer selections atomically.
- Multi-object deletion across layers.
- Deletion rejects locked-layer selections atomically.
- Hidden-layer visibility preserved when duplicating.
- Document snapshot-based Undo/Redo history.
- History limits and redo-branch invalidation.
- Main window Undo/Redo integration.
- Document restoration rebuilds canvas graphics items.
- Selection restoration after Undo/Redo where objects still exist.

### Latest Test Results

- Renderer tests: 17 passed.
- History tests: 9 passed.
- Full test suite: 138 passed.

### Current Development Focus

Continue strengthening Undo/Redo integration.

Recommended next regression tests:

1. Undo restores layer visibility and locking.
2. Redo restores layer visibility and locking.
3. Undo/Redo preserves object IDs.
4. Restored graphics items correctly reflect layer properties.
5. Undo/Redo action enabled states remain synchronized.
6. Selection restoration works when objects are removed or restored.

### Development Workflow

Run the complete test suite:

    python -m pytest -q

Run individual test modules when investigating regressions.

Always verify the full suite before committing changes.

### Project Persistence Validation Improvements — November 23, 2026

#### Completed

Additional project persistence validation and regression testing
have been implemented.

Changes to `cutstudio/core/project_file.py`:

- Added duplicate layer ID detection during project loading.
- Added duplicate object ID detection across all document layers.
- Added strict boolean validation for layer visibility.
- Added strict boolean validation for layer locking.
- Invalid project data continues to be reported through
  `ProjectFileError`.

Additional regression tests in `tests/test_project_file.py`:

- Round-trip preservation of layer state.
- Round-trip preservation of object properties.
- Round-trip preservation of multiple layers and objects.
- Document dimension preservation.
- Duplicate layer ID rejection.
- Duplicate object ID rejection.
- Non-finite document dimension rejection.
- Invalid layer visibility rejection.
- Invalid layer locking rejection.
- Invalid JSON rejection.

#### Latest Test Results

Full automated test suite:

    152 passed

Command:

    python -m pytest -q

Formatting verification:

    git diff --check

No formatting errors remain following the final newline correction.

#### Current Development State

The project persistence implementation and associated regression
tests were committed prior to the November 25, 2026 geometry and snapping updates.

### Geometry and Geometric Snapping Fixes — November 25, 2026

#### Completed

- Updated `MainWindow.add_rectangle()` and `MainWindow.add_ellipse()` in `cutstudio/ui/main_window.py` to create exact `25.0 × 25.0 mm` default objects instead of `100 * 25.4 / 96` (`~26.46 mm`).
- Added `CuttingMat._item_geometric_scene_bounds()` in `cutstudio/ui/canvas/cutting_mat.py` and updated `_snap_selected_group()` to snap using geometric scene bounds (`item.sceneTransform().mapRect(item.rect())` for shapes and `item.boundingRect()` for text) rather than `item.sceneBoundingRect()`, eliminating the `0.26 mm` half-stroke coordinate offset.
- Added regression tests in `tests/test_cutting_mat.py` and `tests/test_main_window.py` covering `25.0 × 25.0 mm` default object dimensions, stroke-width independence during snapping, and rotated-object geometric snapping.

## Latest Development Update — November 27, 2026

### Completed

- Implemented object alignment operations.
- Implemented object distribution operations.
- Implemented rotation-aware equal-gap distribution.
- Implemented Ctrl+A to select all visible canvas objects.

### Latest Test Results

Full automated test suite:

    169 passed

Command:

    python -m pytest -q

Formatting verification:

    git diff --check

### Latest Git Commit

Commit:

    0f9519c

Message:

    Add Ctrl+A select all canvas objects

Branch:

    main

### Working Tree Before Documentation Updates

- ROADMAP.md had pending documentation changes.
- No other working-tree changes were reported.

### Current Development Priorities

The next development objective is grouping and ungrouping objects.

Before implementation:

1. Design the document-level group data model.
2. Determine how groups interact with existing layers.
3. Preserve individual object IDs, dimensions and rotations.
4. Establish renderer integration requirements.
5. Plan Undo/Redo integration.
6. Determine project serialization and backward-compatibility requirements.

Grouping should be implemented incrementally with automated regression tests.

### Development Workflow

Run the complete automated test suite:

    python -m pytest -q

Check whitespace and formatting:

    git diff --check

Perform manual GUI verification before committing completed functionality.

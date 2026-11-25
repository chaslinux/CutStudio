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
- history.py
- layer.py
- mat.py
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
- Duplicate vector objects.

Project file management:
- Save projects.
- Load projects.
- Validate project file formats.
- Handle project version information.
- Preserve document dimensions.
- Preserve layer and object information.
- Store physical cutting mat configuration separately
  from document dimensions.
- Support projects without an explicitly stored mat configuration
  using default mat dimensions.

Unit management:
- Convert millimetres to scene units.
- Convert scene units to millimetres.
- Convert inches to millimetres.

Cutting mat configuration:

The `mat.py` module defines the `CuttingMatConfig` dataclass.

Responsibilities:
- Maintain physical cutting mat dimensions in millimetres.
- Validate cutting mat dimensions.
- Reject non-finite dimension values.
- Reject zero and negative dimensions.
- Provide default 12 x 12 inch mat dimensions.

Cutting mat configuration is independent of document dimensions
and document history.

The physical cutting mat configuration determines the graphics
scene dimensions.

History management:

The `history.py` module provides document-level Undo and Redo
functionality through the `UndoHistory` class.

Responsibilities:
- Maintain document history using independent snapshots.
- Create snapshots using Python's `deepcopy`.
- Restore previous document states through Undo.
- Restore subsequent document states through Redo.
- Discard redo history when a new edit follows an Undo.
- Avoid recording identical document states.
- Limit the number of stored operations.
- Reset history when a document is replaced.

The default history limit is 100 operations.

The history module is independent of PySide6 and Qt graphics
components. The main window coordinates history operations
with the graphical interface.

### 2.2 User Interface

Location:

cutstudio/ui/

The UI package contains the graphical application.

Current modules:

- grid_settings_dialog.py
- main_window.py
- mat_settings_dialog.py

Responsibilities:

- Main application window.
- Menus.
- Toolbars.
- Drawing tool activation.
- Zoom to Fit toolbar action and keyboard shortcut (Ctrl+0).
- Object creation (25.0 × 25.0 mm default rectangle and ellipse dimensions).
- Object selection.
- Object duplication.
- Object deletion.
- Property editing.
- Layer management.
- Project operations.
- Save and load interaction.
- Unsaved-change handling.

The main window coordinates the document model and canvas renderer.

Additional responsibilities:

- Copy selected objects.
- Cut selected objects.
- Paste objects into the active layer.
- Keyboard shortcuts for Copy, Cut, Paste, Undo, Redo, and Duplicate.
- Coordinate object editing operations with document history.
- Maintain physical cutting mat configuration.
- Update graphics scene dimensions when mat configuration changes.
- Update the cutting mat dimensions displayed in the status bar.
- Coordinate grid visibility, spacing, major intervals, and snapping settings.
- Coordinate canvas zoom and navigation.
- Display the current canvas zoom percentage.
- Preserve selected objects when restoring document history.

Cutting mat settings:

The `mat_settings_dialog.py` module provides the cutting mat
configuration interface.

Current functionality:

- Provide predefined cutting mat dimensions.
- Support custom cutting mat dimensions.
- Display dimensions in inches.
- Display corresponding dimensions in millimetres.
- Return validated cutting mat configuration.

Available predefined mat sizes:

- 12 x 12 inches.
- 12 x 24 inches.
- 12 x 36 inches.
- 12 x 48 inches.

Custom dimensions are entered in inches and converted to
millimetres.

The main window applies accepted mat configuration changes
independently of document dimensions and document history.

Grid settings:

The `grid_settings_dialog.py` module provides the configurable
grid settings interface.

Current functionality:

- Configure grid spacing in inches or millimetres.
- Select from built-in spacing presets or enter custom values.
- Configure major grid line intervals (2, 4, 5, or 10 minor divisions).
- Validate positive finite spacing and supported major intervals.

### 2.3 Canvas

Location:

cutstudio/ui/canvas/

Current modules:

- cutting_mat.py
- renderer.py
- rulers.py

#### cutting_mat.py

Responsible for canvas interaction.

Current functionality:

- Display the cutting mat.
- Display the canvas grid with configurable spacing and major intervals.
- Zoom using Ctrl + mouse wheel.
- Dedicated Zoom In and Zoom Out controls.
- Zoom In and Zoom Out keyboard shortcuts.
- Zoom to Fit with a 3% margin around the cutting mat.
- Maintain zoom limits of 10% minimum and 500% maximum.
- Display current zoom percentage through a signal.
- Anchor interactive zoom to the mouse position.
- Anchor toolbar zoom operations to the viewport centre.
- Middle-mouse-button canvas panning.
- Object selection.
- Rubber-band selection.
- Object movement.
- Grid snapping and multi-object group snapping using stroke-independent geometric scene bounds (`_item_geometric_scene_bounds()`).
- Object resizing (including grid-aligned resizing).
- Shift-based aspect-ratio constrained resizing.
- Object rotation.
- Resize handle interaction.
- Rotation handle interaction.
- Shift-based rotation snapping.
- Geometry change notifications.

The canvas uses Qt's QGraphicsView framework.

Canvas navigation uses the view transformation matrix and
scrollbars.

The physical cutting mat dimensions determine the scene rectangle.

Document dimensions remain independent of the physical mat.

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
- Manage rotation handles.
- Manage rotation connectors.
- Manage layer visibility.
- Manage layer locking.
- Duplicate objects.
- Delete objects.

The renderer maintains the relationship between the document model
and the Qt graphics scene.

Selection manipulation handles are managed separately from
the underlying document objects.

#### rulers.py

Responsible for displaying measurement rulers around the canvas.

Current functionality:

- Display a horizontal measurement ruler.
- Display a vertical measurement ruler.
- Display measurements in inches.
- Use four minor divisions per inch.
- Display major measurement markings at whole-inch intervals.
- Synchronize ruler markings with canvas scene coordinates.
- Update ruler markings when canvas scrollbars move.
- Maintain alignment with the visible graphics viewport.

The rulers use the canvas transformation to determine visible
measurement positions.

Ruler markings update when the canvas is zoomed or panned.

The ruler implementation follows the physical cutting mat
coordinate system.
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
7. The cutting mat configuration determines the physical
   graphics scene dimensions.
8. The ruler widgets display measurements corresponding
   to the visible canvas coordinates.

The document model is the authoritative representation of the design.

The graphics scene is its visual representation.

The physical cutting mat configuration is maintained separately
from the document model.

Changing the physical cutting mat dimensions does not change
the document dimensions or object geometry.

Project files preserve both document information and physical
cutting mat configuration.

### 4.1 Document and Cutting Mat Independence

CutStudio maintains two separate dimensional concepts.

Document dimensions:
- Define the dimensions of the design document.
- Belong to the document model.
- Are preserved through document history.
- Are stored in the project file.

Physical cutting mat dimensions:
- Define the physical cutting area displayed by the canvas.
- Are maintained through `CuttingMatConfig`.
- Are independent of document history.
- Are stored separately in the project file.
- Determine the graphics scene rectangle.

The canvas displays the physical mat independently of the
document dimensions.

Future machine profiles will need to distinguish physical
mat dimensions from the usable cutting area.

---

## 5. Measurement System

CutStudio uses millimetres as its primary document measurement unit.

Qt graphics items operate using scene coordinates (96 units per inch).

The units module provides conversions between these systems.

The application must preserve physical dimensions accurately.

Future cutting and export operations must use the document's physical
measurements rather than relying on screen pixel dimensions.

### 5.1 Unit Conversion

The core units module provides centralized measurement conversions.

Responsibilities:

- Convert millimetres to scene units.
- Convert scene units to millimetres.
- Convert inches to millimetres.

The application uses a consistent scene coordinate system
for document objects and physical mat positioning.

### 5.2 Cutting Mat Measurements

Physical cutting mat dimensions are stored in millimetres.

The `CuttingMatConfig` dataclass maintains:

- Width in millimetres.
- Height in millimetres.

The default configuration is:

- Width: 304.8 mm.
- Height: 304.8 mm.
- Equivalent dimensions: 12 x 12 inches.

Predefined mat configurations are provided through the
mat settings dialog.

Custom dimensions are entered in inches and converted
to millimetres.

Mat dimensions must be finite and greater than zero.

### 5.3 Measurement Rulers

The canvas includes horizontal and vertical measurement rulers.

Rulers display measurements in inches.

The current ruler configuration uses:

- Four minor divisions per inch.
- Major markings at whole-inch intervals.
- Scene-coordinate positioning.
- Automatic updates following canvas scrolling.
- Automatic updates following canvas zooming.

The ruler widgets use the canvas viewport transformation
to calculate visible measurement positions.

Ruler measurements are independent of screen pixel dimensions.

### 5.4 Zoom and Physical Measurements

Canvas zoom changes the visual scale of the graphics scene.

Zoom does not change:

- Document dimensions.
- Object dimensions.
- Cutting mat dimensions.
- Physical measurement values.

The zoom percentage represents the current graphics view
transformation rather than a change in physical object size.

The application currently limits interactive zoom to
10% minimum and 500% maximum.

---

## 6. Current Testing Architecture

Location:

tests/

The project currently uses pytest (155 passing tests as of November 25, 2026).

Existing test modules:

- test_cutting_mat.py
- test_document.py
- test_duplication.py
- test_grid_settings_dialog.py
- test_history.py
- test_layers.py
- test_main_window.py
- test_mat.py
- test_objects.py
- test_project_file.py
- test_renderer.py
- test_units.py

The tests currently cover:

- Document creation.
- Document dimensions.
- Layer creation and removal.
- Layer locking.
- Object creation (including exact 25.0 × 25.0 mm default rectangle and ellipse dimensions).
- Object validation.
- Object identifiers.
- Object duplication.
- Undo and Redo history.
- Project saving and loading.
- Project validation (duplicate layer/object ID rejection, strict boolean checks).
- Renderer operations.
- Position synchronization.
- Unit conversions.
- Cutting mat configuration.
- Cutting mat dimension validation.
- Project persistence of cutting mat dimensions.
- Grid settings configuration, conversions, and validation.
- Stroke-independent geometric snapping (including rotated objects).
- Canvas zoom and navigation behavior.
- Main window functionality.

GUI interaction testing remains an area for future expansion.

Mouse-driven operations, keyboard shortcuts, ruler appearance,
and visual behavior should continue to receive GUI-level
verification where practical.

### 6.1 Testing Principles

New functionality should include appropriate automated tests.

Core functionality should be tested independently of the GUI.

GUI functionality should be tested using PySide6 test facilities
where practical.

The complete test suite should be executed before significant
changes are committed.

Documentation should only describe functionality that has
been implemented and verified.

---

## 7. Architectural Development Principles

### Separation of Responsibilities

Keep document logic separate from graphical interface logic.

Avoid placing document validation and file-format handling inside
the main window.

Core modules should remain independent of PySide6 wherever practical.

### Document Independence

The document model should not depend on Qt graphics items.

A document should remain usable by future importers, exporters,
cutting services, and other application components.

Document dimensions and physical cutting mat dimensions must
remain separate concepts.

Changing the cutting mat configuration must not modify
document geometry or document history.

### Accurate Measurements

All physical object dimensions must remain accurate.

Unit conversions must be centralized rather than duplicated
throughout the application.

Physical cutting mat dimensions are stored in millimetres.

Canvas rulers must display measurements corresponding to
scene coordinates rather than screen pixel dimensions.

Zooming and panning must not alter physical measurements.

### Testability

New functionality should include appropriate automated tests.

Core functionality should be testable without requiring the
complete graphical application.

GUI functionality should receive automated testing where practical.

Mouse-driven operations and visual behavior should also be
verified through application testing.

### Cross-Platform Compatibility

Use PySide6 and Qt abstractions wherever possible.

Maintain compatibility with both X11 and Wayland environments.

Avoid display-server-specific canvas implementations.

Avoid hardcoded operating-system-specific paths.

Use Qt-provided platform integration and bundled dependencies
where appropriate.

### Maintainability

Extend the existing architecture before introducing unnecessary
new packages or directory structures.

New modules should have clearly defined responsibilities.

Keep the document model authoritative.

Avoid duplicating document state between the model and renderer.

Preserve existing functionality when introducing new features.
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

Import and export functionality should operate on the core
document model rather than depending directly on graphics
scene objects.

Physical measurements must be preserved during file conversion.

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

Machine configuration should distinguish between:

- Physical cutting mat dimensions.
- Usable cutting area.
- Machine-specific operating restrictions.

Machine-specific limitations should not be assumed to be
identical to physical mat dimensions.

### Document Services

Potential future responsibilities:

- Document operations.
- Application settings.
- Autosave.
- Document recovery.
- Recent project management.

### User Interface Expansion

Potential future modules:

- Dedicated properties panel.
- Dedicated layer panel.
- Additional drawing tool panels.
- Machine configuration interface.
- Configurable ruler units.

These modules should only be introduced when their responsibilities
justify separation from the existing main window.

### Canvas Expansion

Planned functionality:

- Object-to-object snapping.
- Alignment guides.
- Improved canvas rendering performance.
- Additional measurement units.
- Improved ruler presentation.
- More advanced navigation controls.

Canvas enhancements should preserve accurate physical
measurement behavior.

---

## 9. Development Priorities

Development should proceed incrementally.

Priority should be given to:

1. Reliable document operations.
2. Object manipulation.
3. Accurate physical dimensions.
4. Reliable project saving and loading.
5. Improved drawing and editing tools.
6. Vector import and export.
7. Cutting job preparation.
8. Machine integration.

Existing functionality must not regress when new features
are introduced.

New functionality should be accompanied by appropriate
automated tests.

Documentation must accurately distinguish implemented
functionality from planned functionality.

The application should remain modular and maintainable
as additional capabilities are introduced.

---

## 10. Architecture Maintenance

This document must be updated whenever significant architectural
changes are made.

Documentation must reflect the actual implementation.

Do not describe planned functionality as implemented functionality.

Do not introduce imaginary directory structures into the
description of the current application.

Maintain consistency between:

- ARCHITECTURE.md
- HANDOFF.md
- ROADMAP.md

New modules should be documented with their actual responsibilities.

Changes to document persistence, measurement handling, canvas
interaction, or application workflow should be reflected in
this document.

---

## 11. Document History

### 11.1 Core History Module

Location:

`cutstudio/core/history.py`

The `UndoHistory` class manages document history independently
of the graphical user interface.

History uses independent document snapshots created with deepcopy.

Responsibilities:

- Record document states.
- Restore previous document states through Undo.
- Restore subsequent document states through Redo.
- Discard redo history when a new edit follows an Undo.
- Avoid recording identical document states.
- Limit the number of stored operations.
- Reset history when a document is replaced.

The default history limit is 100 operations.

### 11.2 Clipboard and Editing Integration

The main window coordinates clipboard operations with document
history.

- Copy operations maintain independent clipboard snapshots.
- Cut operations copy selected objects before deletion.
- Paste operations create new objects with unique identifiers.
- Paste operations respect active-layer locking.
- Paste operations place duplicated objects with a 5 mm offset.
- Cut, Paste, and Duplicate operations integrate with Undo and Redo.

Clipboard contents are maintained independently of document
history.

### 11.3 History Operations

The `UndoHistory` class provides the following operations:

- `record(document)` - Record a document state.
- `undo()` - Return the previous document state.
- `redo()` - Return the next document state.
- `clear(document)` - Reset history.

Available properties:

- `can_undo`
- `can_redo`
- `undo_count`
- `redo_count`

The default history limit is 100 operations.

Recording a new state after Undo discards unreachable redo states.

Identical document states are ignored.

### 11.4 Main Window Integration

`cutstudio/ui/main_window.py` integrates history with the Edit menu.

The main window handles:

- Recording document changes.
- Undo and Redo actions.
- Restoring document snapshots.
- Updating the renderer.
- Rebuilding the graphics scene.
- Refreshing layer and property panels.
- Resetting history when replacing a project.
- Preserving selected objects where possible during restoration.

The history module has no PySide6 or Qt graphics dependency.

### 11.5 Testing

Location:

`tests/test_history.py`

History functionality is tested independently of the GUI.

Six dedicated Undo and Redo tests were established in the
initial history implementation.

Command-based history may be considered in the future if
snapshot memory consumption becomes significant.
---

## 12. Canvas Zoom, Grid, and Manipulation Improvements

### 12.1 Zoom Reporting

The canvas is implemented using `QGraphicsView`.

Zoom is controlled through the view transformation matrix.

The `CuttingMat` class provides a `zoom_changed` signal that
reports the current zoom percentage.

The zoom percentage is calculated from the horizontal
transformation scale:

    self.transform().m11() * 100

Zoom changes are reported when:

- Ctrl + mouse wheel changes the zoom.
- Zoom In is activated.
- Zoom Out is activated.
- Zoom to Fit is activated.

The main window connects this signal to its status bar,
where a permanent label displays the current percentage.

The zoom percentage is based on the view transformation,
not on the physical dimensions of the cutting mat.

### 12.2 Zoom Controls

The canvas provides:

- Ctrl + mouse wheel zoom.
- Dedicated Zoom In and Zoom Out toolbar controls.
- Standard Qt Zoom In and Zoom Out keyboard shortcuts.
- Zoom to Fit.
- Interactive zoom limits of 10% minimum and 500% maximum.

Toolbar zoom operations use the viewport centre as their anchor.

Ctrl + mouse wheel zoom uses the mouse position as its anchor.

All zoom operations use the same internal zoom handling.

### 12.3 Measurement Rulers

The canvas includes horizontal and vertical measurement rulers.

Implementation:

`cutstudio/ui/canvas/rulers.py`

The ruler widgets:

- Display measurements in inches.
- Use four minor divisions per inch.
- Display major markings at whole-inch intervals.
- Calculate visible measurement positions using canvas coordinates.
- Update when horizontal or vertical scrollbars move.
- Update when the canvas is zoomed.
- Remain aligned with the graphics viewport.

The rulers are positioned around the graphics viewport
using viewport margins.

The horizontal and vertical rulers are independent widgets.

A corner widget fills the space where the two rulers meet.

Ruler measurements follow the physical cutting mat coordinate
system and do not depend on screen pixel dimensions.

### 12.4 Cutting Mat Configuration

Physical cutting mat configuration is maintained by:

`cutstudio/core/mat.py`

The `CuttingMatConfig` dataclass stores:

- Width in millimetres.
- Height in millimetres.

The default configuration is 12 x 12 inches.

The configuration validates that dimensions are finite
and greater than zero.

The user interface for mat configuration is implemented in:

`cutstudio/ui/mat_settings_dialog.py`

Available presets:

- 12 x 12 inches.
- 12 x 24 inches.
- 12 x 36 inches.
- 12 x 48 inches.

Custom dimensions can also be entered.

The main window:

- Maintains the current mat configuration.
- Updates the graphics scene rectangle.
- Updates the canvas view.
- Updates the cutting mat dimensions displayed in the status bar.

Mat configuration is independent of document dimensions
and document history.

### 12.5 Canvas Panning

The canvas supports middle-mouse-button dragging.

Panning uses Qt scrollbars.

The cutting mat must extend beyond the viewport for scrollbar
movement to be possible.

Canvas rulers update as the scrollbars move.

### 12.6 Resize and Rotation Handles

`CanvasRenderer` manages the selection manipulation handles.

Resize handles are separate graphics items rather than
children of the document objects.

The renderer maintains the handles and rotation connector
during updates rather than unnecessarily recreating them.

The rotation control consists of:

- A circular rotation handle.
- A connecting line.
- A position calculated relative to the object's local
  upward direction.

The rotation handle maintains a 30-screen-pixel offset
from the top-middle resize handle.

The handle and connector follow the object's rotation.

### 12.7 Rotation Handle Positioning

Rotation handle positioning uses the view's viewport
transformation matrix.

Floating-point coordinates are retained when converting
between scene and viewport coordinates.

This avoids the integer rounding introduced by
`mapFromScene()` and prevents visible positional jitter
during slow rotation.

The rotation handle also receives priority during mouse
hit detection, with a larger interaction area than the
resize handles.

### 12.8 Configurable Grid and Stroke-Independent Geometric Snapping

`CuttingMat` renders a configurable physical grid and performs
grid snapping using geometric bounds rather than Qt's stroke-expanded
`sceneBoundingRect()`.

- Default grid spacing is 6.35 mm (1/4 inch) with major lines every
  4 minor divisions (25.4 mm / 1 inch).
- `GridSettingsDialog` (`cutstudio/ui/grid_settings_dialog.py`) allows
  configuring spacing in inches or millimetres, selecting presets, and
  choosing major line intervals (2, 4, 5, or 10).
- `_item_geometric_scene_bounds(item)` maps the unstroked local
  geometry (`item.rect()` for `QGraphicsRectItem` and `QGraphicsEllipseItem`,
  and `item.boundingRect()` for `QGraphicsTextItem`) through
  `item.sceneTransform().mapRect(...)`, ensuring grid snapping and
  multi-object group snapping remain accurate for both unrotated and
  rotated objects regardless of `QPen` stroke width.
- Default rectangle and ellipse creation (`MainWindow.add_rectangle()` and
  `MainWindow.add_ellipse()`) uses exact `25.0 × 25.0 mm` dimensions.

### 12.9 Canvas Interaction

Current canvas interaction includes:

- Ctrl + mouse wheel zoom.
- Dedicated Zoom In and Zoom Out toolbar controls.
- Zoom In and Zoom Out keyboard shortcuts.
- Zoom to Fit.
- Interactive zoom limits.
- Mouse-position-anchored zoom.
- Viewport-centre-anchored toolbar zoom.
- Zoom percentage notifications.
- Middle-mouse-button panning.
- Horizontal and vertical measurement rulers.
- Configurable grid display and stroke-independent grid snapping.
- Object selection and multi-selection.
- Object movement.
- Object resizing.
- Aspect-ratio constrained resizing.
- Object rotation.
- Shift-based rotation snapping.
- Rotation handle and connector positioning.

These features are implemented in:

- `cutstudio/ui/canvas/cutting_mat.py`
- `cutstudio/ui/canvas/renderer.py`
- `cutstudio/ui/canvas/rulers.py`
- `cutstudio/ui/grid_settings_dialog.py`

The main window coordinates canvas controls and status
information through:

`cutstudio/ui/main_window.py`

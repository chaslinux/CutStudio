# CutStudio Development Roadmap

Last updated: November 24, 2026

## 1. Project Vision

CutStudio is a cross-platform desktop vector design and vinyl cutting
application built with Python and PySide6.

The goal is to create an accessible, reliable design environment for
vinyl cutting, plotter workflows, and other vector-based fabrication
projects.

CutStudio is inspired by established vector design and cutting
applications, including Brother ScanNCut Canvas.

The long-term objective is to provide a capable vector design
environment that supports professional editing workflows, accurate
physical measurements, common vector file formats, and communication
with multiple cutting machines.

The application should eventually support:

- Linux.
- Windows.
- macOS.
- Multiple cutting machines.
- Common vector file formats.
- Accurate physical measurements.
- Professional vector editing workflows.
- Reliable document management.
- Vector geometry suitable for fabrication and cutting.

### Core Principles

- Cross-platform compatibility.
- Reproducible installation.
- Modular architecture.
- Accurate physical measurements.
- Non-destructive editing wherever practical.
- Open vector file formats.
- Extensible machine support.
- Reliable document handling.
- Predictable object positioning and geometry.
- Preservation of document accuracy during editing and export.

### Intended Application Direction

CutStudio is intended to become a vector design and fabrication
application rather than a general-purpose raster graphics editor.

Development should prioritize functionality that supports:

- Creating and editing vector designs.
- Precise positioning and sizing of objects.
- Working with multiple objects and layers.
- Preparing designs for vinyl cutting and plotter workflows.
- Importing and exporting standard vector formats.
- Preparing designs for specific cutting machines.
- Maintaining accurate physical dimensions throughout the workflow.

Machine-specific functionality should remain separate from general
document editing wherever practical.

The physical cutting mat, document dimensions, and machine-specific
usable cutting area must remain independent concepts.

---

## 2. Current Development Status

CutStudio has progressed substantially beyond its original prototype.

The application currently includes:

### Application Architecture

- Modular Python application architecture.
- PySide6 and Qt 6 graphical interface.
- Qt graphics-based canvas.
- Separation between document objects and graphical representations.
- Core document and layer management.
- Physical measurement conversion functions.
- Native project file handling.

### Canvas and Navigation

- Cutting mat display.
- Configurable physical cutting mat dimensions.
- Built-in cutting mat presets.
- Custom cutting mat dimensions.
- Grid display.
- Configurable grid spacing.
- Grid spacing presets in inches and millimetres.
- Configurable major grid line intervals.
- Visually differentiated major and minor grid lines.
- Grid visibility control.
- Grid snapping.
- Multi-object group snapping.
- Zoom In and Zoom Out.
- Zoom to Fit.
- Ctrl + mouse wheel zoom.
- Middle-mouse-button canvas panning.
- Horizontal measurement ruler.
- Vertical measurement ruler.
- Permanent zoom percentage display.
- Permanent cutting mat dimension display.

### Object Editing

- Rectangle objects.
- Ellipse objects.
- Text objects.
- Object selection and multi-selection.
- Object movement.
- Eight resize handles.
- Resizing of rotated objects.
- Shift-constrained aspect-ratio resizing.
- Object rotation.
- Rotation snapping in 15-degree increments.
- Object duplication.
- Object deletion.
- Copy, Cut and Paste.
- Editable object position and dimension properties.

### Layers and Document Management

- Multiple layers.
- Layer visibility.
- Layer locking.
- Protection of locked-layer objects.
- Native project saving and loading.
- Cutting mat configuration persistence.
- Project file validation.
- Unsaved-change protection.
- Undo and Redo history.
- Document snapshot restoration.
- Selection restoration following document restoration.

### Automated Testing

Latest verified automated test result:

    152 passed

Verification date:

    November 24, 2026

Command:

    python -m pytest -q

The automated test suite covers core document functionality,
object editing, canvas integration, project persistence, history,
clipboard operations, grid configuration, and other application
functionality.

Automated test success does not replace manual verification of
interactive GUI behaviour.

### Manual Verification

Manual GUI verification has been completed for several existing
features, including:

- Cutting mat configuration.
- Ruler display and text positioning.
- Cutting mat status bar behaviour.
- Unsaved-change protection.
- Object resizing and rotation.
- Aspect-ratio-constrained resizing.
- Cutting mat project persistence.

Further manual verification remains necessary for:

- Grid appearance at different zoom levels.
- Grid spacing accuracy.
- Major and minor grid line visibility.
- Individual and group snapping.
- Snapping with rotated objects.
- Resizing with snapping enabled.
- Ruler alignment and measurement accuracy.
- General canvas navigation.

The application is under active development. Implemented functionality
should not automatically be considered fully verified in every
possible interaction or operating environment.

---

## 3. Development Phases

Development should proceed incrementally through the following
phases.

Completed functionality is marked `[x]`.

Outstanding functionality is marked `[ ]`.

A feature should only be marked complete after implementation
and appropriate verification.

### Phase 1: Foundation and Architecture

Status: Substantially Complete

- [x] Establish Python virtual environment.
- [x] Install PySide6.
- [x] Create application entry point.
- [x] Implement main application window.
- [x] Implement menu bar.
- [x] Implement main toolbar.
- [x] Implement drawing tools.
- [x] Implement properties and layers panels.
- [x] Establish core document architecture.
- [x] Implement document model.
- [x] Implement layer model.
- [x] Implement vector object model.
- [x] Implement physical measurement conversions.
- [x] Implement initial cutting mat.
- [x] Implement graphics-based canvas.
- [x] Establish automated test suite.
- [ ] Establish reproducible cross-platform Qt configuration.
- [ ] Document complete installation requirements.
- [ ] Implement automated application startup tests.
- [ ] Verify installation and application startup on Windows.
- [ ] Verify installation and application startup on macOS.
- [ ] Establish documented release and packaging procedures.

Future architectural development should preserve separation
between document logic, graphical presentation, and machine-specific
functionality.

### Phase 2: Canvas and Navigation

Status: Substantially Complete

#### Implemented

- [x] Implement cutting mat display.
- [x] Implement configurable cutting mat dimensions.
- [x] Implement built-in cutting mat presets.
- [x] Implement custom cutting mat dimensions.
- [x] Implement grid display.
- [x] Implement configurable grid spacing.
- [x] Implement grid spacing presets.
- [x] Support grid spacing in inches and millimetres.
- [x] Implement configurable major grid intervals.
- [x] Distinguish major and minor grid lines.
- [x] Implement independent grid visibility control.
- [x] Implement grid snapping.
- [x] Implement grid-aligned object resizing.
- [x] Implement multi-object group snapping.
- [x] Preserve relative object positions during group snapping.
- [x] Implement Ctrl + mouse wheel zoom.
- [x] Implement dedicated Zoom In and Zoom Out controls.
- [x] Implement Zoom to Fit.
- [x] Implement middle-mouse-button canvas panning.
- [x] Display current zoom percentage.
- [x] Display cutting mat dimensions permanently.
- [x] Implement horizontal measurement ruler.
- [x] Implement vertical measurement ruler.
- [x] Synchronize rulers with canvas scrolling.
- [x] Synchronize rulers with canvas zoom.
- [x] Persist cutting mat configuration in project files.

#### Outstanding

- [ ] Complete manual verification of grid appearance.
- [ ] Verify grid visibility at different zoom levels.
- [ ] Verify grid spacing accuracy in inches and millimetres.
- [ ] Verify major and minor grid line contrast.
- [ ] Verify individual object snapping.
- [ ] Verify multi-object group snapping.
- [ ] Verify snapping with rotated objects.
- [ ] Verify resizing with snapping enabled.
- [ ] Investigate geometry-based snapping independently of stroke
      expansion.
- [ ] Implement object-to-object snapping.
- [ ] Implement alignment guides.
- [ ] Improve canvas rendering performance.
- [ ] Further improve canvas navigation usability.

#### Canvas Navigation

Current navigation functionality:

- Middle mouse button + drag pans the canvas.
- Panning uses Qt scrollbars.
- Ctrl + mouse wheel zooms in and out.
- Zoom to Fit restores the complete cutting mat to view.
- Dedicated toolbar buttons provide Zoom In and Zoom Out.
- Standard Qt keyboard shortcuts provide Zoom In and Zoom Out.
- Interactive zoom is limited to 10% minimum and 500% maximum.
- Toolbar zoom operations use the viewport centre as their anchor.
- Mouse-wheel zoom uses the mouse position as its anchor.
- The status bar reports the current zoom percentage.
- Horizontal and vertical rulers display physical measurements.

The zoom percentage represents the actual canvas view transformation,
not the physical dimensions of the cutting mat.

Further manual verification should cover different window sizes,
zoom levels, cutting mat dimensions, and scroll positions.

#### Grid and Snapping

Default grid configuration:

- Grid spacing: 6.35 mm (1/4 inch).
- Major interval: 4 minor grid intervals.
- Major line spacing: 25.4 mm (1 inch).
- Grid visible: enabled.
- Snap to Grid: disabled.

Grid display and snapping use the same configured physical spacing.

Grid visibility and snapping are independent settings.

Document object coordinates remain stored in millimetres.

Object-to-object snapping and alignment guides are separate
capabilities and remain outstanding.

### Phase 3: Object Editing

Status: In Progress

#### Implemented

- [x] Implement rectangle objects.
- [x] Implement ellipse objects.
- [x] Implement text objects.
- [x] Implement object selection.
- [x] Implement multi-selection.
- [x] Implement rubber-band selection.
- [x] Implement object movement.
- [x] Implement eight resize handles.
- [x] Support resizing after object rotation.
- [x] Implement opposite-edge and opposite-corner resize anchoring.
- [x] Implement Shift + resize aspect-ratio locking.
- [x] Support aspect-ratio locking with all eight resize handles.
- [x] Implement object rotation.
- [x] Implement rotation handle.
- [x] Implement rotation handle connector.
- [x] Improve rotation handle hit detection.
- [x] Improve rotation handle positioning stability.
- [x] Implement rotation snapping with Shift.
- [x] Snap rotation to 15-degree increments.
- [x] Implement object duplication.
- [x] Implement Ctrl+D duplication shortcut.
- [x] Implement object deletion.
- [x] Implement unique object identifiers.
- [x] Implement object validation.
- [x] Implement Copy.
- [x] Implement Cut.
- [x] Implement Paste.
- [x] Implement Undo and Redo.
- [x] Implement document snapshot-based history.
- [x] Implement history limits.
- [x] Implement redo-branch invalidation following new edits.
- [x] Implement restoration of document state.
- [x] Implement restoration of layer visibility and locking.
- [x] Preserve object identifiers during history restoration.
- [x] Implement selection restoration where objects still exist.
- [x] Synchronize graphics items following document restoration.

#### Outstanding

- [ ] Implement grouping and ungrouping.
- [ ] Implement object alignment.
- [ ] Implement object distribution.
- [ ] Improve multi-object manipulation.
- [ ] Improve selection feedback.
- [ ] Improve text editing.
- [ ] Implement additional vector object types.
- [ ] Improve geometry consistency across different zoom levels.
- [ ] Investigate object positioning discrepancies.
- [ ] Implement more advanced object transformation workflows.

#### Multi-Object Editing

Future multi-object editing should support predictable manipulation
of several selected objects.

Operations should preserve:

- Individual object dimensions.
- Individual object rotations.
- Relative object positions where appropriate.
- Unique object identifiers.
- Layer assignments.
- Undo and Redo behaviour.

Grouping and ungrouping should integrate with the existing document
and history architecture.

Object alignment and distribution should operate on selected
objects and provide predictable geometric results.

#### Clipboard Operations

Current clipboard functionality:

- Copy selected objects.
- Cut selected objects.
- Paste copied objects.
- Support multiple selected objects.
- Generate new identifiers for pasted objects.
- Insert pasted objects into the active layer.
- Offset pasted objects by 5 mm in X and Y.
- Reject paste operations on locked layers.
- Support Undo and Redo.
- Maintain independent copies for repeated paste operations.

The clipboard currently exists in application memory.

Operating system clipboard integration remains a possible future
improvement.

### Phase 4: Properties and Layers

Status: Partially Complete

#### Implemented

- [x] Display selected object type.
- [x] Implement X position editing.
- [x] Implement Y position editing.
- [x] Implement width editing.
- [x] Implement height editing.
- [x] Implement rotation editing.
- [x] Display measurements in millimetres and degrees.
- [x] Synchronize properties with canvas geometry.
- [x] Implement layer selection.
- [x] Implement multiple layers.
- [x] Implement layer visibility.
- [x] Implement layer locking.
- [x] Prevent movement of objects on locked layers.
- [x] Prevent editing objects on locked layers.
- [x] Prevent drawing on locked layers.
- [x] Protect locked-layer objects during duplication and deletion.
- [x] Preserve layer visibility when duplicating objects.
- [x] Support layer visibility and locking through Undo and Redo.
- [x] Refresh properties following document restoration.

#### Outstanding

- [ ] Implement fill colour editing.
- [ ] Implement stroke colour editing.
- [ ] Implement stroke width editing.
- [ ] Implement font selection.
- [ ] Implement font size editing.
- [ ] Implement layer creation.
- [ ] Implement layer deletion.
- [ ] Implement layer reordering.
- [ ] Improve layer management interface.
- [ ] Improve multi-selection property editing.
- [ ] Improve property panel usability.
- [ ] Implement appropriate property validation and constraints.

Future property editing must maintain synchronization between
the document model, canvas representation, and Undo/Redo history.

Properties should use the application's physical measurement
model consistently.

Text width and height are not currently directly editable.

Layer operations must respect layer visibility and locking rules.

### Phase 5: Document Management

Status: Substantially Complete

#### Implemented

- [x] Implement document creation.
- [x] Implement document dimensions.
- [x] Implement document layers.
- [x] Implement native CutStudio project format.
- [x] Implement project saving.
- [x] Implement project loading.
- [x] Implement JSON-based project serialization.
- [x] Implement project validation.
- [x] Implement project version checking.
- [x] Implement document reconstruction.
- [x] Implement modified-document tracking.
- [x] Implement unsaved-change detection.
- [x] Implement save confirmation.
- [x] Implement discard confirmation.
- [x] Verify Cancel behaviour for unsaved changes.
- [x] Implement application-close confirmation.
- [x] Verify Save, Discard, and Cancel when closing the application.
- [x] Implement Undo and Redo history.
- [x] Implement cutting mat configuration persistence.
- [x] Maintain separation between document dimensions and physical
      cutting mat dimensions.
- [x] Implement backward compatibility for older project files.
- [x] Detect duplicate layer identifiers during project loading.
- [x] Detect duplicate object identifiers across document layers.
- [x] Validate layer visibility values strictly as booleans.
- [x] Validate layer locking values strictly as booleans.
- [x] Reject non-finite document dimensions.
- [x] Report invalid project data through ProjectFileError.
- [x] Add project persistence regression tests.

#### Outstanding

- [ ] Implement autosave.
- [ ] Implement crash recovery.
- [ ] Implement recent project list.
- [ ] Improve project recovery and error reporting.
- [ ] Consider native project format migration support.
- [ ] Expand project compatibility testing.
- [ ] Improve recovery from interrupted or incomplete saves.

#### Project Persistence

The native project format currently supports persistence of:

- Document identification.
- Document dimensions.
- Active layer identification.
- Layer names.
- Layer visibility.
- Layer locking.
- Vector object properties.
- Object positions and dimensions.
- Object rotation.
- Object fill and stroke properties.
- Text content and font properties.
- Physical cutting mat dimensions.

Cutting mat configuration is independent of document dimensions
and is persisted separately in project data.

Older project files without cutting mat configuration receive
the default cutting mat configuration.

Project validation includes checks for:

- Valid project structure.
- Valid document dimensions.
- Unique layer identifiers.
- Unique object identifiers across layers.
- Valid layer visibility.
- Valid layer locking.
- Valid JSON data.
- Valid cutting mat configuration.

Any future changes to the native project format must include
appropriate backward-compatibility tests.

Project persistence must remain reliable as new object types,
properties, layers, and vector editing capabilities are introduced.

### Phase 6: Vector Editing

Status: Planned

Vector editing is a major future development phase.

The objective is to provide proper path-based vector design
capabilities suitable for detailed design work and fabrication.

#### Path Editing

- [ ] Implement path objects.
- [ ] Implement freehand drawing.
- [ ] Implement Bézier curves.
- [ ] Implement node editing.
- [ ] Implement node selection.
- [ ] Implement node movement.
- [ ] Implement node insertion.
- [ ] Implement node deletion.
- [ ] Implement path joining.
- [ ] Implement path splitting.
- [ ] Implement path closure.
- [ ] Implement path conversion.
- [ ] Implement path geometry validation.

#### Advanced Editing

- [ ] Implement boolean union operations.
- [ ] Implement boolean subtraction.
- [ ] Implement boolean intersection.
- [ ] Implement boolean exclusion.
- [ ] Implement compound paths.
- [ ] Implement group selection and manipulation.
- [ ] Implement advanced text editing.
- [ ] Implement text-to-path conversion.
- [ ] Implement path simplification where appropriate.
- [ ] Implement reliable handling of open and closed paths.

Vector editing should use a modular architecture that keeps
geometry operations independent of the GUI wherever practical.

Complex geometry operations should include automated tests
covering valid geometry, invalid geometry, and boundary cases.

Vector geometry should remain suitable for accurate physical
measurements and future cutting machine workflows.

---

## 4. File Import and Export

Status: Planned

File import and export are essential capabilities for a practical
vector design and cutting application.

### SVG Support

- [ ] Implement SVG import.
- [ ] Implement SVG export.
- [ ] Preserve physical dimensions.
- [ ] Preserve object positions.
- [ ] Preserve object rotations.
- [ ] Preserve vector geometry.
- [ ] Preserve fill and stroke properties where supported.
- [ ] Preserve layers where supported.
- [ ] Handle unsupported SVG elements appropriately.
- [ ] Test compatibility with external vector applications.
- [ ] Verify compatibility with Brother ScanNCut workflows.

SVG should be a primary interoperability format.

Import and export should preserve physical sizing rather than
silently changing dimensions through pixel-based assumptions.

### PDF Support

- [ ] Implement PDF export.
- [ ] Preserve physical page dimensions.
- [ ] Preserve vector geometry where possible.
- [ ] Verify output in external PDF applications.
- [ ] Investigate PDF import where practical.

### PNG Support

- [ ] Implement PNG export.
- [ ] Support configurable output resolution.
- [ ] Support transparent backgrounds.
- [ ] Preserve intended physical output dimensions where applicable.
- [ ] Provide suitable export options.

### Import and Export Reliability

Future file operations should include:

- Input validation.
- Appropriate error reporting.
- Compatibility testing.
- Physical dimension verification.
- Geometry preservation testing.
- Protection against malformed files.

Import and export functionality should be implemented incrementally,
with SVG support taking priority over additional formats.

---

## 5. Cutting Machine Integration

Status: Planned

The long-term objective is to support multiple cutting machines
through an extensible machine integration architecture.

Machine-specific functionality should remain separate from
general vector document editing.

### Machine Integration Architecture

- [ ] Establish cutter communication architecture.
- [ ] Research supported machine protocols.
- [ ] Identify appropriate communication interfaces.
- [ ] Implement machine configuration profiles.
- [ ] Implement machine selection.
- [ ] Implement machine-specific settings.
- [ ] Implement cutting preview.
- [ ] Implement cut job preparation.
- [ ] Implement supported cutter communication.
- [ ] Implement job status reporting.
- [ ] Implement connection and communication error handling.
- [ ] Implement machine-specific usable cutting areas.
- [ ] Test with physical cutting machines.

### Brother ScanNCut SDX125

The Brother ScanNCut SDX125 is an important target for future
machine compatibility.

Development objectives include:

- [ ] Research the SDX125 file and communication workflows.
- [ ] Implement an SDX125 machine profile.
- [ ] Support standard 12 x 12 inch mat configuration.
- [ ] Support optional 12 x 24 inch mat configuration.
- [ ] Distinguish physical mat dimensions from usable cutting area.
- [ ] Verify machine-specific cutting restrictions against
      manufacturer specifications.
- [ ] Verify SVG compatibility with Brother ScanNCut workflows.
- [ ] Test exported designs using actual machine workflows.
- [ ] Document supported machine capabilities and limitations.

Machine-specific dimensions and restrictions must be based on
verified manufacturer specifications.

The physical cutting mat dimensions must never be treated as
automatically equivalent to the usable cutting area.

### Machine Integration Principles

- Maintain separation between general document editing and
  machine-specific functionality.
- Avoid hard-coding individual machine restrictions into the
  general document model.
- Support multiple machine profiles.
- Preserve document geometry when preparing cutting jobs.
- Validate machine-specific restrictions before sending jobs.
- Provide clear feedback when a design exceeds machine limits.

Physical machine testing will be required before declaring
machine communication functionality complete.

---

## 6. Important Source Files

The following files contain principal application functionality.

This is not a complete filesystem listing.

Always inspect the actual project structure before assuming
that files or modules remain unchanged.

### Main Application

`cutstudio/main.py`

Application entry point.

Launch the application using:

    python -m cutstudio.main

### Main Window

`cutstudio/ui/main_window.py`

Responsible for:

- Main application window.
- Menu bar and toolbar.
- Document creation, opening, and saving.
- Unsaved-change protection.
- Undo and Redo integration.
- Object duplication and deletion.
- Copy, Cut, and Paste.
- Properties panel integration.
- Layer management.
- Cutting mat configuration integration.
- Zoom controls.
- Status bar.
- Ruler integration.
- Grid settings integration.

### Canvas Renderer

`cutstudio/ui/canvas/renderer.py`

Responsible for:

- Rendering document objects.
- Synchronizing graphics items with the document model.
- Maintaining object identifiers.
- Rebuilding canvas contents.
- Updating object geometry.
- Managing graphical representations of document objects.
- Layer visibility and locking integration.

### Cutting Mat

`cutstudio/ui/canvas/cutting_mat.py`

Responsible for:

- Qt graphics view.
- Cutting mat background.
- Grid rendering.
- Canvas mouse interaction.
- Object selection.
- Object movement.
- Object resizing.
- Object rotation.
- Rotation snapping.
- Resize handle detection.
- Geometry synchronization.
- Zooming.
- Zoom to Fit.
- Canvas navigation.
- Zoom percentage notifications.
- Grid snapping integration.

### Grid Settings Dialog

`cutstudio/ui/grid_settings_dialog.py`

Responsible for:

- Grid spacing configuration.
- Inches and millimetres selection.
- Grid spacing presets.
- Major grid interval selection.
- Physical measurement conversion.
- Grid configuration validation.

### Measurement Rulers

`cutstudio/ui/canvas/rulers.py`

Responsible for:

- Horizontal measurement ruler.
- Vertical measurement ruler.
- Inch-based measurements.
- Major and minor ruler divisions.
- Synchronization with canvas scrolling.
- Synchronization with canvas zoom.
- Visible scene-range calculations.

Additional ruler-related files may exist in:

    cutstudio/ui/rulers/

Inspect the actual directory contents before modifying ruler
functionality.

### Cutting Mat Configuration

`cutstudio/core/mat.py`

Responsible for:

- CuttingMatConfig dataclass.
- Physical dimensions stored in millimetres.
- Validation of finite dimensions.
- Validation of positive dimensions.
- Immutable configuration.

### Mat Settings Dialog

`cutstudio/ui/mat_settings_dialog.py`

Responsible for:

- Built-in cutting mat presets.
- Custom cutting mat dimensions.
- Inch-based dimension entry.
- Metric dimension display.
- Cutting mat configuration selection.

### Project Persistence

`cutstudio/core/project_file.py`

Responsible for:

- Native project serialization.
- JSON project files.
- Document reconstruction.
- Project format validation.
- Project version checking.
- Cutting mat configuration persistence.
- Backward compatibility with older project files.

### History

`cutstudio/core/history.py`

Responsible for:

- Undo history.
- Redo history.
- Document snapshots.
- History limits.
- History restoration.
- Redo-branch invalidation.

### Core Document Architecture

The `cutstudio/core/` directory contains document-related
functionality.

Important modules include:

- `document.py`
- `layer.py`
- `objects.py`
- `history.py`
- `project_file.py`
- `constants.py`
- `units.py`
- `mat.py`

Inspect the actual directory before modifying core functionality.

---

## 7. Outstanding Work and Development Priorities

Development should proceed incrementally.

The following items represent outstanding development objectives.
They are not claims of existing functionality.

Priorities should be reviewed against the actual application
implementation before beginning each new milestone.

### 7.1 Canvas and Navigation

Implemented:

- [x] Cutting mat display.
- [x] Configurable cutting mat dimensions.
- [x] Grid rendering.
- [x] Configurable grid spacing.
- [x] Major and minor grid intervals.
- [x] Grid visibility control.
- [x] Grid snapping.
- [x] Group snapping.
- [x] Zoom In and Zoom Out.
- [x] Zoom to Fit.
- [x] Ctrl + mouse wheel zoom.
- [x] Middle-mouse-button panning.
- [x] Horizontal and vertical measurement rulers.
- [x] Permanent zoom percentage display.
- [x] Permanent cutting mat dimension display.

Outstanding:

- [ ] Complete manual grid verification.
- [ ] Verify ruler alignment and measurement accuracy.
- [ ] Verify rotated-object snapping.
- [ ] Verify group snapping under different conditions.
- [ ] Verify resizing with snapping enabled.
- [ ] Investigate geometry-based snapping independent of stroke
      expansion.
- [ ] Implement object-to-object snapping.
- [ ] Implement alignment guides.
- [ ] Improve canvas rendering performance.
- [ ] Improve navigation usability.

### 7.2 Object Editing and Positioning

Implemented:

- [x] Rectangle objects.
- [x] Ellipse objects.
- [x] Text objects.
- [x] Object selection and multi-selection.
- [x] Object movement.
- [x] Eight resize handles.
- [x] Aspect-ratio-constrained resizing.
- [x] Object rotation.
- [x] Rotation snapping.
- [x] Object duplication.
- [x] Object deletion.
- [x] Copy, Cut, and Paste.
- [x] Undo and Redo.
- [x] Snapshot-based document restoration.
- [x] Selection restoration.

Outstanding:

- [ ] Grouping and ungrouping.
- [ ] Align Left.
- [ ] Align Right.
- [ ] Align Top.
- [ ] Align Bottom.
- [ ] Align Horizontal Centre.
- [ ] Align Vertical Centre.
- [ ] Distribute Evenly Horizontally.
- [ ] Distribute Evenly Vertically.
- [ ] Improve multi-object manipulation.
- [ ] Improve selection feedback.
- [ ] Improve text editing.
- [ ] Additional vector object types.

Alignment and distribution operations should work with multiple
selected objects and preserve individual object dimensions
and rotations.

### 7.3 Properties and Layers

Outstanding:

- [ ] Fill colour editing.
- [ ] Stroke colour editing.
- [ ] Stroke width editing.
- [ ] Font selection.
- [ ] Font size editing.
- [ ] Layer creation.
- [ ] Layer deletion.
- [ ] Layer reordering.
- [ ] Improve layer management interface.
- [ ] Improve multi-selection property editing.

Property changes must integrate with document modification
tracking and Undo/Redo.

### 7.4 Document Management

Outstanding:

- [ ] Autosave.
- [ ] Crash recovery.
- [ ] Recent project list.
- [ ] Improve project recovery and error reporting.
- [ ] Consider native project format migration support.
- [ ] Additional project compatibility testing.

Document reliability should remain a priority as the application
becomes capable of handling increasingly complex designs.

### 7.5 Vector Editing

Outstanding:

- [ ] Path objects.
- [ ] Freehand drawing.
- [ ] Bézier curves.
- [ ] Node editing.
- [ ] Node insertion and deletion.
- [ ] Path joining.
- [ ] Path splitting.
- [ ] Path closure.
- [ ] Boolean operations.
- [ ] Compound paths.
- [ ] Text-to-path conversion.
- [ ] Advanced text editing.

### 7.6 File Import and Export

Outstanding:

- [ ] SVG import.
- [ ] SVG export.
- [ ] PDF export.
- [ ] PNG export.
- [ ] Preserve physical dimensions.
- [ ] Preserve object positions and rotations.
- [ ] Preserve vector geometry.
- [ ] Preserve layers where supported.
- [ ] Test external application compatibility.

SVG should receive priority because of its importance to vector
design and cutting machine workflows.

### 7.7 Cutting Machine Integration

Outstanding:

- [ ] Establish cutter communication architecture.
- [ ] Research supported machine protocols.
- [ ] Implement machine configuration profiles.
- [ ] Implement cutting preview.
- [ ] Implement cut job preparation.
- [ ] Implement supported cutter communication.
- [ ] Implement machine-specific usable cutting areas.
- [ ] Implement job status reporting.
- [ ] Implement Brother ScanNCut SDX125 profile.
- [ ] Verify SVG compatibility with Brother ScanNCut workflows.
- [ ] Test with physical cutting machines.

---

## 8. Geometry and Measurement Requirements

Accurate physical measurements are fundamental to CutStudio.

The application must maintain a consistent relationship between
document geometry, scene coordinates, object properties, and
exported vector geometry.

### Coordinate System

The established coordinate system is:

- Object positions are stored in millimetres.
- Object dimensions are stored in millimetres.
- Scene coordinates use 96 units per inch.
- Conversion between millimetres and scene coordinates uses
  the core unit conversion functions.
- The cutting mat origin is at the top-left.
- X increases to the right.
- Y increases downward.

Object X/Y coordinates represent the geometric object origin,
not the visible stroke boundary.

The geometric path determines object dimensions and position.

Stroke thickness is a visual property and must not silently
alter reported object geometry.

### Outstanding Geometry Work

The following discrepancies have been identified:

1. Default rectangle dimensions currently calculate to
   approximately 26.46 × 26.46 mm.
2. Default ellipse dimensions currently calculate to
   approximately 26.46 × 26.46 mm.
3. The intended default dimensions are 25 × 25 mm.
4. Verify that object coordinates consistently represent
   geometric origins.
5. Investigate the small apparent coordinate discrepancy
   of approximately 0.26 mm in X and Y.
6. Review snapping calculations to ensure geometry-based
   bounds are used where appropriate.
7. Investigate the effect of stroke expansion on selection
   bounds and snapping.

### Important Coordinate Conversion Requirement

Do not change the underlying 96-units-per-inch coordinate
conversion simply to correct the identified discrepancies.

The existing conversion model is internally consistent.

Investigate the geometry creation, positioning, and snapping
calculations before modifying fundamental coordinate conversion.

Any changes must be evaluated against:

- Existing document geometry.
- Object properties.
- Canvas rendering.
- Measurement rulers.
- Grid rendering.
- Grid snapping.
- Object rotation.
- Project persistence.
- Future vector export.

### Intended Professional Behaviour

CutStudio should provide:

- Exact physical dimensions.
- Predictable millimetre-based positioning.
- Geometry-based coordinates.
- Independent visual stroke properties.
- Reliable grid snapping.
- Reliable object-to-object snapping.
- Consistent object alignment.
- No unexpected movement when toggling snapping.
- Consistent exported vector geometry.

Geometry accuracy should take precedence over visual approximations
where the two conflict.

---

## 9. Immediate Development Priorities

The next development milestones should improve precision and
editing efficiency without destabilizing existing functionality.

### Initial Verification

Before implementing additional canvas functionality:

1. Inspect the current Git working tree.
2. Verify the existing grid implementation.
3. Verify grid visibility at different zoom levels.
4. Verify major and minor grid intervals.
5. Verify inch and millimetre spacing.
6. Test individual object snapping.
7. Test multi-object group snapping.
8. Test snapping with rotated objects.
9. Test resizing with snapping enabled.
10. Investigate geometry-based snapping versus stroke-expanded
    bounds.
11. Investigate the identified default object dimension
    discrepancies.

### Next Editing Milestone

Following verification of the existing canvas functionality,
the next major editing objective is object alignment and
positioning.

Proposed functionality:

- Align Left.
- Align Right.
- Align Top.
- Align Bottom.
- Align Horizontal Centre.
- Align Vertical Centre.
- Distribute Evenly Horizontally.
- Distribute Evenly Vertically.

Before implementation:

- Inspect the current document object model.
- Inspect the canvas renderer.
- Review selection handling.
- Review object geometry calculations.
- Review Undo/Redo integration.
- Determine how rotated objects should be handled.
- Define predictable alignment behaviour.
- Add automated regression tests.

Alignment operations should preserve object dimensions,
rotations, identifiers, and layer assignments.

All operations must integrate with Undo and Redo.

### Subsequent Editing Milestones

Following object alignment and distribution:

1. Implement grouping and ungrouping.
2. Improve multi-object manipulation.
3. Improve layer management.
4. Expand object property editing.
5. Investigate object-to-object snapping and alignment guides.
6. Continue development toward path-based vector editing.

Do not begin a new milestone simply because a feature appears
on the roadmap.

First establish whether the functionality already exists,
whether it requires improvement, and whether its dependencies
have been satisfied.

### Development Verification

Every significant milestone should include:

- Source inspection.
- Appropriate automated regression tests.
- Full automated test suite execution.
- Manual GUI verification where appropriate.
- Review of Git changes.
- Documentation updates following verification.

---

## 10. Git and Repository Management

The project is maintained in Git.

The primary development branch is:

    main

Always inspect the actual working tree before modifying files.

### Useful Commands

Navigate to the project directory:

    cd ~/Code/CutStudio

Activate the development environment:

    source .venv/bin/activate

Check Git status:

    git status --short

Inspect recent commits:

    git log -5 --oneline

Inspect differences:

    git diff

Inspect the change summary:

    git diff --stat

Check whitespace errors:

    git diff --check

Run the complete automated test suite:

    python -m pytest -q

### Repository Management Requirements

- Never discard existing user modifications without permission.
- Never overwrite existing uncommitted work.
- Inspect unexpected untracked files before removing them.
- Preserve useful backup files until their purpose is established.
- Do not automatically stage unrelated files.
- Review changes before committing.
- Keep commits focused on related functionality.
- Run appropriate tests before committing significant changes.
- Update documentation when functionality changes.
- Do not commit changes until the user has reviewed and approved them.

### Backup Files

Backup files may contain earlier implementations or useful
development history.

Do not assume that an untracked backup file is unnecessary.

Before removing or replacing a backup:

1. Inspect its contents.
2. Compare it with the current source file.
3. Determine whether it contains unique functionality.
4. Obtain approval before deleting it.

Backup files should not be included in commits automatically.

### Latest Recorded Repository State

Latest recorded commit:

    0278bb6 Strengthen project persistence validation

Recent development commits include:

    13938cb Improve undo redo history and selection restoration
    82802d8 Fix undo redo layer state and selection restoration
    724ceac Update handoff and regression tests
    47a2456 Add grid and snapping regression tests

Latest recorded branch relationship:

    main == origin/main

Latest verified automated test result:

    152 passed

Verification date:

    November 24, 2026

The working tree contained the following untracked backup files
at the latest inspection:

    cutstudio/core/project_file.py.bak
    cutstudio/ui/main_window.py.before_selection_fix

These files must be preserved unless their removal is explicitly
approved after inspection.

Repository state must always be checked again before making
development decisions.

---

## 11. Documentation Requirements

Maintain consistency between:

- `HANDOFF.md`
- `ROADMAP.md`
- `ARCHITECTURE.md`

Each document serves a different purpose.

### HANDOFF.md

The development handoff records the current implementation state.

It should describe:

- Implemented functionality.
- Confirmed working behaviour.
- Automated test results.
- Manual verification results.
- Important implementation details.
- Current Git state.
- Outstanding development tasks.
- Immediate development recommendations.

HANDOFF.md should be the primary reference for understanding
the latest development progress.

### ROADMAP.md

The development roadmap records the intended product direction.

It should describe:

- Project vision.
- Development phases.
- Feature implementation status.
- Outstanding functionality.
- Long-term objectives.
- Development priorities.
- Future machine integration.

ROADMAP.md should not become a duplicate of HANDOFF.md.

Avoid unnecessary implementation details that belong in the
development handoff or architecture documentation.

### ARCHITECTURE.md

The architecture document records the technical design of
the application.

It should describe:

- Application architecture.
- Module responsibilities.
- Document model.
- Object model.
- Layer model.
- Canvas architecture.
- Coordinate system.
- Measurement conversions.
- Rendering architecture.
- Project persistence.
- Undo and Redo architecture.
- Important architectural decisions.

Architecture documentation should reflect actual source code,
not proposed or hypothetical implementations.

### Markdown Source Requirements

All project documentation must be maintained as genuine
raw Markdown.

Requirements:

- Use `#` for document titles.
- Use `##` for major sections.
- Use `###` for subsections.
- Use standard Markdown bullet lists.
- Use standard Markdown numbered lists.
- Use fenced code blocks for commands and source examples.
- Use Markdown checkboxes for implementation status.
- Preserve technical details.
- Avoid unnecessary HTML formatting.
- Keep documents directly editable in plain-text editors.

When providing long Markdown documents through ChatGPT:

- Divide the complete document into four consecutive chunks.
- Place each chunk in its own fenced Markdown code block.
- Preserve the original document order.
- Do not omit sections.
- Do not duplicate sections.
- Ensure that the four chunks can be concatenated into one
  complete Markdown document.
- Avoid interrupting important technical details at chunk
  boundaries.

### Document Revision Requirements

When revising documentation:

1. Inspect the existing document.
2. Preserve relevant existing information.
3. Verify implementation claims against current source code.
4. Update obsolete descriptions.
5. Keep implemented functionality separate from planned
   functionality.
6. Update automated test counts only after running the tests.
7. Record verification dates accurately.
8. Maintain consistency across project documentation.
9. Avoid duplicating information unnecessarily.
10. Preserve important historical implementation decisions.

Do not claim functionality is implemented merely because it
appears in a roadmap or previous development discussion.

---

## 12. Development Policy

CutStudio should be developed incrementally.

The primary development priorities are:

1. Maintain application stability.
2. Preserve existing functionality.
3. Improve canvas usability.
4. Improve object editing capabilities.
5. Maintain accurate physical measurements.
6. Expand automated test coverage.
7. Improve document reliability.
8. Develop professional vector editing capabilities.
9. Implement reliable file import and export.
10. Prepare for future cutting machine integration.

### Mandatory Development Practices

- Always inspect current source code before making
  implementation decisions.
- Always inspect Git status before modifying files.
- Preserve existing uncommitted work.
- Do not overwrite user changes.
- Do not remove backup files without inspection and permission.
- Prefer small, controlled modifications.
- Avoid unnecessary architectural changes.
- Preserve established functionality.
- Add automated tests for significant functionality.
- Run the complete automated test suite after significant
  changes.
- Perform manual GUI verification where appropriate.
- Verify changes before declaring functionality complete.
- Update documentation after verified changes.
- Do not mark planned features as implemented prematurely.

### Testing Policy

Automated testing is essential to maintaining application
stability.

The complete test suite should be run after significant changes.

Use:

    python -m pytest -q

Run individual test modules when investigating specific
regressions.

Automated tests do not replace manual GUI verification.

Features involving the following require appropriate manual
testing:

- Mouse interaction.
- Keyboard shortcuts.
- Object selection.
- Object movement.
- Resizing.
- Rotation.
- Canvas rendering.
- Zooming.
- Panning.
- Grid visibility.
- Grid snapping.
- Physical measurements.
- Ruler alignment.
- Project saving and loading.
- Dialog behaviour.

Testing should cover the primary Linux Mint development
environment.

Wayland compatibility should also be considered during GUI
development and testing.

Windows and macOS compatibility should be verified as the
application progresses toward cross-platform releases.

### Physical Measurement Policy

The established physical measurement model must be preserved.

Important requirements:

- Store physical document measurements in millimetres.
- Maintain the existing 96-units-per-inch scene coordinate
  system.
- Keep physical cutting mat dimensions independent of
  document dimensions.
- Keep machine-specific usable cutting areas separate.
- Ensure object geometry remains independent of visual
  stroke expansion.
- Preserve physical dimensions during file import and export.
- Avoid unexpected coordinate changes during editing.

Do not change fundamental coordinate conversion functions
without investigating their impact on the entire application.

### Architectural Policy

- Maintain separation between document objects and graphical
  representations.
- Keep core geometry functionality independent of the GUI
  wherever practical.
- Avoid placing machine-specific restrictions in the general
  document model.
- Preserve backward compatibility when changing project files.
- Keep Undo and Redo integrated with document operations.
- Use automated tests to protect important architectural
  behaviour.

### Documentation Policy

Documentation must remain synchronized with the actual
implementation.

Update HANDOFF.md following significant development milestones.

Update ROADMAP.md when development priorities or implementation
status change.

Update ARCHITECTURE.md when architectural decisions or
implementation structures change.

Preserve relevant technical information when revising documents.

Do not maintain competing development handoffs as separate
sources of truth.

---

## 13. Current Development State

CutStudio is a functioning early-stage vector design and
vinyl cutting application.

The project has progressed substantially beyond its original
prototype.

The current implementation provides a foundation for more
advanced vector editing and future cutting machine integration.

### Completed Development Areas

- Modular document architecture.
- Qt graphics-based canvas.
- Rectangle, ellipse, and text objects.
- Object selection and multi-selection.
- Object movement, resizing, and rotation.
- Eight resize handles.
- Shift-constrained aspect-ratio resizing.
- Rotation snapping in 15-degree increments.
- Object duplication and deletion.
- Copy, Cut, and Paste.
- Snapshot-based Undo and Redo.
- Layer visibility and locking.
- Selection restoration following document restoration.
- Editable object position and dimension properties.
- Native project saving and loading.
- Project file validation.
- Cutting mat configuration and persistence.
- Zoom controls and Zoom to Fit.
- Horizontal and vertical measurement rulers.
- Canvas panning.
- Physical measurement support using millimetres.
- Permanent zoom percentage display.
- Permanent cutting mat dimension display.
- Configurable grid spacing.
- Grid spacing presets in inches and millimetres.
- Configurable major grid line intervals.
- Independent grid visibility control.
- Grid snapping.
- Grid-aligned resizing.
- Multi-object group snapping.
- Project persistence validation and regression tests.

### Current Grid Configuration

Default settings:

- Grid spacing: 6.35 mm (1/4 inch).
- Major interval: 4 minor grid intervals.
- Major grid spacing: 25.4 mm (1 inch).
- Grid visible: enabled.
- Snap to Grid: disabled.

Grid display and snapping use the same underlying physical
measurement configuration.

Further manual verification remains necessary for rotated
objects, multi-object selections, and resizing with snapping.

### Automated Testing

Latest verified automated test result:

    152 passed

Verification date:

    November 24, 2026

Command:

    python -m pytest -q

### Latest Recorded Git Commit

Commit:

    0278bb6

Message:

    Strengthen project persistence validation

Branch:

    main

Remote:

    origin/main

The latest recorded local and remote branch positions are
identical.

The working tree contains two untracked backup files that
must be preserved.

### Immediate Development Direction

The next development objective is to continue strengthening
canvas accuracy and object editing.

The recommended sequence is:

1. Complete manual verification of configurable grid behaviour.
2. Investigate geometry-based snapping and stroke expansion.
3. Investigate the outstanding default object dimension
   discrepancies.
4. Develop object alignment and positioning tools.
5. Implement object distribution.
6. Improve multi-object editing.
7. Develop grouping and ungrouping.
8. Continue expanding vector editing capabilities.

All development should preserve the existing document
architecture, physical measurement model, and established
application functionality.

Always inspect the actual source code and Git working tree
before making development decisions.

The long-term objective remains to develop CutStudio into
a reliable, cross-platform vector design and vinyl cutting
application with accurate geometry, professional editing
capabilities, common vector file formats, and extensible
cutting machine support.

# CutStudio Development Handoff

Last updated: November 17, 2026

## 1. Project Overview

CutStudio is a cross-platform desktop vector design application built with Python and PySide6.

The project aims to provide an accessible vector design and vinyl cutting environment, particularly for Linux users and Brother ScanNCut workflows.

Development is ongoing.

## 2. Current Development Status

CutStudio has progressed beyond its initial prototype.

Implemented functionality includes:

- Modular core document architecture.
- Qt graphics-based canvas.
- Document and layer management.
- Rectangle, ellipse, and text objects.
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

## 3. Latest Development: Measurement Rulers

Horizontal and vertical measurement rulers have been implemented.

### Functionality

- Horizontal ruler.
- Vertical ruler.
- Rulers positioned alongside the canvas viewport.
- Ruler markings synchronized with canvas scrolling.
- Ruler markings synchronized with canvas zoom.
- Inch-based measurements.
- Quarter-inch subdivisions.

### Implementation

New source files:

- cutstudio/ui/canvas/rulers.py
- cutstudio/ui/rulers/

Modified files:

- cutstudio/ui/canvas/cutting_mat.py
- cutstudio/ui/main_window.py

New tests:

- tests/test_cutting_mat.py

### Verification

The complete automated test suite reports:

99 passed

Manual GUI verification remains important, particularly:

- Ruler alignment.
- Horizontal scrolling.
- Vertical scrolling.
- Zoom synchronization.
- Measurement accuracy.
- Display behaviour at different zoom levels.

## 4. Configurable Cutting Mat

Physical cutting mat configuration has been implemented.

### Built-in presets

- 12 × 12 inches.
- 12 × 24 inches.
- 12 × 36 inches.
- 12 × 48 inches.

Custom dimensions are also supported.

### User interface

Mat settings are accessible through:

Machine → Mat Settings

Implementation:

- cutstudio/core/mat.py
- cutstudio/ui/mat_settings_dialog.py

### Project persistence

Implementation:

- cutstudio/core/project_file.py

Mat configuration is saved with native CutStudio projects.

When loading projects:

- Existing mat configuration is restored.
- Older projects without mat configuration receive the default configuration.
- Invalid mat configuration is rejected.
- Document dimensions remain independent of mat dimensions.

### Important distinction

Three concepts must remain separate:

1. Physical cutting mat dimensions.
2. Document dimensions.
3. Usable cutting area.

Machine-specific usable cutting-area restrictions have not yet been implemented.

## 5. Automated Testing

Latest verified test result:

99 passed in 0.35s

Command:

python -m pytest -q

The test suite includes coverage for:

- Document creation and management.
- Object creation and validation.
- Object manipulation.
- Undo and Redo.
- Copy, Cut, and Paste.
- Layer management.
- Project saving and loading.
- Cutting mat configuration.
- Mat configuration validation.
- Legacy project compatibility.
- Document and mat dimension independence.
- Canvas interaction.
- Rendering.
- Main window integration.

Six dedicated tests cover Undo and Redo history.

Always run the complete test suite before committing significant changes.

## 6. Current Git State

At the latest recorded inspection, the following files were modified:

- ARCHITECTURE.md
- HANDOFF.md
- README.md
- ROADMAP.md
- cutstudio/ui/canvas/cutting_mat.py
- cutstudio/ui/main_window.py
- cutstudio/ui/mat_settings_dialog.py

New files:

- cutstudio/ui/canvas/rulers.py
- cutstudio/ui/rulers/
- tests/test_cutting_mat.py

Backup files were also present:

- ARCHITECTURE.md.bak
- HANDOFF.md.bak
- README.md.bak
- ROADMAP.md.bak

IMPORTANT:

The documentation modifications were subsequently targeted for restoration to their committed versions.

Do not assume the Git status above still represents the current working tree.

Check the actual state using:

git status --short

Do not discard application source changes when restoring documentation.

## 7. Remaining Development Priorities

### Canvas and Navigation

- Complete manual verification of horizontal and vertical rulers.
- Verify ruler synchronization during zooming.
- Verify ruler synchronization during panning.
- Implement configurable grid spacing.
- Implement grid snapping.
- Implement object snapping.
- Implement alignment guides.
- Improve canvas rendering performance.

### Object Editing

- Implement grouping and ungrouping.
- Implement object alignment.
- Implement object distribution.
- Improve multi-object manipulation.

### Properties and Layers

- Implement fill color editing.
- Implement stroke color editing.
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
- Implement text editing.
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

## 8. Immediate Next Steps

Recommended development sequence:

1. Verify the current Git working tree.
2. Confirm the 99-test baseline.
3. Launch CutStudio.
4. Manually verify horizontal and vertical rulers.
5. Verify ruler behaviour during zooming and panning.
6. Verify cutting mat presets.
7. Verify custom cutting mat dimensions.
8. Verify saving and reopening projects.
9. Verify older project compatibility.
10. Continue with configurable grid spacing.

## 9. Development Environment

The project uses:

- Python.
- PySide6.
- pytest.
- Git.

Activate the virtual environment before running commands:

source .venv/bin/activate

Run the application using the existing project entry point.

Run automated tests:

python -m pytest -q

Check whitespace errors:

git diff --check

Inspect working tree:

git status --short

## 10. Development Policy

- Preserve existing functionality.
- Avoid unnecessary architectural changes.
- Do not rewrite established documentation when updating development status.
- Update the handoff document when significant features are completed.
- Keep historical test results where they describe earlier development stages.
- Only report functionality as complete when verified.
- Include automated tests for significant functionality.
- Supplement automated testing with manual GUI verification.
- Keep physical mat dimensions separate from document dimensions and usable cutting areas.

The immediate objective is to continue improving the canvas and editing experience while maintaining the existing 99-test passing baseline.


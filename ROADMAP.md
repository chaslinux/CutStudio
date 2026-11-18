# CutStudio Development Roadmap

## 1. Project Vision

CutStudio is a cross-platform desktop vector design application built
with Python and PySide6.

The goal is to create an accessible, reliable design environment for
vinyl cutting, plotter workflows, and other vector-based fabrication
projects.

The application should eventually support:

- Linux.
- Windows.
- macOS.
- Multiple cutting machines.
- Common vector file formats.
- Accurate physical measurements.
- Professional vector editing workflows.

### Core Principles

- Cross-platform compatibility.
- Reproducible installation.
- Modular architecture.
- Accurate physical measurements.
- Non-destructive editing wherever practical.
- Open vector file formats.
- Extensible machine support.
- Reliable document handling.

---

## 2. Current Development Status

CutStudio has progressed substantially beyond its initial prototype.

The application currently includes:

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
- Permanent zoom percentage display.
- Permanent cutting mat dimension display.
- Unsaved-change protection.

### Automated Testing

Latest recorded automated test result:

104 tests passing.

Verification date:

November 17, 2026.

The test suite provides automated coverage of core functionality,
document management, editing operations, and application behaviour.

The existing 104-test result is the current recorded baseline.

Further testing should be performed whenever significant changes
are introduced.

### Manual Verification

Ruler and status bar fixes have been manually verified.

Further manual GUI verification remains appropriate for:

- Ruler alignment.
- Measurement accuracy.
- Zoom behaviour.
- Canvas panning.
- Object resizing at different zoom levels.
- Rotation behaviour.
- Cutting mat configuration.
- Project persistence.

Automated test success does not replace manual verification of
interactive GUI behaviour.

---

## 3. Development Phases

### Phase 1: Foundation and Architecture

Status: Substantially Complete

- [x] Establish Python virtual environment.
- [x] Install PySide6.
- [x] Create application entry point.
- [x] Implement main application window.
- [x] Implement menu bar.
- [x] Implement main toolbar.
- [x] Implement drawing tools panel.
- [x] Implement properties and layers panel.
- [x] Establish core document architecture.
- [x] Implement document model.
- [x] Implement layer model.
- [x] Implement vector object model.
- [x] Implement physical measurement conversions.
- [x] Implement initial cutting mat.
- [x] Implement grid.
- [x] Establish automated tests.
- [ ] Establish reproducible cross-platform Qt configuration.
- [ ] Document complete installation requirements.
- [ ] Implement automated application startup tests.

### Phase 2: Canvas and Navigation

Status: Substantially Complete

- [x] Implement cutting mat display.
- [x] Implement grid display.
- [x] Implement Ctrl + mouse wheel zoom.
- [x] Display current zoom percentage in the status bar.
- [x] Implement canvas selection.
- [x] Implement rubber-band selection.
- [x] Implement dedicated Zoom In and Zoom Out controls.
- [x] Implement Zoom to Fit.
- [x] Implement middle-mouse canvas panning.
- [x] Add configurable cutting mat dimensions.
- [x] Add built-in cutting mat presets.
- [x] Add custom cutting mat dimensions.
- [x] Persist cutting mat configuration in project files.
- [x] Implement horizontal measurement ruler.
- [x] Implement vertical measurement ruler.
- [x] Synchronize rulers with canvas scrolling.
- [x] Synchronize rulers with canvas zoom.
- [ ] Add configurable grid spacing.
- [ ] Implement grid snapping.
- [ ] Implement object snapping.
- [ ] Implement alignment guides.
- [ ] Improve canvas rendering performance.

#### Canvas Navigation

Current navigation functionality:

- Middle mouse button + drag pans the canvas.
- Panning uses Qt scrollbars.
- Ctrl + mouse wheel zooms in and out.
- Zoom to Fit restores the complete cutting mat to view.
- Dedicated toolbar buttons provide Zoom In and Zoom Out.
- Standard Qt keyboard shortcuts provide Zoom In and Zoom Out.
- Interactive zoom is limited to 10% minimum and 500% maximum.
- The status bar reports the current zoom percentage.
- Horizontal and vertical rulers display physical measurements.
- Rulers update when the canvas scrolls or zoom changes.

Further manual verification should cover different window sizes,
zoom levels, and cutting mat dimensions.

### Phase 3: Object Editing

Status: In Progress

- [x] Implement rectangle objects.
- [x] Implement ellipse objects.
- [x] Implement text objects.
- [x] Implement object selection.
- [x] Implement multi-selection.
- [x] Implement object movement.
- [x] Implement eight resize handles.
- [x] Implement object rotation.
- [x] Implement rotation handle.
- [x] Implement rotation handle connector.
- [x] Improve rotation handle hit detection.
- [x] Eliminate rotation handle positioning jitter.
- [x] Implement rotation snapping with Shift.
- [x] Implement object duplication.
- [x] Implement Ctrl+D duplication shortcut.
- [x] Implement object deletion.
- [x] Implement object identifiers.
- [x] Implement object validation.
- [x] Implement Shift + resize aspect-ratio locking.
- [x] Implement Copy.
- [x] Implement Cut.
- [x] Implement Paste.
- [x] Implement Undo and Redo.
- [ ] Implement grouping and ungrouping.
- [ ] Implement object alignment.
- [ ] Implement object distribution.
- [ ] Improve multi-object manipulation.

Further development should prioritize reliable multi-object editing
and consistent geometry handling across different zoom levels.

### Phase 4: Properties and Layers

Status: Partially Complete

#### Implemented

- [x] Display selected object type.
- [x] Implement X position editing.
- [x] Implement Y position editing.
- [x] Implement width editing.
- [x] Implement height editing.
- [x] Implement rotation editing.
- [x] Synchronize properties with canvas geometry.
- [x] Implement layer selection.
- [x] Implement layer visibility.
- [x] Implement layer locking.
- [x] Prevent editing objects on locked layers.
- [x] Refresh properties following document restoration.

#### Outstanding

- [ ] Implement fill color editing.
- [ ] Implement stroke color editing.
- [ ] Implement stroke width editing.
- [ ] Implement font selection.
- [ ] Implement font size editing.
- [ ] Implement layer creation.
- [ ] Implement layer deletion.
- [ ] Implement layer reordering.
- [ ] Improve layer management interface.
- [ ] Improve multi-selection property editing.

Future property editing should maintain synchronization between
the document model, canvas representation, and undo history.

### Phase 5: Document Management

Status: Substantially Complete

#### Implemented

- [x] Implement document creation.
- [x] Implement document dimensions.
- [x] Implement document layers.
- [x] Implement native CutStudio project format.
- [x] Implement project saving.
- [x] Implement project loading.
- [x] Implement project validation.
- [x] Implement project version checking.
- [x] Implement modified-document tracking.
- [x] Implement unsaved-change detection.
- [x] Implement save confirmation.
- [x] Implement discard confirmation.
- [x] Verify and correct Cancel behavior for unsaved changes.
- [x] Implement application-close confirmation.
- [x] Verify Save, Discard, and Cancel when closing the application.
- [x] Implement Undo and Redo history.
- [x] Implement cutting mat configuration persistence.
- [x] Maintain separation between document dimensions and physical
      cutting mat dimensions.

#### Outstanding

- [ ] Implement autosave.
- [ ] Implement crash recovery.
- [ ] Implement recent project list.
- [ ] Improve project recovery and error reporting.
- [ ] Consider native project format migration support.

#### Project Persistence

The native project format currently stores:

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

The cutting mat configuration is independent of the document
dimensions and is persisted separately in the project data.

Older project files without cutting mat configuration use the
default 12 x 12 inch cutting mat dimensions.

Any changes to the project format should include appropriate
backward-compatibility tests.

### Phase 6: Vector Editing

Status: Planned

#### Path Editing

- [ ] Implement path objects.
- [ ] Implement freehand drawing.
- [ ] Implement Bézier curves.
- [ ] Implement node editing.
- [ ] Implement path joining.
- [ ] Implement path splitting.
- [ ] Implement node deletion.
- [ ] Implement node insertion.
- [ ] Implement path closure.
- [ ] Implement path conversion.

#### Advanced Editing

- [ ] Implement boolean union operations.
- [ ] Implement boolean subtraction.
- [ ] Implement boolean intersection.
- [ ] Implement boolean exclusion.
- [ ] Implement grouping and compound paths.
- [ ] Implement group selection and manipulation.
- [ ] Implement text editing.
- [ ] Implement font selection.
- [ ] Implement text-to-path conversion.

Vector editing should use a modular architecture that keeps
geometry operations independent of the GUI wherever practical.

Complex geometry operations should include automated tests
covering valid and invalid geometry.

## 9. Important Source Files

The following files contain the principal application functionality.

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
- Zoom controls and status bar.

### Canvas Renderer

`cutstudio/ui/canvas/renderer.py`

Responsible for:

- Rendering document objects.
- Synchronizing graphics items with the document model.
- Maintaining object identifiers.
- Rebuilding canvas contents.
- Updating object geometry.
- Managing selection and object positioning.

### Cutting Mat

`cutstudio/ui/canvas/cutting_mat.py`

Responsible for:

- Qt graphics view.
- Cutting mat background.
- Grid rendering.
- Canvas zooming.
- Zoom to Fit.
- Middle-mouse-button panning.
- Mouse-driven object resizing.
- Mouse-driven object rotation.
- Measurement ruler integration.
- Zoom percentage notifications.

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

The rulers are integrated directly into the cutting mat graphics view.

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
- Backward compatibility with projects without saved mat settings.

### History

`cutstudio/core/history.py`

Responsible for:

- Undo history.
- Redo history.
- Document snapshots.
- History restoration.

### Core

The `cutstudio/core/` directory contains the document model and supporting functionality.

Important modules include:

- `document.py`
- `layer.py`
- `objects.py`
- `history.py`
- `project_file.py`
- `constants.py`
- `units.py`
- `mat.py`

---

## 10. Outstanding Work and Development Priorities

Development should proceed incrementally.

Always inspect the current source code before assuming a feature is implemented or a proposed change is still necessary.

### Canvas and Navigation

Current functionality includes:

- Cutting mat display.
- Configurable mat dimensions.
- Grid rendering.
- Zoom in and Zoom out.
- Zoom to Fit.
- Ctrl + mouse wheel zoom.
- Middle-mouse-button panning.
- Horizontal measurement ruler.
- Vertical measurement ruler.
- Permanent zoom percentage display.
- Permanent cutting mat dimension display.

Outstanding work:

- [ ] Configurable grid spacing.
- [ ] Grid snapping.
- [ ] Object snapping.
- [ ] Alignment guides.
- [ ] Improve canvas rendering performance.
- [ ] Further verify ruler alignment at different zoom levels.
- [ ] Verify ruler measurements against physical dimensions.
- [ ] Improve navigation usability.

### Object Editing

Implemented:

- [x] Rectangle objects.
- [x] Ellipse objects.
- [x] Text objects.
- [x] Object selection.
- [x] Multi-selection.
- [x] Object movement.
- [x] Eight resize handles.
- [x] Aspect-ratio-constrained resizing.
- [x] Object rotation.
- [x] Rotation snapping.
- [x] Object duplication.
- [x] Object deletion.
- [x] Copy.
- [x] Cut.
- [x] Paste.
- [x] Undo and Redo.

Outstanding work:

- [ ] Grouping and ungrouping.
- [ ] Object alignment.
- [ ] Object distribution.
- [ ] Improve multi-object manipulation.
- [ ] Improve text editing.
- [ ] Additional vector object types.

### Properties and Layers

Outstanding work:

- [ ] Fill colour editing.
- [ ] Stroke colour editing.
- [ ] Stroke width editing.
- [ ] Font selection.
- [ ] Font size editing.
- [ ] Layer creation.
- [ ] Layer deletion.
- [ ] Layer reordering.
- [ ] Improve layer management interface.

### Document Management

Outstanding work:

- [ ] Autosave.
- [ ] Crash recovery.
- [ ] Recent project list.
- [ ] Additional project persistence tests.
- [ ] Improve document management workflow.

### Vector Editing

Planned:

- [ ] Path objects.
- [ ] Freehand drawing.
- [ ] Bézier curves.
- [ ] Node editing.
- [ ] Path joining.
- [ ] Path splitting.
- [ ] Boolean operations.
- [ ] Text-to-path conversion.
- [ ] Compound paths.

### File Import and Export

Planned:

- [ ] SVG import.
- [ ] SVG export.
- [ ] PDF export.
- [ ] PNG export.
- [ ] Preserve physical dimensions.
- [ ] Preserve object positions and rotations.
- [ ] Preserve layers where supported.
- [ ] Test external application compatibility.

### Cutting Machine Integration

Long-term objectives:

- [ ] Establish cutter communication architecture.
- [ ] Research supported cutting machine protocols.
- [ ] Implement machine configuration profiles.
- [ ] Implement cutting preview.
- [ ] Implement cut job preparation.
- [ ] Implement supported cutter communication.
- [ ] Add machine-specific settings.
- [ ] Implement job status reporting.
- [ ] Test with physical cutting machines.

Brother ScanNCut SDX125 considerations:

- [ ] Implement an SDX125 machine profile.
- [ ] Support standard 12 x 12 inch mat configuration.
- [ ] Support optional 12 x 24 inch mat configuration.
- [ ] Distinguish physical mat dimensions from usable cutting area.
- [ ] Validate cutting-area restrictions against Brother specifications.
- [ ] Verify SVG compatibility with Brother ScanNCut workflows.

---

## 11. Immediate Next Steps

The immediate objective is to continue improving the canvas and editing experience without destabilizing existing functionality.

Recommended sequence:

1. Inspect the current Git working tree.
2. Inspect the existing canvas implementation.
3. Verify ruler alignment and measurements.
4. Verify zooming and panning at different zoom levels.
5. Investigate grid spacing configuration.
6. Consider grid snapping as a separate feature.
7. Add automated tests for any new core functionality.
8. Run the complete automated test suite.
9. Update HANDOFF.md and ROADMAP.md after verified changes.

Do not begin implementing a feature simply because it appears on the roadmap.

First establish whether the functionality already exists and whether it requires improvement.

---

## 12. Git and Repository Management

The project is maintained in Git.

Always inspect the working tree before modifying files.

Useful commands:

    git status --short

    git diff --stat

    git diff

    git log -5 --oneline

Run the complete test suite before committing significant changes:

    python -m pytest -q

### Important Git Instructions

- Never discard existing user modifications without permission.
- Never overwrite existing uncommitted work.
- Inspect unexpected untracked files before removing them.
- Preserve useful backup files until their purpose is established.
- Do not automatically stage unrelated files.
- Review changes before committing.
- Keep commits focused on related functionality.
- Update documentation when functionality changes.

The current working tree previously contained:

    M HANDOFF.md
    ?? cutstudio/ui/main_window.py.pre-scroll-pan

The backup file must be inspected before any decision to remove it.

Its differences from the current main window include earlier implementations of:

- Cutting mat configuration.
- Project persistence integration.
- Copy, Cut, and Paste.
- Zoom controls.
- Status bar improvements.
- Selection restoration.
- Application-close protection.

Do not assume this backup is unnecessary without checking whether it contains any unique work.

## 13. Documentation Requirements

Maintain consistency between:

- `HANDOFF.md`
- `ROADMAP.md`
- `ARCHITECTURE.md`

Documentation must reflect the actual implementation.

### Markdown Source Requirements

All Markdown documentation must be maintained as genuine raw Markdown.

Requirements:

- Use `#` for document titles.
- Use `##` for major sections.
- Use `###` for subsections.
- Use standard Markdown bullet lists.
- Use standard Markdown numbered lists.
- Use fenced code blocks for commands and source examples.
- Use Markdown checkboxes for implementation status.
- Preserve existing document structure where practical.
- Do not replace Markdown source with visually formatted text.
- Do not introduce HTML formatting unnecessarily.
- Do not omit existing documentation when revising a document.
- Preserve technical details and implementation history.

When providing long Markdown documents through ChatGPT, divide the complete document into four consecutive chunks.

Each chunk must contain raw Markdown source in its own fenced code block.

Do not render the document as formatted Markdown outside those code blocks.

Ensure that:

- Chunks follow the original document order.
- No sections are omitted.
- No sections are duplicated.
- Headings retain their original Markdown syntax.
- The four chunks can be concatenated to reconstruct the complete document.
- Chunk boundaries do not interrupt important technical details unnecessarily.

### Document Revision Requirements

When revising documentation:

1. Inspect the existing document.
2. Preserve relevant existing information.
3. Verify implementation claims against current source code.
4. Update obsolete descriptions.
5. Keep implemented functionality separate from planned functionality.
6. Update automated test counts only after running the tests.
7. Record verification dates accurately.
8. Maintain consistency across project documentation.

Do not claim functionality is implemented merely because it appears in a roadmap or previous handoff.

### Development Communication Requirements

Development instructions should be incremental and specific.

When proposing code changes:

- Identify the relevant source file.
- Inspect the current implementation first.
- Explain the intended change.
- Avoid unnecessary architectural changes.
- Preserve existing functionality.
- Provide complete code where practical.
- Include relevant test instructions.
- Verify results before declaring completion.

Do not assume that previously discussed code changes were successfully applied.

---

## 14. Development Policy

CutStudio should be developed incrementally.

The primary development priorities are:

1. Maintain application stability.
2. Preserve existing functionality.
3. Improve canvas usability.
4. Improve editing capabilities.
5. Maintain accurate physical measurements.
6. Expand automated test coverage.
7. Improve document reliability.
8. Prepare for future machine integration.

### Mandatory Development Practices

- Always inspect current source code before making implementation decisions.
- Always inspect Git status before modifying files.
- Preserve existing uncommitted work.
- Do not overwrite user changes.
- Do not remove backup files without inspection and permission.
- Run the complete automated test suite after significant changes.
- Perform manual GUI verification when appropriate.
- Update documentation after verified changes.
- Do not mark planned features as implemented prematurely.

### Testing Policy

Automated tests are essential but do not replace manual GUI verification.

Features involving mouse interaction, keyboard shortcuts, rendering, zooming, and physical measurements should receive appropriate manual testing.

The existing automated test baseline must be maintained unless a test is deliberately changed for a documented reason.

### Documentation Policy

Documentation must remain genuine Markdown source.

When supplying long documents, use four consecutive raw Markdown chunks rather than rendered Markdown or visually formatted text.

Preserve all relevant technical information when updating project documentation.

---

## 15. Current Development State

CutStudio is a functioning early-stage vector design application.

The application has progressed substantially beyond its original prototype.

Implemented functionality includes:

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

Latest recorded automated test result:

    104 passed

Verification date:

    November 17, 2026

Ruler and status bar fixes have been manually verified.

Further manual GUI verification remains appropriate for ruler alignment, measurement accuracy, zooming, and panning.

The immediate objective is to continue improving the canvas and editing experience while maintaining the existing automated test baseline.

Always inspect the current source code and Git working tree before making development decisions.

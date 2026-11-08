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

CutStudio has progressed beyond its initial prototype.

The application currently has:

- A modular core document architecture.
- A Qt graphics-based canvas.
- Document and layer management.
- Rectangle, ellipse, and text objects.
- Object selection and manipulation.
- Object properties.
- Object duplication and deletion.
- Layer visibility and locking.
- Native project saving and loading.
- Automated unit and integration tests.

Current automated test results:

37 tests passing.

The next development stage focuses on improving existing functionality,
reliability, and professional editing capabilities.

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

Status: In Progress

- [x] Implement cutting mat display.
- [x] Implement grid display.
- [x] Implement Ctrl + mouse wheel zoom.
- [x] Implement canvas selection.
- [x] Implement rubber-band selection.
- [ ] Implement dedicated zoom in/out controls.
- [ ] Implement zoom-to-fit.
- [ ] Implement canvas panning.
- [ ] Add configurable mat dimensions.
- [ ] Add measurement rulers.
- [ ] Add configurable grid spacing.
- [ ] Implement grid snapping.
- [ ] Implement object snapping.
- [ ] Implement alignment guides.
- [ ] Improve canvas rendering performance.

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
- [x] Implement rotation snapping with Shift.
- [x] Implement object duplication.
- [x] Implement Ctrl+D duplication shortcut.
- [x] Implement object deletion.
- [x] Implement object identifiers.
- [x] Implement object validation.
- [ ] Implement Shift + resize aspect-ratio locking.
- [ ] Implement copy and paste.
- [ ] Implement undo and redo.
- [ ] Implement grouping and ungrouping.
- [ ] Implement object alignment.
- [ ] Implement object distribution.
- [ ] Improve multi-object manipulation.

### Phase 4: Properties and Layers

Status: Partially Complete

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
- [ ] Implement fill color editing.
- [ ] Implement stroke color editing.
- [ ] Implement stroke width editing.
- [ ] Implement font selection.
- [ ] Implement font size editing.
- [ ] Implement layer creation.
- [ ] Implement layer deletion.
- [ ] Implement layer reordering.
- [ ] Improve layer management interface.

### Phase 5: Document Management

Status: Partially Complete

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
- [ ] Verify and correct Cancel behavior for unsaved changes.
- [ ] Implement undo and redo history.
- [ ] Implement autosave.
- [ ] Implement crash recovery.
- [ ] Implement recent project list.

### Phase 6: Vector Editing

Status: Planned

- [ ] Implement path objects.
- [ ] Implement freehand drawing.
- [ ] Implement Bézier curves.
- [ ] Implement node editing.
- [ ] Implement path joining.
- [ ] Implement path splitting.
- [ ] Implement boolean operations.
- [ ] Implement text editing.
- [ ] Implement font selection.
- [ ] Implement text-to-path conversion.
- [ ] Implement grouping and compound paths.

### Phase 7: File Import and Export

Status: Planned

- [ ] Implement SVG import.
- [ ] Implement SVG export.
- [ ] Implement PDF export.
- [ ] Implement PNG export.
- [ ] Preserve physical dimensions during export.
- [ ] Preserve object positions and rotations.
- [ ] Preserve layers where supported.
- [ ] Test compatibility with external vector applications.
- [ ] Document supported import and export features.

### Phase 8: Cutting Machine Integration

Status: Planned

- [ ] Establish cutter communication architecture.
- [ ] Research supported cutting machine protocols.
- [ ] Implement machine configuration profiles.
- [ ] Implement cutter discovery where supported.
- [ ] Implement cutting preview.
- [ ] Implement cut job preparation.
- [ ] Implement supported cutter communication.
- [ ] Add machine-specific settings.
- [ ] Implement job status reporting.
- [ ] Implement error handling.
- [ ] Test with physical cutting machines.

### Phase 9: Packaging and Distribution

Status: Planned

- [ ] Establish application versioning.
- [ ] Create Linux installation package.
- [ ] Create Windows installer.
- [ ] Create macOS application package.
- [ ] Bundle required Qt dependencies.
- [ ] Test clean installations.
- [ ] Establish release process.
- [ ] Publish user documentation.

---

## 4. Immediate Development Priorities

The next development work should follow this order.

1. Complete and verify Shift-based aspect-ratio locking.
2. Verify and correct unsaved-change Cancel behavior.
3. Implement undo and redo.
4. Improve canvas navigation.
5. Add copy and paste.
6. Improve object alignment and distribution.
7. Expand text properties.
8. Implement SVG export.
9. Implement SVG import.

These priorities should be revisited as functionality is completed.

---

## 5. Cross-Platform Requirements

CutStudio must not depend on developer-specific paths or manually
configured Qt environment variables.

Requirements:

- Use Python virtual environments.
- Maintain declared dependencies.
- Use PySide6 bundled Qt libraries and plugins.
- Avoid hardcoded developer-specific paths.
- Detect Qt platform integration automatically.
- Support X11 and Wayland where available.
- Test Windows independently.
- Test macOS independently.
- Document operating-system dependencies.

---

## 6. Development and Testing Policy

Every significant feature should include appropriate automated tests.

Existing functionality must not regress when new features are added.

Development should follow these principles:

- Test core document logic independently of the GUI.
- Test geometry and measurement conversions.
- Test document persistence.
- Test object manipulation.
- Test layer behavior.
- Add GUI interaction tests where practical.
- Run the complete test suite before committing significant changes.

Current baseline:

37 automated tests passing.

---

## 7. Long-Term Goal

Build CutStudio into a dependable, cross-platform vector design and
vinyl cutting application.

The application should provide:

- Accurate physical measurements.
- Professional vector editing tools.
- Reliable document management.
- Open vector file compatibility.
- Flexible layer management.
- Cutting job preparation.
- Extensible machine support.

The long-term objective is to provide a capable alternative to
proprietary vinyl cutting design software, including workflows
traditionally available in Brother ScanNCut software.

---

## 8. Roadmap Maintenance

Update this document whenever significant functionality is completed.

Only mark features as implemented when they have been verified.

Keep implemented functionality separate from planned functionality.

Maintain consistency between:

- ARCHITECTURE.md
- HANDOFF.md
- ROADMAP.md

The roadmap describes development objectives, not a guarantee
that every planned feature has been implemented.

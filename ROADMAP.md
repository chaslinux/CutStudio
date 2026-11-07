# CutStudio Development Roadmap

## 1. Project Vision

CutStudio is a cross-platform desktop vector design application built with Python and PySide6.

The goal is to create an accessible, reliable design environment for vinyl cutting, plotter workflows, and other vector-based fabrication projects.

The application should eventually support Linux, Windows, and macOS.

### Core Principles

- Cross-platform compatibility.
- Reproducible installation and development environments.
- Modular, maintainable architecture.
- Accurate physical measurements.
- Non-destructive editing wherever practical.
- Open vector file formats.
- Extensible machine and cutter support.

---

## 2. Development Phases

### Phase 1: Foundation and Application Structure

**Status: In Progress**

- [x] Establish Python virtual environment.
- [x] Install PySide6.
- [x] Create initial application window.
- [x] Implement basic menu bar.
- [x] Implement main toolbar.
- [x] Create left drawing tools panel.
- [x] Create right properties and layers panel.
- [x] Implement initial 12 × 12 inch cutting mat.
- [x] Implement basic grid.
- [x] Implement rectangle tool.
- [x] Implement ellipse tool.
- [x] Implement text tool.
- [x] Implement object selection and movement.
- [x] Implement Ctrl + mouse wheel zoom.
- [x] Resolve Qt platform plugin initialization on Linux.
- [ ] Establish reproducible cross-platform Qt configuration.
- [ ] Document installation dependencies.
- [ ] Create automated startup tests.

### Phase 2: Canvas and Navigation

- [ ] Implement zoom in/out controls.
- [ ] Implement zoom-to-fit.
- [ ] Implement canvas panning.
- [ ] Add configurable mat dimensions.
- [ ] Add measurement rulers.
- [ ] Add configurable grid spacing.
- [ ] Add grid snapping.
- [ ] Add object snapping and alignment guides.
- [ ] Improve canvas rendering performance.

### Phase 3: Object Editing

- [ ] Implement object selection.
- [ ] Implement multi-selection.
- [ ] Implement resize handles.
- [ ] Implement object rotation.
- [ ] Implement object duplication.
- [ ] Implement delete and copy/paste.
- [ ] Implement undo/redo.
- [ ] Implement grouping and ungrouping.
- [ ] Implement object locking.
- [ ] Implement object alignment and distribution.

### Phase 4: Properties and Layers

- [ ] Implement live object properties.
- [ ] Add position controls (X/Y).
- [ ] Add width and height controls.
- [ ] Add rotation controls.
- [ ] Add fill and stroke controls.
- [ ] Add line width controls.
- [ ] Implement functional layer management.
- [ ] Add layer visibility.
- [ ] Add layer locking.
- [ ] Add layer reordering.

### Phase 5: Vector Editing

- [ ] Implement path objects.
- [ ] Implement Bézier curves.
- [ ] Implement node editing.
- [ ] Implement path joining and splitting.
- [ ] Implement boolean operations.
- [ ] Implement text editing and font selection.
- [ ] Implement text-to-path conversion.

### Phase 6: File Support

- [ ] Implement native CutStudio project format.
- [ ] Implement SVG import.
- [ ] Implement SVG export.
- [ ] Implement PDF export.
- [ ] Implement PNG export.
- [ ] Implement project save/load.
- [ ] Implement autosave and recovery.

### Phase 7: Cutting Machine Integration

- [ ] Establish cutter communication architecture.
- [ ] Implement machine configuration profiles.
- [ ] Implement cutter discovery where supported.
- [ ] Implement cutting preview.
- [ ] Implement cut job preparation.
- [ ] Implement supported cutter communication protocols.
- [ ] Add machine-specific settings.
- [ ] Implement job status and error reporting.

### Phase 8: Packaging and Distribution

- [ ] Create Linux installation package.
- [ ] Create Windows installer.
- [ ] Create macOS application package.
- [ ] Bundle required Qt dependencies.
- [ ] Test clean installations.
- [ ] Establish release and versioning process.
- [ ] Publish user documentation.

---

## 3. Architecture Guidelines

The application should evolve beyond a single-file implementation.

Recommended responsibilities:

- `canvas/`: Drawing surface, grid, navigation, and rendering.
- `tools/`: Selection, shapes, text, and path editing.
- `panels/`: Properties, layers, and application sidebars.
- `models/`: Document, layer, and object data models.
- `exporters/`: SVG, PDF, and raster export.
- `machine/`: Cutter profiles, communication, and job management.

The graphical interface should remain separate from the underlying document model.

This will make future features easier to test and maintain.

---

## 4. Cross-Platform Requirements

CutStudio should not depend on machine-specific paths or manually configured Qt environment variables.

Requirements:

- Use Python virtual environments.
- Declare dependencies in project metadata.
- Use PySide6's bundled Qt libraries and plugins.
- Avoid hardcoded developer-specific paths.
- Detect the appropriate Qt platform integration automatically.
- Support X11 and Wayland on Linux where available.
- Test Windows and macOS independently.
- Document operating-system-level dependencies.

---

## 5. Development Priorities

Our immediate priorities are:

1. Establish the project architecture.
2. Make installation and startup reproducible.
3. Improve the canvas and navigation.
4. Implement functional object properties.
5. Establish a proper document and layer model.
6. Add SVG import/export.

---

## 6. Long-Term Goal

Build CutStudio into a dependable, cross-platform vector design and vinyl cutting application with a clean interface, accurate measurements, and extensible hardware support.

The project should remain modular so that additional design tools, file formats, and cutting machines can be supported without major architectural changes.

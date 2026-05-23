# Annotated Score — Constraint Overlay Sheet Music Specification

**Status:** Draft v0.1  
**Date:** 2026-05-23  
**Authors:** SuperInstance Research

---

## 1. Introduction

Traditional sheet music tells you *what* notes to play. The Annotated Score tells you *why* — by overlaying the active constraints that shaped each note's position, timing, and dynamics onto standard musical notation.

This specification defines a visual language, data format, and rendering model for **constraint-augmented sheet music**: a new kind of score where color-coded layers reveal the hidden forces acting on every note.

### 1.1 Motivation

Constraint-based music systems (snap lattices, funnel attractors, consensus protocols, rigid Laman substructures, tempo governors) produce music through the interaction of multiple simultaneous constraints. Performers, students, and analysts currently have no way to *see* these constraints in the score. The Annotated Score makes the invisible visible.

### 1.2 Design Principles

1. **Non-destructive layering** — constraint overlays add information without obscuring the underlying notation.
2. **Progressive disclosure** — a score should be readable without constraints; constraints enhance understanding when activated.
3. **Accessibility** — every visual encoding has a pattern-based fallback (not color alone).
4. **Machine-readable** — constraint annotations are structured data, not just visual decoration.

---

## 2. Visual Language

### 2.1 Constraint Type Colors

Each constraint type maps to a distinct color and pattern:

| Constraint | Color | Hex | Pattern | Visual Element |
|---|---|---|---|---|
| **Snap** | Blue | `#4A90D9` | Dotted outline | Highlight on note heads showing lattice grid |
| **Funnel** | Green | `#2ECC71` | Gradient fill | Arrows showing gravitational pull toward target |
| **Consensus** | Gold | `#F1C40F` | Dashed lines | Connecting lines between voices showing agreement/tension |
| **Laman** | Red | `#E74C3C` | Solid brackets | Brackets marking rigid (generically rigid) sections |
| **Tempo** | Purple | `#9B59B6` | Pulsing dots | Metronomic pressure marks |

### 2.2 Intensity Encoding

Constraint *strength* maps to visual intensity:

- **Opacity** — 0.3 (weak/near-deadband) to 1.0 (fully active)
- **Saturation** — desaturated at low intensity, vivid at high
- **Line weight** — thin (1px) for weak, thick (3px) for strong

The formula for visual opacity:

```
visual_opacity = 0.3 + 0.7 × (constraint_strength / max_strength)
```

### 2.3 Note Head Modifications

When a constraint is active on a note:

- The note head fill adopts the constraint color (blended if multiple)
- A small symbol appears above/below the note head:
  - **Snap**: ⊞ (grid icon)
  - **Funnel**: ↘ (pull arrow)
  - **Consensus**: ⊙ (agreement circle)
  - **Laman**: ⊓ (rigid bracket)
  - **Tempo**: ♩ (metronome mark)

For accessibility, these symbols are always present (not color-only encoding).

### 2.4 Constraint Region Brackets

Above each staff system, horizontal brackets span the duration of each active constraint region:

```
╔═════════════════╗        ╔══════════╗
║  SNAP (lattice) ║        ║ LAMAN    ║
╚═════════════════╝        ╚══════════╝
```

Multiple brackets can stack vertically when constraints overlap. Each bracket is color-coded and labeled with the constraint type and its key parameter.

### 2.5 Margin Annotations

The left margin (or right, for even pages) contains:

- **Constraint parameters** — lattice spacing, funnel target, Laman dimension
- **Small constraint diagram** — a miniature visualization of the constraint's state, analogous to figured bass numerals but for constraints

Example margin annotation:

```
┌─────────────┐
│ SNAP: d=12  │
│ lattice:    │
│  ┌─┬─┬─┐   │
│  │●│ │●│   │
│  ├─┼─┼─┤   │
│  │ │●│ │   │
│  └─┴─┴─┘   │
│ target: C4  │
└─────────────┘
```

### 2.6 Funnel Arrows

Funnel constraints render as green gradient arrows overlaid on the staff:

- Arrow points from current note toward the attractor target
- Arrow opacity indicates pull strength
- Multiple funnel targets produce multiple arrows with different shades

### 2.7 Consensus Lines

When voices agree (or disagree) via consensus constraints:

- **Gold solid lines** connect synchronized note heads across staves
- **Gold dashed lines** indicate partial agreement (within tolerance)
- **No line** = consensus not reached (useful for spotting tension)

---

## 3. Notation Extensions

### 3.1 Multi-Constraint Blending

When multiple constraints act on the same note, the note head uses a **segmented fill** — each constraint claims a proportional wedge of the note head circle. The dominant constraint occupies the largest wedge.

Alternatively, renderers may display the note head in the color of the *strongest* constraint and show secondary constraints as colored dots around the note.

### 3.2 Constraint Transitions

When a constraint activates or deactivates mid-measure:

- A thin vertical line marks the transition point
- A small label (e.g., "SNAP on", "FUNNEL off") appears at the transition
- The bracket above the staff begins or ends at this point

### 3.3 Dynamic Constraint Indicators

For constraints that change intensity over time:

- A small intensity graph (sparkline) appears below the staff for that region
- The graph's color matches the constraint type
- This is optional and typically used in analysis/teaching contexts

---

## 4. Data Format

### 4.1 Score Representation

An Annotated Score consists of:

1. **Base score** — MusicXML or LilyPond notation (standard)
2. **Constraint annotations** — JSON sidecar or embedded annotations

### 4.2 JSON Schema for Constraint Annotations

```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "Annotated Score Constraint Annotations",
  "type": "object",
  "properties": {
    "version": { "type": "string", "const": "0.1" },
    "scoreRef": { "type": "string", "description": "Reference to base score file" },
    "constraints": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["id", "type", "region", "params"],
        "properties": {
          "id": { "type": "string" },
          "type": { 
            "type": "string",
            "enum": ["snap", "funnel", "consensus", "laman", "tempo"]
          },
          "region": {
            "type": "object",
            "properties": {
              "startMeasure": { "type": "integer" },
              "startBeat": { "type": "number" },
              "endMeasure": { "type": "integer" },
              "endBeat": { "type": "number" },
              "staff": { "type": "integer" },
              "voice": { "type": "integer" }
            }
          },
          "params": { "type": "object" },
          "intensity": {
            "type": "object",
            "description": "Optional per-beat intensity curve",
            "properties": {
              "type": { "enum": ["constant", "linear", "curve"] },
              "values": { 
                "type": "array", 
                "items": { "type": "number", "min": 0, "max": 1 }
              }
            }
          }
        }
      }
    }
  }
}
```

### 4.3 Example Annotation

```json
{
  "version": "0.1",
  "scoreRef": "melody.musicxml",
  "constraints": [
    {
      "id": "snap-1",
      "type": "snap",
      "region": { "startMeasure": 1, "startBeat": 1, "endMeasure": 2, "endBeat": 4, "staff": 1, "voice": 1 },
      "params": { "latticeType": "tonnetz", "spacing": 7, "target": "C4" },
      "intensity": { "type": "constant", "values": [0.8] }
    },
    {
      "id": "funnel-1",
      "type": "funnel",
      "region": { "startMeasure": 1, "startBeat": 3, "endMeasure": 2, "endBeat": 4, "staff": 1, "voice": 1 },
      "params": { "attractor": "G4", "pullStrength": 0.6, "deadband": 0.05 },
      "intensity": { "type": "linear", "values": [0.2, 0.4, 0.6, 0.8, 1.0] }
    }
  ]
}
```

---

## 5. Rendering Architecture

### 5.1 SVG Layer Model

The Annotated Score renders as layered SVG:

```
<svg>
  <g id="staff-lines">        <!-- Base staff lines -->
  <g id="notes">              <!-- Standard note rendering -->
  <g id="constraint-snap">    <!-- Snap overlay layer -->
  <g id="constraint-funnel">  <!-- Funnel overlay layer -->
  <g id="constraint-consensus"><!-- Consensus overlay layer -->
  <g id="constraint-laman">   <!-- Laman overlay layer -->
  <g id="constraint-tempo">   <!-- Tempo overlay layer -->
  <g id="brackets">           <!-- Region brackets above staff -->
  <g id="annotations">        <!-- Margin annotations -->
</svg>
```

Each constraint type is a separate SVG group, enabling:

- Selective show/hide of constraint types
- Independent styling and animation
- Clean layering without z-index conflicts

### 5.2 Rendering Pipeline

1. Parse base score (MusicXML/LilyPond) → note positions, timing, pitch
2. Load constraint annotations → map constraints to time regions
3. For each time slice, determine active constraints and intensities
4. Render base notation (staff + notes)
5. For each constraint layer, render overlays at computed positions
6. Render brackets and margin annotations

### 5.3 Print vs. Interactive

- **Print/static**: All layers composited into a single SVG/PDF
- **Interactive (web)**: Layers toggleable via checkboxes; hover on notes shows constraint details; intensity animations possible

---

## 6. Use Cases

### 6.1 Teaching Tool

Students can *see why* a note is where it is. Instead of memorizing rules, they observe constraint forces shaping the music in real time. An instructor might show only the snap layer to explain lattice quantization, then add the funnel layer to show how gravity toward a target note shapes melodic contour.

### 6.2 Analysis Tool

Given two performances of the same piece, overlay their constraint adherence profiles. Where do they agree? Where does one performer "resist" a constraint while another conforms? This reveals interpretive differences as constraint space trajectories.

### 6.3 Composition Tool

Compose directly in constraint space: define regions, set constraint parameters, and let the system generate note candidates. The annotated score becomes the *interface* — the composer adjusts constraints and sees the musical result, adjusting in a feedback loop.

### 6.4 Accessibility

All visual encodings are dual-coded (color + pattern/symbol). A color-blind musician can distinguish constraint types by their symbols (⊞, ↘, ⊙, ⊓, ♩) and line patterns (dotted, solid, dashed). Screen readers can describe constraint annotations from the structured JSON data.

---

## 7. Constraint-Specific Visual Details

### 7.1 Snap Constraints (Blue)

- Note heads outlined in blue with dotted pattern
- Faint grid lines visible behind the staff in the snap region, showing the lattice
- Small numbers above notes indicating snap distance (how far the note was pulled to the lattice point)

### 7.2 Funnel Constraints (Green)

- Green gradient arrows from each note toward the attractor pitch
- The attractor pitch itself is highlighted with a green halo
- Arrow thickness proportional to pull strength
- Deadband region shown as a faint green band around the attractor

### 7.3 Consensus Constraints (Gold)

- Gold lines connect note heads across voices/staves that are in consensus
- Solid line = agreement within tolerance
- Dashed = borderline (near edge of tolerance)
- A small "agreement percentage" label optionally appears at the midpoint

### 7.4 Laman Constraints (Red)

- Red brackets above the staff span rigid sections
- Notes within a Laman region have a faint red background
- The bracket label includes the rigidity dimension (e.g., "Laman d=3")

### 7.5 Tempo Constraints (Purple)

- Purple dots at beat positions, sized by tempo pressure
- A small tempo curve appears below the staff in the constrained region
- Metronome markings in the margin are highlighted purple when tempo-constrained

---

## 8. Relationship to Existing Standards

| Standard | Relationship |
|---|---|
| MusicXML | Base notation format; constraint annotations are a separate JSON layer |
| LilyPond | Alternative base notation; annotations via custom markup commands |
| SVG | Rendering target with constraint layers as `<g>` groups |
| MIDI | Timing reference; constraint annotations align to MIDI tick positions |
| MEI (Music Encoding Initiative) | Potential future integration as custom MEI metadata |

---

## 9. Future Directions

- **Animation** — SVG animations showing constraints activating/deactivating during playback
- **3D rendering** — WebGL depth for overlapping constraints (especially useful for multi-voice consensus)
- **Haptic feedback** — constraint intensity mapped to vibration for accessible score reading
- **AI-assisted annotation** — automatically infer constraints from existing scores
- **Collaborative annotation** — multiple analysts annotating the same score with different constraint interpretations

---

## 10. Conclusion

The Annotated Score transforms sheet music from a static prescription into a dynamic map of the forces that shape music. By making constraints visible, we open new possibilities for teaching, analysis, composition, and accessibility in constraint-based music systems.

---

*This specification is part of the SuperInstance FM Research project.*

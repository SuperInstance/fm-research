# PHYSICAL-INSTRUMENTS-CAD/

CAD files for the physical constraint instruments described in [PHYSICAL-INSTRUMENTS.md](../PHYSICAL-INSTRUMENTS.md).

## File Conventions

### Directory Structure

```
PHYSICAL-INSTRUMENTS-CAD/
├── README.md              ← you are here
├── lattice-piano/         ← SNAP instrument
│   ├── cam-shaft/
│   ├── follower/
│   ├── enclosure/
│   └── README.md
├── gravity-well/          ← FUNNEL instrument
│   ├── bowl-linear/
│   ├── bowl-exponential/
│   ├── bowl-gaussian/
│   ├── frame/
│   └── README.md
├── agreement-network/     ← CONSENSUS instrument
│   ├── fader-mount/
│   ├── cord-routing/
│   ├── base-plate/
│   └── README.md
├── rigidity-board/        ← LAMAN instrument
│   ├── pegs/
│   ├── bars/
│   ├── joints/
│   └── README.md
├── metronome-funnel/      ← TEMPO instrument
│   ├── pendulum-mount/
│   ├── led-housing/
│   ├── pad-mount/
│   └── README.md
└── shared/                ← Reusable parts (brackets, mounts, etc.)
```

### File Formats

| Format | Extension | Use |
|---|---|---|
| OpenSCAD | `.scad` | Parametric source files (preferred for editable designs) |
| STL | `.stl` | 3D-printable export (binary preferred) |
| STEP | `.step` | CAD interchange for CNC milling |
| SVG | `.svg` | 2D profiles for laser cutting |
| PDF | `.pdf` | Dimensioned drawings for manual fabrication |

### Naming Convention

`{part-name}-{version}.{ext}`

Examples:
- `cam-shaft-12tet-v1.scad`
- `peg-balljoint-v2.stl`
- `bowl-gaussian-profile-v1.step`

### Parametric Design

All OpenSCAD files should expose key parameters at the top of the file:

```openscad
// === PARAMETERS ===
lattice_resolution = 12;    // TET
key_travel_mm = 60;
snap_force_n = 0.8;
// === END PARAMETERS ===
```

This allows regenerating parts for different configurations without understanding the full geometry.

### Versioning

- `v1` = initial design, untested
- `v2` = first revision after physical test
- `v3+` = refined designs

Tag working designs with a `README.md` note: "Printed and tested ✓"

### License

All CAD files in this directory are released under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) unless otherwise noted. Build them, modify them, share them.

---

To contribute CAD files, open a PR against the `fm-research` repo with files placed in the appropriate subdirectory following the conventions above.

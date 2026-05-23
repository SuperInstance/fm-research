#!/usr/bin/env python3
"""
Annotated Score Demo — generates an SVG of a C major scale with constraint overlays.

No external dependencies beyond the Python standard library.
Outputs: annotated-score-demo.svg
"""

import math

# ── SVG helpers ──────────────────────────────────────────────────────────

def svg_header(width, height, viewBox=None):
    if viewBox is None:
        viewBox = f"0 0 {width} {height}"
    return f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="{viewBox}">
<style>
  .staff-line {{ stroke: #999; stroke-width: 1; }}
  .barline {{ stroke: #333; stroke-width: 1.5; }}
  .note-head {{ fill: #333; }}
  text {{ font-family: "Helvetica Neue", Arial, sans-serif; }}
  .label {{ font-size: 10px; fill: #666; }}
  .title {{ font-size: 18px; font-weight: bold; fill: #222; }}
  .subtitle {{ font-size: 12px; fill: #888; }}
  .bracket-label {{ font-size: 9px; font-weight: 600; }}
  .margin-label {{ font-size: 8px; fill: #555; }}
  .pitch-label {{ font-size: 11px; font-weight: bold; }}
</style>
'''

def svg_footer():
    return '</svg>\n'

def rect(x, y, w, h, fill, opacity=1.0, rx=0):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" opacity="{opacity}" rx="{rx}"/>\n'

def circle(cx, cy, r, fill, opacity=1.0, stroke=None, stroke_width=1):
    s = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{fill}" opacity="{opacity}"'
    if stroke:
        s += f' stroke="{stroke}" stroke-width="{stroke_width}"'
    return s + '/>\n'

def line(x1, y1, x2, y2, stroke, stroke_width=1, opacity=1.0, dash=None):
    s = f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{stroke}" stroke-width="{stroke_width}" opacity="{opacity}"'
    if dash:
        s += f' stroke-dasharray="{dash}"'
    return s + '/>\n'

def polygon(points, fill, opacity=1.0, stroke=None):
    s = f'<polygon points="{" ".join(str(p) for p in points)}" fill="{fill}" opacity="{opacity}"'
    if stroke:
        s += f' stroke="{stroke}"'
    return s + '/>\n'

def text(x, y, content, cls=None, fill=None, font_size=None, anchor=None, weight=None):
    s = '<text'
    s += f' x="{x}" y="{y}"'
    if cls:
        s += f' class="{cls}"'
    if fill:
        s += f' fill="{fill}"'
    if font_size:
        s += f' font-size="{font_size}"'
    if anchor:
        s += f' text-anchor="{anchor}"'
    if weight:
        s += f' font-weight="{weight}"'
    return s + f'>{content}</text>\n'

def group(id):
    return f'<g id="{id}">\n'

def end_group():
    return '</g>\n'


# ── Music constants ──────────────────────────────────────────────────────

# C major scale: C4 D4 E4 F4 G4 A4 B4 C5
SCALE = ['C4', 'D4', 'E4', 'F4', 'G4', 'A4', 'B4', 'C5']

# Staff position (y offset from staff top line) — higher pitch = lower y
# Top line of treble clef (E5) = y=0, each semitone step is ~3.5px
# For simplicity, map diatonic steps in one octave
STAFF_TOP_Y = 80  # y of top line
LINE_SPACING = 12
NOTE_RADIUS = 5.5

def pitch_to_y(pitch):
    """Map pitch name to y position on staff."""
    note_map = {'C': 0, 'D': 1, 'E': 2, 'F': 3, 'G': 4, 'A': 5, 'B': 6}
    name = pitch[0]
    octave = int(pitch[1])
    # C4 is on the first ledger line below treble clef
    # Position relative to top line (E5)
    # E5=0, D5=1, C5=2, B4=3, A4=4, G4=5, F4=6, E4=7, D4=8, C4=9
    top_ref = {'C': 9, 'D': 8, 'E': 7, 'F': 6, 'G': 5, 'A': 4, 'B': 3}  # for octave 4
    offset = top_ref[name] - (octave - 4) * 7
    return STAFF_TOP_Y + offset * (LINE_SPACING / 2)


# ── Layout ───────────────────────────────────────────────────────────────

MARGIN_LEFT = 120
MARGIN_RIGHT = 40
NOTE_SPACING = 70
STAFF_WIDTH = len(SCALE) * NOTE_SPACING
SVG_WIDTH = MARGIN_LEFT + STAFF_WIDTH + MARGIN_RIGHT
SVG_HEIGHT = 300

# Note x positions
def note_x(i):
    return MARGIN_LEFT + 30 + i * NOTE_SPACING

# ── Constraint definitions ───────────────────────────────────────────────

# Colors
SNAP_COLOR = "#4A90D9"
FUNNEL_COLOR = "#2ECC71"
CONSENSUS_COLOR = "#F1C40F"

# Snap constraint: active on notes 0-5 (C4 through A4)
SNAP_REGION = (0, 5)
SNAP_INTENSITY = [0.8, 0.9, 0.7, 0.85, 0.95, 0.75]

# Funnel constraint: active on notes 3-7 (F4 through C5), pulling toward G4
FUNNEL_REGION = (3, 7)
FUNNEL_TARGET_IDX = 4  # G4
FUNNEL_INTENSITY = [0.3, 0.5, 0.7, 0.85, 1.0]

# Consensus: connecting notes 2-4 between two implied voices
CONSENSUS_PAIRS = [(2, 4), (3, 5)]  # E4-G4, F4-A4


# ── Build SVG ────────────────────────────────────────────────────────────

def build_svg():
    out = svg_header(SVG_WIDTH, SVG_HEIGHT)
    
    # Title
    out += text(MARGIN_LEFT + 10, 35, "Annotated Score Demo", cls="title")
    out += text(MARGIN_LEFT + 10, 52, "C Major Scale — Constraint Overlays", cls="subtitle")
    
    # ── Staff lines ──
    out += group("staff-lines")
    staff_lines_y = [STAFF_TOP_Y + i * LINE_SPACING for i in range(5)]
    for y in staff_lines_y:
        out += line(MARGIN_LEFT, y, SVG_WIDTH - MARGIN_RIGHT, y, "#999", 1)
    # Ledger line for C4 (below staff)
    c4_y = pitch_to_y('C4')
    out += line(note_x(0) - 15, c4_y, note_x(0) + 15, c4_y, "#999", 1)
    # Ledger line for middle C (below staff)
    # Barlines
    out += line(MARGIN_LEFT, STAFF_TOP_Y, MARGIN_LEFT, STAFF_TOP_Y + 4 * LINE_SPACING, "#333", 1.5)
    out += line(SVG_WIDTH - MARGIN_RIGHT, STAFF_TOP_Y, SVG_WIDTH - MARGIN_RIGHT, STAFF_TOP_Y + 4 * LINE_SPACING, "#333", 1.5)
    out += end_group()
    
    # ── Snap constraint layer (blue) ──
    out += group("constraint-snap")
    for i in range(SNAP_REGION[0], SNAP_REGION[1] + 1):
        x = note_x(i)
        y = pitch_to_y(SCALE[i])
        intensity = SNAP_INTENSITY[i - SNAP_REGION[0]]
        opacity = 0.3 + 0.7 * intensity
        # Blue glow around note
        out += circle(x, y, NOTE_RADIUS + 6, SNAP_COLOR, opacity=0.25 * intensity)
        out += circle(x, y, NOTE_RADIUS + 3, SNAP_COLOR, opacity=0.4 * intensity)
        # Faint lattice grid lines (horizontal guides near note)
        out += line(x - 20, y - LINE_SPACING, x + 20, y - LINE_SPACING, SNAP_COLOR, 0.5, opacity=0.3)
        out += line(x - 20, y + LINE_SPACING, x + 20, y + LINE_SPACING, SNAP_COLOR, 0.5, opacity=0.3)
        # Snap distance label
        dist = abs(i - 0)  # snap distance from lattice root
        out += text(x, y - NOTE_RADIUS - 10, f"d={dist}", cls="margin-label", fill=SNAP_COLOR, font_size=8)
    out += end_group()
    
    # ── Funnel constraint layer (green) ──
    out += group("constraint-funnel")
    funnel_target_x = note_x(FUNNEL_TARGET_IDX)
    funnel_target_y = pitch_to_y(SCALE[FUNNEL_TARGET_IDX])
    # Green halo on target
    out += circle(funnel_target_x, funnel_target_y, NOTE_RADIUS + 10, FUNNEL_COLOR, opacity=0.15)
    out += circle(funnel_target_x, funnel_target_y, NOTE_RADIUS + 5, FUNNEL_COLOR, opacity=0.25)
    # Target label
    out += text(funnel_target_x, funnel_target_y + NOTE_RADIUS + 22, "⟵ target", 
                cls="margin-label", fill=FUNNEL_COLOR, font_size=8, weight="bold")
    
    for j, i in enumerate(range(FUNNEL_REGION[0], FUNNEL_REGION[1] + 1)):
        if i == FUNNEL_TARGET_IDX:
            continue  # skip arrow on target itself
        x = note_x(i)
        y = pitch_to_y(SCALE[i])
        intensity = FUNNEL_INTENSITY[j]
        opacity = 0.3 + 0.7 * intensity
        # Arrow from note toward target
        dx = funnel_target_x - x
        dy = funnel_target_y - y
        dist = math.sqrt(dx*dx + dy*dy)
        if dist > 0:
            # Shorten arrow to not overlap note heads
            ux, uy = dx/dist, dy/dist
            ax1 = x + ux * (NOTE_RADIUS + 2)
            ay1 = y + uy * (NOTE_RADIUS + 2)
            ax2 = funnel_target_x - ux * (NOTE_RADIUS + 4)
            ay2 = funnel_target_y - uy * (NOTE_RADIUS + 4)
            out += line(ax1, ay1, ax2, ay2, FUNNEL_COLOR, 1.5 + intensity, opacity=opacity * 0.7)
            # Arrowhead
            angle = math.atan2(dy, dx)
            arrow_size = 6
            tip_x, tip_y = ax2, ay2
            p1 = (tip_x, tip_y)
            p2 = (tip_x - arrow_size * math.cos(angle - 0.4), tip_y - arrow_size * math.sin(angle - 0.4))
            p3 = (tip_x - arrow_size * math.cos(angle + 0.4), tip_y - arrow_size * math.sin(angle + 0.4))
            out += polygon([p1, p2, p3], FUNNEL_COLOR, opacity=opacity * 0.7)
    out += end_group()
    
    # ── Consensus constraint layer (gold) ──
    out += group("constraint-consensus")
    for (a, b) in CONSENSUS_PAIRS:
        ax, ay = note_x(a), pitch_to_y(SCALE[a])
        bx, by = note_x(b), pitch_to_y(SCALE[b])
        # Curved connecting line (approximated with straight dashed)
        out += line(ax, ay, bx, by, CONSENSUS_COLOR, 1.5, opacity=0.6, dash="4,3")
        # Agreement circle at midpoint
        mx, my = (ax + bx) / 2, (ay + by) / 2
        out += circle(mx, my, 4, CONSENSUS_COLOR, opacity=0.4)
        out += text(mx + 7, my + 3, "⊙", fill=CONSENSUS_COLOR, font_size=9)
    out += end_group()
    
    # ── Notes (on top of overlays) ──
    out += group("notes")
    for i, pitch in enumerate(SCALE):
        x = note_x(i)
        y = pitch_to_y(pitch)
        
        # Determine note head color based on active constraints
        in_snap = SNAP_REGION[0] <= i <= SNAP_REGION[1]
        in_funnel = FUNNEL_REGION[0] <= i <= FUNNEL_REGION[1]
        
        if in_snap and in_funnel:
            # Blended: use a teal-ish color
            head_fill = "#3AA89E"
        elif in_snap:
            head_fill = SNAP_COLOR
        elif in_funnel:
            head_fill = FUNNEL_COLOR
        else:
            head_fill = "#333"
        
        # Note head (ellipse approximated as circle)
        out += circle(x, y, NOTE_RADIUS, head_fill)
        out += circle(x, y, NOTE_RADIUS, "none", stroke=head_fill, stroke_width=0.5)
        
        # Stem (going up for notes below middle line, down for above)
        mid_staff_y = STAFF_TOP_Y + 2 * LINE_SPACING
        stem_len = 30
        if y > mid_staff_y:
            # Stem up (right side)
            out += line(x + NOTE_RADIUS, y, x + NOTE_RADIUS, y - stem_len, head_fill, 1.2)
        else:
            # Stem down (left side)
            out += line(x - NOTE_RADIUS, y, x - NOTE_RADIUS, y + stem_len, head_fill, 1.2)
        
        # Pitch label below
        out += text(x, y + NOTE_RADIUS + 28, pitch, cls="pitch-label", 
                    fill=head_fill, font_size=10, anchor="middle", weight="bold")
    out += end_group()
    
    # ── Constraint region brackets ──
    bracket_y = STAFF_TOP_Y - 25
    out += group("brackets")
    
    # Snap bracket
    sx = note_x(SNAP_REGION[0]) - 15
    ex = note_x(SNAP_REGION[1]) + 15
    out += line(sx, bracket_y, ex, bracket_y, SNAP_COLOR, 2)
    out += line(sx, bracket_y, sx, bracket_y + 5, SNAP_COLOR, 2)
    out += line(ex, bracket_y, ex, bracket_y + 5, SNAP_COLOR, 2)
    out += text((sx + ex) / 2, bracket_y - 5, "SNAP (Tonnetz lattice)", 
                cls="bracket-label", fill=SNAP_COLOR, font_size=9, anchor="middle")
    
    # Funnel bracket (offset below snap)
    bracket_y2 = bracket_y - 20
    fx = note_x(FUNNEL_REGION[0]) - 15
    fex = note_x(FUNNEL_REGION[1]) + 15
    out += line(fx, bracket_y2, fex, bracket_y2, FUNNEL_COLOR, 2)
    out += line(fx, bracket_y2, fx, bracket_y2 + 5, FUNNEL_COLOR, 2)
    out += line(fex, bracket_y2, fex, bracket_y2 + 5, FUNNEL_COLOR, 2)
    out += text((fx + fex) / 2, bracket_y2 - 5, "FUNNEL → G4", 
                cls="bracket-label", fill=FUNNEL_COLOR, font_size=9, anchor="middle")
    
    out += end_group()
    
    # ── Margin annotations ──
    out += group("annotations")
    margin_x = 8
    out += rect(margin_x, STAFF_TOP_Y - 10, 100, 80, "#f0f0f0", opacity=0.8, rx=4)
    out += text(margin_x + 5, STAFF_TOP_Y + 5, "Constraint Parameters", 
                cls="margin-label", fill="#333", font_size=8, weight="bold")
    out += text(margin_x + 5, STAFF_TOP_Y + 18, "SNAP: lattice d=7",
                cls="margin-label", fill=SNAP_COLOR, font_size=8)
    out += text(margin_x + 5, STAFF_TOP_Y + 30, "FUNNEL: target=G4",
                cls="margin-label", fill=FUNNEL_COLOR, font_size=8)
    out += text(margin_x + 5, STAFF_TOP_Y + 42, "  pull=0.6, db=0.05",
                cls="margin-label", fill=FUNNEL_COLOR, font_size=7)
    out += text(margin_x + 5, STAFF_TOP_Y + 55, "CONSENSUS: tol=0.1",
                cls="margin-label", fill=CONSENSUS_COLOR, font_size=8)
    
    # Mini lattice diagram
    out += text(margin_x + 5, STAFF_TOP_Y + 72, "Lattice:",
                cls="margin-label", fill="#999", font_size=7)
    for row in range(3):
        for col in range(3):
            cx = margin_x + 25 + col * 14
            cy = STAFF_TOP_Y + 82 + row * 10
            filled = (row + col) % 2 == 0
            out += circle(cx, cy, 3, SNAP_COLOR if filled else "#ddd", opacity=0.7 if filled else 0.3)
    
    out += end_group()
    
    # ── Legend ──
    legend_y = STAFF_TOP_Y + 4 * LINE_SPACING + 30
    out += group("legend")
    out += text(MARGIN_LEFT, legend_y, "Legend:", font_size=10, weight="bold")
    
    items = [
        (SNAP_COLOR, "Snap — lattice quantization"),
        (FUNNEL_COLOR, "Funnel — gravitational pull toward target"),
        (CONSENSUS_COLOR, "Consensus — voice agreement"),
    ]
    for j, (color, label) in enumerate(items):
        ly = legend_y + 16 + j * 14
        out += circle(MARGIN_LEFT + 6, ly - 3, 4, color)
        out += text(MARGIN_LEFT + 16, ly, label, font_size=9, fill=color)
    
    # Pattern fallback note
    out += text(MARGIN_LEFT, legend_y + 60, "Patterns: ⊞ Snap  ↘ Funnel  ⊙ Consensus",
                font_size=8, fill="#999")
    out += end_group()
    
    out += svg_footer()
    return out


# ── Main ─────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    svg = build_svg()
    output_path = "annotated-score-demo.svg"
    with open(output_path, "w") as f:
        f.write(svg)
    print(f"Generated {output_path} ({len(svg)} bytes)")

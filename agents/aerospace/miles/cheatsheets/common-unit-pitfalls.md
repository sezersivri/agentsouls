---
topic: "Common Unit and Reference Pitfalls"
agent: "miles"
confidence: "VERIFIED"
source: "Accumulated field experience, AIAA standards, engineering mishap reports"
last_updated: "2026-02-18"
version: "1.0"
---

# Common Unit and Reference Pitfalls

> **One-line summary:** Unit conversion errors, reference inconsistencies, and dimensional analysis traps that cause aerodynamic analysis failures — catch them before they bite.

## Key Concepts

**The Three Unit Traps:**
1. **Unit inconsistency** — Mixing SI and Imperial units (meters vs feet, kg vs slugs)
2. **Reference confusion** — Swapping reference area, length, or moment center between tools
3. **Angular units** — Degrees vs radians in derivatives and trigonometric functions

**Defense Strategy:**
- **Always check units explicitly** — Write units next to every number in hand calculations
- **Verify reference quantities** — Sref, Lref, Xref must match between analysis tools, CFD, and flight code
- **Dimensional analysis** — If units don't cancel correctly, equation is wrong

**Famous Mishaps:**
- Mars Climate Orbiter (1999): Thruster software in lbf·s, navigation expected N·s → $327M loss
- Gimli Glider (1983): Fuel loaded in pounds, gauge read kilograms → Ran out of fuel mid-flight
- NASA Mars Polar Lander (1999): Altitude in meters vs feet confusion → Crashed

## Quick Reference: Conversion Table

| Quantity | SI | Imperial | Conversion Factor |
|----------|----|----|-------------------|
| **Length** | meter (m) | foot (ft) | 1 ft = 0.3048 m |
| **Area** | m² | ft² | 1 ft² = 0.092903 m² |
| **Mass** | kilogram (kg) | slug | 1 slug = 14.5939 kg |
| **Force** | Newton (N) | pound-force (lbf) | 1 lbf = 4.44822 N |
| **Pressure** | Pascal (Pa) | psf (lb/ft²) | 1 psf = 47.88 Pa |
| **Density** | kg/m³ | slug/ft³ | 1 slug/ft³ = 515.379 kg/m³ |
| **Velocity** | m/s | ft/s, knots | 1 ft/s = 0.3048 m/s; 1 kt = 0.5144 m/s |
| **Angular rate** | rad/s | deg/s, rpm | 1 deg/s = 0.017453 rad/s; 1 rpm = 0.10472 rad/s |
| **Angle** | radian | degree | 1 deg = 0.017453 rad; 1 rad = 57.2958 deg |
| **Moment of Inertia** | kg·m² | slug·ft² | 1 slug·ft² = 1.35582 kg·m² |
| **Dynamic Pressure** | Pa (N/m²) | psf (lb/ft²) | q = 0.5 * ρ * V² |

**Critical:**
- **Aerodynamic derivatives** are typically **per radian** (e.g., C_N_alpha = 4 /rad ≠ 4 /deg)
- **Dynamic pressure** q = 0.5 * ρ * V² → Units must match: [kg/m³] * [m/s]² = [Pa]
- **Moment coefficients** reference length differs: pitch uses chord/diameter, roll/yaw use span

## Common Patterns

### Pattern 1: Checking Units in Force Equation

```
Force equation:
  N = C_N * q * S_ref

Unit check:
  [N] = [dimensionless] * [Pa] * [m²]
  [N] = [dimensionless] * [N/m²] * [m²]  ✓ Units cancel correctly

If using Imperial:
  [lbf] = [dimensionless] * [psf] * [ft²]
  [lbf] = [dimensionless] * [lbf/ft²] * [ft²]  ✓

Common error:
  [lbf] = [dimensionless] * [Pa] * [m²]  ✗ Mixing SI pressure with Imperial force!
```

**When to use:** Before every calculation — make unit check a habit
**Watch out for:** Dynamic pressure q often stored in different units than expected

### Pattern 2: Converting Stability Derivatives (Degrees to Radians)

```
Aerodynamic tool outputs C_m_alpha in /rad:
  C_m_alpha = -10 /rad

If angle of attack in degrees:
  C_m = C_m_alpha * alpha  ✗ WRONG if alpha in degrees

Correct:
  C_m = C_m_alpha * (alpha * π/180)
  OR convert derivative:
  C_m_alpha_deg = C_m_alpha * (π/180) = -10 * 0.017453 = -0.1745 /deg

Then:
  C_m = C_m_alpha_deg * alpha  ✓ (alpha in degrees)
```

**When to use:** Anytime derivatives interface with flight code or spreadsheets
**Watch out for:** Some tools output both /rad and /deg versions — check file header

### Pattern 3: Reference Area Consistency

```
Typical reference area (cylindrical bodies):
  S_ref = π * D² / 4  (base area, circular cross-section)

CFD may use different reference:
  S_ref = wetted area  ✗ Different definition!
  S_ref = max cross-section  ✓ Usually same as base area

Flight code assumes:
  C_N = N / (q * S_ref)

If CFD used wetted area but flight code expects base area:
  C_N_flight = C_N_CFD * (S_wetted / S_base)  (scaling factor ~3-5 for missiles!)
```

**When to use:** Integrating aerodynamic data from multiple sources
**Watch out for:** ALWAYS verify S_ref definition in tool documentation

## ⚠️ WARNING

- **Degrees vs Radians in Derivatives** — Most aero derivatives (C_N_alpha, C_m_q, etc.) are **per radian**. If your flight code uses degrees for alpha, you MUST convert the derivative: C_N_alpha_deg = C_N_alpha_rad * (π/180). Missing this gives 57× error!
- **Reference Length for Moments** — Pitch moment uses L_ref (diameter or chord), roll/yaw use b (span). If you mix them, moment coefficients are wrong by factor of b/L_ref (can be 2-4×). Check tool input file.
- **Slugs vs Kilograms** — US aerodynamic tools often use slugs (Imperial mass unit). 1 slug = 14.59 kg. Confusing mass with weight causes √(g) ≈ 3.13× error in dynamic calculations.
- **Moment Reference Point (MRP)** — Aerodynamic coefficients (C_m, C_n, C_l) are valid only at the defined MRP. Moving MRP by Δx changes C_m by -C_N * Δx / L_ref. **Always document MRP location.**
- **Non-dimensional Rates** — Derivatives C_m_q, C_l_p, C_n_r use **non-dimensional rates**: q*c/2V, p*b/2V, r*b/2V. Don't forget the 2V divisor! Missing it gives 2V error (can be 100-1000×).
- **Base Pressure Coefficient** — Wind tunnel data reports C_p_base (pressure coefficient), not C_D_base (drag coefficient). Conversion: C_D_base = C_p_base * (A_base / S_ref). Confusing them gives wrong base drag.

## 📋 EXAMPLES

### Example 1: Detecting Degrees/Radians Error

**Problem:** Flight sim shows missile pitching 10° for 1° stick input. Expected 1:1 response.

**Investigation:**
```
Flight code:
  alpha_cmd = delta_stick  (in degrees)
  C_m = C_m_delta * delta_stick + C_m_alpha * alpha

Aero table loaded:
  C_m_alpha = -10 /rad  (per radian, as labeled)

Simulation alpha = 1°:
  C_m = C_m_delta * 1° + (-10) * 1
      = C_m_delta + (-10)  ✗ Treating 1° as 1 radian!

Correct:
  C_m = C_m_delta * 1° + (-10) * (1° * π/180)
      = C_m_delta + (-10) * 0.01745
      = C_m_delta - 0.1745  ✓
```

**Root cause:** Forgot to convert alpha from degrees to radians when using /rad derivative.

**Fix:** Add conversion: `alpha_rad = alpha_deg * 0.017453` before applying C_m_alpha.

### Example 2: Reference Area Mismatch

**Given:**
- Wind tunnel data: C_N_alpha = 2.5 /rad (referenced to S_ref = wetted area = 0.5 m²)
- Flight code expects: S_ref = base area = π*(0.2 m)²/4 = 0.0314 m²

**Problem:** Flight code computes normal force:
```
N = C_N * q * S_ref
  = 2.5 * alpha * 50000 Pa * 0.0314 m²
  = 3925 * alpha  [N]

But wind tunnel intended:
N = 2.5 * alpha * 50000 Pa * 0.5 m²
  = 62500 * alpha  [N]

Error factor: 62500 / 3925 = 15.9×  ✗ Huge underprediction!
```

**Fix:** Rescale coefficient to match reference area:
```
C_N_flight = C_N_WT * (S_ref_WT / S_ref_flight)
           = 2.5 * (0.5 / 0.0314)
           = 2.5 * 15.9
           = 39.8 /rad
```

Now: N = 39.8 * alpha * 50000 * 0.0314 = 62500 * alpha ✓

### Example 3: Dynamic Pressure Unit Trap

**Problem:** Flight dynamics code in SI units. Dynamic pressure from atmospheric model arrives as q = 1000 psf. Missile diameter D = 0.3 m, C_N_alpha = 4 /rad.

**Incorrect calculation:**
```
N = C_N_alpha * alpha * q * S_ref
  = 4 /rad * 0.1 rad * 1000 psf * (π * 0.3² / 4) m²
  = 0.4 * 1000 * 0.0707 m²
  = 28.3  [units unknown — wrong!]
```

**Correct:**
```
Convert q to SI:
  q = 1000 psf * 47.88 Pa/psf = 47880 Pa

N = 4 /rad * 0.1 rad * 47880 Pa * 0.0707 m²
  = 0.4 * 47880 * 0.0707
  = 1354 N  ✓
```

**Lesson:** Always convert to consistent unit system before calculation.

### Example 4: Moment Reference Point Shift

**Given:**
- Aerodynamic output: C_m_alpha = -8 /rad (about nose, X_ref = 0)
- Flight code needs C_m_alpha about CG at X_CG = 1.5 m
- Missile diameter D = 0.25 m (L_ref), C_N_alpha = 4 /rad

**Shift formula:**
```
C_m_alpha (about CG) = C_m_alpha (about nose) + C_N_alpha * (X_CG - X_nose) / L_ref

C_m_alpha_CG = -8 + 4 * (1.5 - 0) / 0.25
             = -8 + 4 * 6
             = -8 + 24
             = +16 /rad  ✗ POSITIVE → Unstable!
```

**Result:** Shifting MRP aft moved from stable (C_m_alpha = -8) to unstable (C_m_alpha = +16).

**Physical meaning:** CG is aft of CP → statically unstable configuration. Requires active control.

## Decision Guide

```
BEFORE every calculation:
  1. Write units next to every number
  2. Check unit consistency (all SI or all Imperial)
  3. Verify units cancel correctly in equation
  4. If mixing sources, convert to common unit system first

IF using aerodynamic derivative:
  Check: Is derivative /rad or /deg?
  IF /rad AND angle variable in degrees THEN
    Convert: derivative_deg = derivative_rad * (π/180)
  END IF

IF loading aero data from external source:
  Check: What is S_ref? (base area, wetted area, wing area?)
  Check: What is L_ref? (diameter, chord, body length?)
  Check: What is X_ref (MRP)? (nose, CG, fin leading edge?)
  Rescale coefficients if references differ from flight code

IF dynamic pressure from atmosphere model:
  Check: Units Pa or psf?
  Convert to match force equation unit system

IF calculation result seems wrong (off by 10×, 50×, 1000×):
  Suspect: Degrees/radians (57× error)
           Reference area mismatch (factor of A_wetted/A_base ≈ 3-10×)
           Missing 2V in non-dimensional rates (factor of 100-1000×)
```

## Related Cheatsheets

- `stability-derivatives.md` — Derivative units and non-dimensional rates
- `x-tail-configurations.md` — Fin numbering and sign conventions

## Sources

- AIAA G-003B-2010, "Guide for the Verification and Validation of Computational Fluid Dynamics Simulations"
- NASA-STD-7009A, "Standard for Models and Simulations" (2016) — Unit consistency requirements
- "Mars Climate Orbiter Mishap Investigation Board Phase I Report" (1999) — Unit conversion failure case study
- Failure case database: IEEE Xplore, "Software Engineering Disasters" collection

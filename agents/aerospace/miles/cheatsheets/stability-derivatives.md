---
topic: "Stability Derivatives Reference"
agent: "miles"
confidence: "TEXTBOOK"
source: "Etkin & Reid 'Dynamics of Flight' (1996), Stevens & Lewis 'Aircraft Control and Simulation' (2003)"
last_updated: "2026-02-18"
version: "1.0"
---

# Stability Derivatives Reference

> **One-line summary:** Definitions, sign conventions, and physical meanings of static and dynamic stability derivatives for missile flight dynamics — know what each derivative means and how to use it.

## Key Concepts

**Stability Derivatives:**
Partial derivatives of forces and moments with respect to state variables (alpha, beta, p, q, r) and control deflections. Linearize aerodynamic forces/moments about a trim condition.

**Sign Conventions (Body Axis):**
- **Forces:** X (forward), Y (right wing), Z (down)
- **Moments:** L (roll, right wing down positive), M (pitch, nose up positive), N (yaw, nose right positive)
- **Angular rates:** p (roll rate), q (pitch rate), r (yaw rate) — all right-hand rule
- **Angles:** alpha (angle of attack, positive nose up), beta (sideslip, positive nose right)

**Linearization:**
```
C_M = C_M0 + C_M_alpha * alpha + C_M_q * (q*c/2V) + C_M_delta_e * delta_e + ...

Where:
  C_M0 = trim pitching moment
  C_M_alpha = ∂C_M/∂alpha  (static stability)
  C_M_q = ∂C_M/∂(q*c/2V)  (pitch damping)
  C_M_delta_e = ∂C_M/∂delta_e  (control effectiveness)
```

## Quick Reference: Common Stability Derivatives

| Derivative | Definition | Physical Meaning | Typical Range (Missiles) | Stability Requirement |
|------------|------------|------------------|--------------------------|----------------------|
| **C_N_alpha** | ∂C_N/∂α | Normal force due to angle of attack | +2 to +8 /rad | Positive (always) |
| **C_m_alpha** | ∂C_m/∂α | Pitching moment due to AoA | -5 to -20 /rad | **Negative for static stability** |
| **C_Y_beta** | ∂C_Y/∂β | Side force due to sideslip | -0.5 to -2 /rad | Negative (weathercock) |
| **C_l_beta** | ∂C_l/∂β | Rolling moment due to sideslip (dihedral effect) | -0.1 to -0.5 /rad | Negative for lateral stability |
| **C_n_beta** | ∂C_n/∂β | Yawing moment due to sideslip (directional stability) | +0.05 to +0.3 /rad | **Positive for directional stability** |
| **C_l_p** | ∂C_l/∂(pb/2V) | Roll damping | -0.3 to -1.5 | Negative (damping) |
| **C_m_q** | ∂C_m/∂(qc/2V) | Pitch damping | -5 to -30 | Negative (damping) |
| **C_n_r** | ∂C_n/∂(rb/2V) | Yaw damping | -0.1 to -0.5 | Negative (damping) |
| **C_l_r** | ∂C_l/∂(rb/2V) | Roll due to yaw rate (coupling) | +0.05 to +0.3 | Positive (missiles) |
| **C_n_p** | ∂C_n/∂(pb/2V) | Yaw due to roll rate (coupling) | -0.01 to -0.1 | Negative (adverse yaw) |
| **C_m_alpha_dot** | ∂C_m/∂(α̇*c/2V) | Pitch moment due to alpha rate | -2 to -10 | Negative (stabilizing) |

**Note:** Dimensional derivatives use reference length: c (mean aerodynamic chord) for pitch, b (wingspan/span) for roll/yaw.

## Common Patterns

### Pattern 1: Static Margin from C_m_alpha

```
C_m_alpha = C_N_alpha * (x_CG - x_CP) / L_ref

Rearranging:
Static Margin = (x_CP - x_CG) / L_ref = -C_m_alpha / C_N_alpha

For missiles, typically express in calibers (diameters):
Static Margin [calibers] = -C_m_alpha / C_N_alpha  (if L_ref = D)

Typical values:
  - Unguided rockets: 1-2 calibers (passive stability)
  - Guided missiles: 0.5-2 calibers (active control available)
  - Unstable missiles (relaxed stability): -0.5 to 0 calibers
```

**When to use:** Preliminary sizing, CG/CP trades
**Watch out for:** Reference length must be consistent (diameter vs body length)

### Pattern 2: Pitch Damping Ratio Estimate

```
Pitch damping derivative C_m_q contributes to short-period damping:

ζ_sp ∝ -C_m_q / (2 * √(C_m_alpha * C_Z_alpha))

Where C_Z_alpha ≈ -C_N_alpha (body axis)

Missiles typically have ζ_sp = 0.4 to 0.8
Low damping → oscillatory response
High damping → sluggish response
```

**When to use:** Estimating transient response without full 6-DOF sim
**Watch out for:** Assumes classical short-period approximation; breaks down for very unstable or very flexible airframes

### Pattern 3: Roll-Yaw Coupling for X-Tail

```
For X-tail (cruciform fins rotated 45°):
C_l_beta ≈ 0  (symmetric)
C_n_p increases due to induced yaw from rolling fins

At alpha > 0:
  Roll command → Induced yaw moment (Dutch roll excitation)
  Magnitude: ΔC_n ≈ C_N_alpha * (L_fin/D_body) * sin(2*phi) * alpha
```

**When to use:** X-tail missiles with rolling airframe or bank-to-turn control
**Watch out for:** Coupling grows with alpha; can cause limit cycles at high alpha

## ⚠️ WARNING

- **C_m_alpha MUST be negative for static stability** — Positive C_m_alpha means unstable (divergent pitch). If your analysis gives positive C_m_alpha, either CG is aft of CP (unstable) or there's a sign error.
- **C_n_beta MUST be positive for directional stability** — Negative C_n_beta means "fishtailing" instability. Common error: confusing body-axis beta (positive = nose right) with wind-axis beta.
- **Dimensional vs non-dimensional rates** — Derivatives C_m_q, C_l_p, C_n_r are w.r.t. NON-DIMENSIONAL rates (q*c/2V, p*b/2V, r*b/2V). Don't forget the 2V normalization.
- **Reference point for moments** — Derivatives are valid only at the reference point (typically nose or CG). Moving CG changes C_m_alpha linearly: ΔC_m_alpha = -C_N_alpha * Δx_CG / L_ref
- **Nonlinear effects at high alpha** — Derivatives are linear approximations. Above 15-20° alpha, vortex shedding, fin stall, and body-fin interactions cause derivatives to vary strongly with alpha. Use nonlinear lookup tables.
- **Compressibility effects** — Derivatives change with Mach number. Transonic region (M = 0.8-1.2) can show rapid variations (e.g., C_N_alpha peaks near Mach 1). Always plot derivatives vs Mach.

## 📋 EXAMPLES

### Example 1: Checking Static Stability

**Given:**
- Aerodynamic analysis output: C_N_alpha = +4.2 /rad, C_m_alpha = -8.4 /rad (about nose)
- Body diameter D = 0.25 m, length L = 2.5 m
- CG location x_CG = 1.2 m from nose

**Check static margin:**
```
Static margin = -C_m_alpha / C_N_alpha = -(-8.4) / 4.2 = 2.0 (dimensionless)

If L_ref = D = 0.25 m:
  Static margin = 2.0 calibers = 0.5 m

Center of Pressure:
  x_CP = x_CG + (Static margin * L_ref) = 1.2 + 0.5 = 1.7 m from nose
```

**Result:** CP is 0.5 m aft of CG → statically stable. Typical for tail-controlled missile.

**Validation:** CP at 68% of body length — reasonable for finned missile.

### Example 2: Estimating Roll Damping

**Given:**
- Missile with four fins, span b = 0.5 m
- Aerodynamic prediction: C_l_p = -0.6
- Flight condition: V = 300 m/s, dynamic pressure q = 50 kPa

**Estimate roll time constant:**
```
Roll equation (simplified):
  I_x * p_dot = L = (1/2) * rho * V² * S_ref * b * C_l_p * (p*b/2V)

Roll time constant:
  tau_roll = -I_x / ((1/2) * rho * V * S_ref * b² * C_l_p)

For typical missile I_x = 5 kg·m², S_ref = 0.05 m²:
  tau_roll = -5 / (0.5 * 1.225 * 300 * 0.05 * 0.25 * (-0.6))
           ≈ 0.18 seconds

Roll bandwidth ≈ 1/tau_roll ≈ 5.6 rad/s
```

**Result:** Fast roll response (time to 63% of commanded roll rate ≈ 0.18 sec)

### Example 3: Identifying Sign Error

**Problem:** CFD output shows C_n_beta = -0.15 /rad for a conventional tail-finned missile at Mach 0.8. Is this correct?

**Analysis:**
- C_n_beta should be POSITIVE for directional stability (weathercock effect)
- Negative C_n_beta → unstable in yaw (nose points away from relative wind)
- Possible causes:
  1. **Sign convention error** — CFD uses different beta definition (positive = nose left?)
  2. **Moment reference point error** — Computed about wrong location
  3. **Destabilizing body or fin configuration** — Unlikely for conventional missile

**Action:** Check CFD beta sign convention. Likely answer: CFD uses wind-axis beta (opposite sign from body-axis). Flip sign.

## Decision Guide

```
IF |C_m_alpha| / C_N_alpha < 0.2 THEN
  Static margin < 0.2 calibers → Borderline stable; requires active control
ELIF C_m_alpha > 0 THEN
  **UNSTABLE** — Check CG location or sign convention error
ELIF C_m_alpha < 0 AND static margin > 0.5 calibers THEN
  Statically stable; benign handling (may be sluggish)
END IF

IF C_n_beta < 0 THEN
  **Check sign convention** — Should be positive for stable missile
END IF

IF |C_m_q| < 5 THEN
  Low pitch damping → Lightly damped short-period mode
  Watch for PIO (pilot-induced oscillation) in manual control
END IF

IF alpha > 20° THEN
  Linear derivatives invalid → Use nonlinear tables or polynomial fits
END IF
```

## Related Cheatsheets

- `x-tail-configurations.md` — Roll-yaw coupling derivatives for X-tail
- `common-unit-pitfalls.md` — Reference length and non-dimensional rate pitfalls

## Sources

- Etkin, B. & Reid, L.D., "Dynamics of Flight: Stability and Control" (1996, 3rd ed.)
- Stevens, B.L. & Lewis, F.L., "Aircraft Control and Simulation" (2003, 2nd ed.)
- Zipfel, P.H., "Modeling and Simulation of Aerospace Vehicle Dynamics" (2007, 2nd ed.)
- Blakelock, J.H., "Automatic Control of Aircraft and Missiles" (1991, 2nd ed.)

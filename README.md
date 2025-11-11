# Active Matter Simulation: Vicsek Model with Vision Cone 

## Project Overview

This repository contains a C++ implementation of an active matter simulation combining the **Vicsek flocking model** The simulation explores how restricted visual perception (vision cone) and particle interactions affect collective behavior, clustering dynamics, and phase transitions in active systems.

### Key Physics

The model simulates N self-propelled particles that:
- Move at constant speed v₀ (active motion)
- Align velocities with visible neighbors (Vicsek mechanism)
- Undergo rotational diffusion (uniform scalar noise)

---

## Novel Features

###  Vision Cone (Non-Reciprocal Interactions)

**Standard Vicsek:** Particles align with ALL neighbors within radius R.

**This Implementation:** Particles only align with neighbors in their **forward vision cone**.

**Mechanism:**
- Agent i includes agent j in alignment if:
  - Distance: |rᵢ - rⱼ| < R_align
  - Angular constraint: vᵢ · n̂ᵢⱼ ≥ cos(α)
  
  where n̂ᵢⱼ = (rⱼ - rᵢ)/|rⱼ - rᵢ| and α is the half-angle of the vision cone.

**Physical Significance:**
- Models realistic animal perception (limited field of view)
- Creates **non-reciprocal interactions**: i sees j ≠ j sees i
- Frustrates global ordering, promoting local clustering
- α → π recovers standard Vicsek model


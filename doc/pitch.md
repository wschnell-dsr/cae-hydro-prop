# Propeller Pitch Distribution: Variants and Parameterizations

---

## **1. Fundamentals**
The **pitch distribution** defines how the **blade angle** $\theta$ of a propeller varies along the radius $r$. It is critical for:
- **Efficiency** (thrust per unit of power input),
- **Noise emission**,
- **Vibration levels**,
- **Performance characteristics** (e.g., acceleration vs. top speed).

---

## **2. Key Radii and Reference Points**
| Term                  | Symbol       | Description                                                                                     | Typical Values (Example)       |
|-----------------------|--------------|-------------------------------------------------------------------------------------------------|----------------------------------|
| **Hub radius**        | $r_{\text{hub}}$ | Smallest radius (near the hub).                                                               | 0.2–0.3 m (aircraft propeller)  |
| **Reference radius**  | $r_{\text{ref}}$  | Typically **70%–75% of the blade length**, where the **pitch** is defined.                     | 0.7–0.75 m                       |
| **Tip radius**        | $r_{\text{tip}}$  | Largest radius (blade tip).                                                                    | 1.0–1.5 m (aircraft propeller)  |

---

## **3. Variants of Pitch Distribution**

### **3.1 Linear Pitch Distribution**
**Description**:
The blade angle decreases linearly from the hub radius to the tip.

**Mathematical Formulation**:
$$\theta(r) = \theta_{\text{hub}} - \left( \frac{\theta_{\text{hub}} - \theta_{\text{tip}}}{r_{\text{tip}} - r_{\text{hub}}} \right) \cdot (r - r_{\text{hub}})$$

**Parameters**:
- $\theta_{\text{hub}}$: Blade angle at the hub (e.g., $40^\circ$).
- $\theta_{\text{tip}}$: Blade angle at the tip (e.g., $20^\circ$).

**Advantages**:
- Simple to calculate and manufacture.
- Low effort for prototyping.

**Disadvantages**:
- Not optimal for high efficiency or low noise.

**Typical Applications**:
- Drone propellers,
- Simple industrial propellers,
- Educational models.

---

### **3.2 Non-Linear Pitch Distributions**

#### **a) Quadratic Distribution**
**Description**:
The blade angle decreases quadratically.

**Mathematical Formulation**:
$$\theta(r) = \theta_{\text{hub}} - k \cdot (r - r_{\text{hub}})^2$$

**Parameters**:
- $k$: Constant for curvature (e.g., $k = 10$).

**Advantages**:
- Better adaptation to aerodynamic requirements.
- Lower noise emission than linear distribution.

**Disadvantages**:
- More complex to calculate.

**Typical Applications**:
- Aircraft propellers (mid-performance range),
- Wind turbines.

---
#### **b) Exponential Distribution**
**Description**:
The blade angle decreases exponentially.

**Mathematical Formulation**:
$$\theta(r) = \theta_{\text{hub}} \cdot e^{-k \cdot (r - r_{\text{hub}})}$$

**Parameters**:
- $k$: Decay constant (e.g., $k = 2$).

**Advantages**:
- Very smooth transition,
- Optimized for high speeds.

**Disadvantages**:
- More complex manufacturing.

**Typical Applications**:
- High-performance aircraft propellers,
- Racing boat propellers.

---
#### **c) Cubic Distribution**
**Description**:
The blade angle follows a cubic function.

**Mathematical Formulation**:
$$\theta(r) = \theta_{\text{hub}} - k_1 \cdot (r - r_{\text{hub}}) - k_2 \cdot (r - r_{\text{hub}})^3$$

**Parameters**:
- $k_1, k_2$: Adjustable constants.

**Advantages**:
- High flexibility for complex requirements.

**Disadvantages**:
- Very complex.

**Typical Applications**:
- Specialized propellers (e.g., for submarines or racing vehicles).

---

### **3.3 Optimized Pitch Distributions**

#### **a) Betz Optimization**
**Description**:
Based on the **optimal vorticity distribution** by Albert Betz (1919). Aims for **maximum energy extraction** from the fluid flow.

**Simplified Mathematical Formulation**:
$$\theta(r) = \arctan\left(\frac{v_{\text{axial}} \cdot (1 - a)}{v_{\text{tangential}} \cdot (1 + a')}\right)$$

**Parameters**:
- $a$: Axial induction factor,
- $a'$: Tangential induction factor,
- $v_{\text{axial}}$: Axial flow velocity,
- $v_{\text{tangential}}$: Tangential flow velocity.

**Advantages**:
- Maximum efficiency for wind turbines and propellers.

**Disadvantages**:
- Requires computational fluid dynamics (CFD) simulations.

**Typical Applications**:
- Wind turbines,
- Large ship propellers.

---
#### **b) Glauert Optimization**
**Description**:
Optimized for **compressible flow** (e.g., aircraft propellers). Based on the work of Hermann Glauert (1930s).

**Simplified Mathematical Formulation**:
$$\theta(r) = \theta_0 \cdot \frac{1 - a}{1 - a + \frac{a}{\cos^2(\phi(r))}}$$

**Parameters**:
- $\phi(r)$: Local inflow angle,
- $\theta_0$: Reference angle.

**Advantages**:
- Optimized for high speeds (e.g., supersonic propellers).

**Disadvantages**:
- Very complex.

**Typical Applications**:
- High-performance aircraft propellers,
- Propellers for military aircraft.

---

### **3.4 Combined Approaches**
**Description**:
Combination of pitch distribution with other geometric adjustments (e.g., **skew** or **twist**).

**Examples**:
- **Skew-Twist Design** (for ship propellers):
  - **Skew**: Blade rake to reduce cavitation and noise.
  - **Twist**: Pitch distribution for optimal efficiency.

- **Constant Speed Propeller** (for aircraft):
  - Pitch distribution optimized for efficiency across various rotational speeds.

**Typical Applications**:
- Large ship propellers,
- Variable-pitch propellers for aircraft.

---

## **4. Typical Values for Pitch Distributions**
| Propeller Type           | $\theta_{\text{hub}}$ | $\theta_{\text{tip}}$ | Typical Distribution          |
|--------------------------|---------------------------|---------------------------|-------------------------------|
| **Aircraft Propeller**   | $30^\circ$–$50^\circ$ | $10^\circ$–$25^\circ$ | Non-linear (exponential)     |
| **Ship Propeller**       | $20^\circ$–$40^\circ$ | $5^\circ$–$15^\circ$  | Linear or quadratic           |
| **Wind Turbine Propeller** | $10^\circ$–$30^\circ$ | $0^\circ$–$5^\circ$   | Betz Optimization             |
| **Drone Propeller**      | $20^\circ$–$40^\circ$ | $10^\circ$–$20^\circ$ | Linear or progressive         |
| **Racing Boat Propeller** | $35^\circ$–$55^\circ$ | $15^\circ$–$30^\circ$ | Exponential or cubic          |

---

## **5. Tools for Calculation and Visualization**
| Tool               | Description                                                                                     | Link/Website                     |
|--------------------|-------------------------------------------------------------------------------------------------|-----------------------------------|
| **QBlade**         | Open-source software for propeller and wind turbine design.                                    | [qblade.org](https://qblade.org)  |
| **OpenProp**       | Calculation of ship propellers with optimized pitch distribution.                              | [openprop.org](https://openprop.org) |
| **XFOIL**          | Aerodynamic analysis of airfoils (can be adapted for propeller blades).                        | [xfoil.mit.edu](https://xfoil.mit.edu) |
| **RANS-CFD**       | Computational fluid dynamics for detailed optimization.                                        | (e.g., OpenFOAM, ANSYS Fluent)    |
| **Propeller Design Software** | Commercial tools from manufacturers like MT-Propeller or Hartzell.                              | Manufacturer websites            |

---
## **6. Practical Tips for Selection**
1. **Simple Applications** (e.g., drones):
   - Choose a **linear or progressive pitch distribution**.
2. **High Efficiency** (e.g., wind turbines):
   - Use **Betz Optimization** or **Glauert Optimization**.
3. **Noise Reduction** (e.g., ship propellers):
   - Combine **skew-twist design**.
4. **High-Performance Applications** (e.g., racing boats):
   - Opt for **exponential or cubic distributions**.

---
## **7. Further Reading**
- Betz, A. (1919). *Das Maximum der theoretisch möglichen Ausnutzung des Windes durch Windmotoren*.
- Glauert, H. (1935). *Aerodynamic Theory*.
- Leishman, J. G. (2006). *Principles of Helicopter Aerodynamics*.
- Carlton, J. (2012). *Marine Propellers and Propulsion*.

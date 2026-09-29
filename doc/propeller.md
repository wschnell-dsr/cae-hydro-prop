# Propeller parameter

## Basic propeller parameter

| **Parameter**          | **Symbol** | **Unit** | Description                                |
| **Rotational speed**   | $n$        | U/s      | Rotational speed of the propeller          |
| **Pitch**              | $P$        | m        | Pitch of the propeller                     |
| **Chord**              | $c$        | m        | Chord length of a propeller blade          |
| **Diameter**           | $D$        | m        | Diameter of the propeller                  |
| **Number of blades**   | $Z$        | -        | Number of propeller blades                 |
| **Advance rate**       | $J$        | -        | Advance rate for one turn                  |
| **Thrust coefficient** | $ K_T $    | -        | Dimension less coefficient for the thrust  |
| **Torque coefficient** | $K_Q$      | -        | Dimension less coefficient for the torque  |
| **Efficiency**         | $\eta$     | -        | Hydrodynamic Efficency                     |

## Formulas for propeller

### Advance rate (J)
The **advance rate** $J$ is the relation between axial fluid velocity $V_A$  and tip speed

$$
J = \frac{V_A}{n \cdot D}
$$

- $V_A$: axial fluid velocity (m/s)
- $n$: frquency (U/s)
- $D$: diameter (m)


### Thrust coefficient (K_T)
THe **thrust coefficient** $K_T$ is the dimensionless expression for the thrust $T$

$$
K_T = \frac{T}{\rho \cdot n^2 \cdot D^4}
$$

- $T$: Schub (N)
- $\rho$: Dichte des Wassers (1000 kg/m³)
- $n$: Drehzahl (U/s)
- $D$: Propellerdurchmesser (m)

**Umgestellt nach Schub:**
\[
T = K_T \cdot \rho \cdot n^2 \cdot D^4
\]



### 2.3 Drehmomentkoeffizient (K_Q)
Der **Drehmomentkoeffizient** $K_Q$ beschreibt das benötigte Drehmoment $Q$ in dimensionsloser Form:

\[
K_Q = \frac{Q}{\rho \cdot n^2 \cdot D^5}
\]

- $Q$: Drehmoment (Nm)
- $\rho$: Dichte des Wassers (1000 kg/m³)
- $n$: Drehzahl (U/s)
- $D$: Propellerdurchmesser (m)


**Umgestellt nach Drehmoment:**
\[
Q = K_Q \cdot \rho \cdot n^2 \cdot D^5
\]



### 2.4 Schub (T)
Der Schub $T$ kann direkt aus $K_T$ berechnet werden:

\[
T = K_T \cdot \rho \cdot n^2 \cdot D^4
\]



### 2.5 Drehmoment (Q)
Das benötigte Drehmoment $Q$ berechnet sich aus $K_Q$:

\[
Q = K_Q \cdot \rho \cdot n^2 \cdot D^5
\]



### 2.6 Leistung (P)
Die **Leistung** $P$, die der Propeller benötigt, berechnet sich aus dem Drehmoment $Q$ und der Winkelgeschwindigkeit $\omega$:

\[
P = Q \cdot \omega = Q \cdot 2 \pi n
\]

Einsetzen von $Q$:

\[
P = 2 \pi \cdot K_Q \cdot \rho \cdot n^3 \cdot D^5
\]



### 2.7 Wirkungsgrad (η)
Der **Wirkungsgrad** $\eta$ des Propellers ist das Verhältnis zwischen der **nutzbaren Leistung** (Schubleistung) und der **zugeführten Leistung**:

\[
\eta = \frac{T \cdot V_A}{P} = \frac{K_T \cdot J}{2 \pi \cdot K_Q}
\]

- $T \cdot V_A$: Nutzbare Schubleistung (W)
- $P$: Zugeführte Leistung (W)


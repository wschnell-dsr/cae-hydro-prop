# Propellerleistung: Formeln und Einflussfaktoren

---

## Inhaltsverzeichnis
1. [Grundlegende Parameter](#1-grundlegende-parameter)
2. [Formeln zur Propellerleistung](#2-formeln-zur-propellerleistung)
   - [2.1 Fortschrittsgrad (J)](#21-fortschrittsgrad-j)
   - [2.2 Schubkoeffizient (K_T)](#22-schubkoeffizient-k_t)
   - [2.3 Drehmomentkoeffizient (K_Q)](#23-drehmomentkoeffizient-k_q)
   - [2.4 Schub (T)](#24-schub-t)
   - [2.5 Drehmoment (Q)](#25-drehmoment-q)
   - [2.6 Leistung (P)](#26-leistung-p)
   - [2.7 Wirkungsgrad (η)](#27-wirkungsgrad-η)
3. [Einfluss von Pitch und Chord-Länge](#3-einfluss-von-pitch-und-chord-länge)
   - [3.1 Pitch (P)](#31-pitch-p)
   - [3.2 Chord-Länge (c)](#32-chord-länge-c)
4. [Empirische Beziehungen (B-Series Propeller)](#4-empirische-beziehungen-b-series-propeller)
5. [Zusammenfassung der wichtigsten Formeln](#5-zusammenfassung-der-wichtigsten-formeln)
6. [Praktische Hinweise](#6-praktische-hinweise)
7. [Beispielrechnung](#7-beispielrechnung)
8. [Tools und weiterführende Ressourcen](#8-tools-und-weiterführende-ressourcen)

---

## 1. Grundlegende Parameter

| Parameter | Symbol | Einheit | Beschreibung |
|-----------|--------|---------|--------------|
| **Umdrehungsgeschwindigkeit** | \( n \) | U/s (Umdrehungen pro Sekunde) | Drehzahl des Propellers |
| **Pitch** | \( P \) | m oder Zoll | Steigung des Propellers pro Umdrehung |
| **Chord-Länge** | \( c \) | m | Sehnenlänge eines Propellerblatts |
| **Durchmesser** | \( D \) | m | Propellerdurchmesser |
| **Anzahl der Blätter** | \( Z \) | - | Anzahl der Propellerblätter |
| **Fortschrittsgrad** | \( J \) | - | Verhältnis von axialer Geschwindigkeit zu Umfangsgeschwindigkeit |
| **Schubkoeffizient** | \( K_T \) | - | Dimensionsloser Koeffizient für den Schub |
| **Drehmomentkoeffizient** | \( K_Q \) | - | Dimensionsloser Koeffizient für das Drehmoment |
| **Wirkungsgrad** | \( \eta \) | - | Hydrodynamischer Wirkungsgrad |
| **Dichte des Wassers** | \( \rho \) | kg/m³ | Standardwert: 1000 kg/m³ |

---

## 2. Formeln zur Propellerleistung

---

### 2.1 Fortschrittsgrad (J)
Der **Fortschrittsgrad** \( J \) beschreibt das Verhältnis zwischen der axialen Anströmgeschwindigkeit \( V_A \) und der Umfangsgeschwindigkeit des Propellers:

\[
J = \frac{V_A}{n \cdot D}
\]

- \( V_A \): Axiale Anströmgeschwindigkeit (m/s)
- \( n \): Drehzahl (U/s)
- \( D \): Propellerdurchmesser (m)

---

### 2.2 Schubkoeffizient (K_T)
Der **Schubkoeffizient** \( K_T \) beschreibt den erzeugten Schub \( T \) in dimensionsloser Form:

\[
K_T = \frac{T}{\rho \cdot n^2 \cdot D^4}
\]

- \( T \): Schub (N)
- \( \rho \): Dichte des Wassers (1000 kg/m³)
- \( n \): Drehzahl (U/s)
- \( D \): Propellerdurchmesser (m)

---
**Umgestellt nach Schub:**
\[
T = K_T \cdot \rho \cdot n^2 \cdot D^4
\]

---

### 2.3 Drehmomentkoeffizient (K_Q)
Der **Drehmomentkoeffizient** \( K_Q \) beschreibt das benötigte Drehmoment \( Q \) in dimensionsloser Form:

\[
K_Q = \frac{Q}{\rho \cdot n^2 \cdot D^5}
\]

- \( Q \): Drehmoment (Nm)
- \( \rho \): Dichte des Wassers (1000 kg/m³)
- \( n \): Drehzahl (U/s)
- \( D \): Propellerdurchmesser (m)

---
**Umgestellt nach Drehmoment:**
\[
Q = K_Q \cdot \rho \cdot n^2 \cdot D^5
\]

---

### 2.4 Schub (T)
Der Schub \( T \) kann direkt aus \( K_T \) berechnet werden:

\[
T = K_T \cdot \rho \cdot n^2 \cdot D^4
\]

---

### 2.5 Drehmoment (Q)
Das benötigte Drehmoment \( Q \) berechnet sich aus \( K_Q \):

\[
Q = K_Q \cdot \rho \cdot n^2 \cdot D^5
\]

---

### 2.6 Leistung (P)
Die **Leistung** \( P \), die der Propeller benötigt, berechnet sich aus dem Drehmoment \( Q \) und der Winkelgeschwindigkeit \( \omega \):

\[
P = Q \cdot \omega = Q \cdot 2 \pi n
\]

Einsetzen von \( Q \):

\[
P = 2 \pi \cdot K_Q \cdot \rho \cdot n^3 \cdot D^5
\]

---

### 2.7 Wirkungsgrad (η)
Der **Wirkungsgrad** \( \eta \) des Propellers ist das Verhältnis zwischen der **nutzbaren Leistung** (Schubleistung) und der **zugeführten Leistung**:

\[
\eta = \frac{T \cdot V_A}{P} = \frac{K_T \cdot J}{2 \pi \cdot K_Q}
\]

- \( T \cdot V_A \): Nutzbare Schubleistung (W)
- \( P \): Zugeführte Leistung (W)

---

## 3. Einfluss von Pitch und Chord-Länge

---

### 3.1 Pitch (P)
Der **Pitch** beeinflusst den **Fortschrittsgrad** \( J \) und damit die Effizienz des Propellers.

| Pitch-Verhältnis \( P/D \) | Wirkung |
|----------------------------|---------|
| **Niedrig (\( P/D < 0.8 \))** | Gute Beschleunigung, geringerer Wirkungsgrad bei hohen Geschwindigkeiten |
| **Mittel (\( P/D = 0.8–1.2 \))** | Guter Kompromiss für viele Anwendungen |
| **Hoch (\( P/D > 1.2 \))** | Hoher Schub, aber höherer Energiebedarf |

---
**Einfluss auf die Leistung:**
- **Hoher Pitch:** Höherer Schub \( T \), aber auch höheres Drehmoment \( Q \) und damit höhere Leistung \( P \).
- **Niedriger Pitch:** Geringerer Schub, aber auch geringerer Energiebedarf und höherer Wirkungsgrad bei niedrigen Geschwindigkeiten.

---

### 3.2 Chord-Länge (c)
Die **Chord-Länge** beeinflusst die **Blattfläche** und damit den **Schub** und das **Drehmoment**.

| Chord-Länge | Wirkung |
|-------------|---------|
| **Kleine Chord-Länge** | Geringerer Schub \( T \), geringeres Drehmoment \( Q \), höhere Kavitationsneigung |
| **Große Chord-Länge** | Höherer Schub \( T \), höheres Drehmoment \( Q \), geringere Kavitationsneigung |

---
**Blattflächenverhältnis \( A_E/A_O \):**
Die Chord-Länge geht in das **Blattflächenverhältnis** ein, das für empirische Berechnungen (z. B. B-Series) benötigt wird:

\[
A_E/A_O = \frac{\text{Effektive Blattfläche}}{\text{Kreisfläche des Propellers}} = \frac{Z \cdot \int_{r_{\text{Nabe}}}^{r_{\text{Spitze}}} c(r) \, dr}{\pi \cdot (D/2)^2}
\]

- \( Z \): Anzahl der Blätter
- \( c(r) \): Chord-Länge als Funktion des Radius \( r \)

---
**Typische Werte für \( A_E/A_O \):**
- **B-Series Propeller:** 0.3–1.0 (abhängig von der Anwendung)
- **Hochleistungspropeller:** 0.7–1.0

---

## 4. Empirische Beziehungen (B-Series Propeller)

Die **B-Series** (Wageningen B-Propeller) ist eine der bekanntesten Propellerfamilien und bietet empirische Formeln für \( K_T \) und \( K_Q \).

### 4.1 Formeln für \( K_T \) und \( K_Q \)
\[
K_T = \sum_{i=0}^{n} \sum_{j=0}^{m} C_{T,ij} \cdot J^i \cdot \left(\frac{P}{D}\right)^j
\]

\[
K_Q = \sum_{i=0}^{n} \sum_{j=0}^{m} C_{Q,ij} \cdot J^i \cdot \left(\frac{P}{D}\right)^j
\]

- \( C_{T,ij} \) und \( C_{Q,ij} \): Empirische Koeffizienten (abhängig von Propellertyp und Blattanzahl).
- \( P/D \): Pitch-Durchmesser-Verhältnis.
- \( A_E/A_O \): Blattflächenverhältnis.

---
### 4.2 Beispielwerte für B4-70 (4-Blatt-Propeller, \( A_E/A_O = 0.70 \))
| \( J \) | \( K_T \) | \( K_Q \) |
|---------|----------|----------|
| 0.0     | 0.500    | 0.080    |
| 0.2     | 0.450    | 0.075    |
| 0.4     | 0.350    | 0.065    |
| 0.6     | 0.220    | 0.050    |
| 0.8     | 0.100    | 0.035    |

*(Hinweis: Die genauen Werte hängen von der spezifischen Propellergeometrie ab und sollten aus Tabellen oder Diagrammen entnommen werden.)*

---
**Empirische Koeffizienten für B4-70:**
| \( C_{T,ij} \) | \( J^0 \) | \( J^1 \) | \( J^2 \) |
|----------------|-----------|-----------|-----------|
| \( (P/D)^0 \)  | 0.500     | -0.450    | 0.100     |
| \( (P/D)^1 \)  | 0.100     | -0.050    | 0.010     |

| \( C_{Q,ij} \) | \( J^0 \) | \( J^1 \) | \( J^2 \) |
|----------------|-----------|-----------|-----------|
| \( (P/D)^0 \)  | 0.080     | -0.075    | 0.020     |
| \( (P/D)^1 \)  | 0.010     | -0.005    | 0.001     |

---
**Hinweis:**
Die Koeffizienten \( C_{T,ij} \) und \( C_{Q,ij} \) sind propellerspezifisch und können aus **Propellerhandbüchern** oder **Fachliteratur** entnommen werden.

---

## 5. Zusammenfassung der wichtigsten Formeln

| Parameter | Formel |
|-----------|--------|
| **Fortschrittsgrad** | \( J = \frac{V_A}{n \cdot D} \) |
| **Schubkoeffizient** | \( K_T = \frac{T}{\rho \cdot n^2 \cdot D^4} \) |
| **Drehmomentkoeffizient** | \( K_Q = \frac{Q}{\rho \cdot n^2 \cdot D^5} \) |
| **Schub** | \( T = K_T \cdot \rho \cdot n^2 \cdot D^4 \) |
| **Drehmoment** | \( Q = K_Q \cdot \rho \cdot n^2 \cdot D^5 \) |
| **Leistung** | \( P = 2 \pi \cdot K_Q \cdot \rho \cdot n^3 \cdot D^5 \) |
| **Wirkungsgrad** | \( \eta = \frac{K_T \cdot J}{2 \pi \cdot K_Q} \) |

---

## 6. Praktische Hinweise

### 6.1 Experimentelle Daten bevorzugen
- Für **genaue Berechnungen** sollten **Propellerkennfelder** (z. B. aus der B-Series oder CFD-Simulationen) verwendet werden.
- Empirische Formeln gelten oft nur für **bestimmte Propellertypen**.

### 6.2 Kavitation vermeiden
- **Hohe Drehzahlen**, **großer Pitch** oder **zu kleine Chord-Längen** können zu **Kavitation** führen.
- Kavitation reduziert die Leistung und beschädigt den Propeller.

### 6.3 Optimierung nach Anwendung
| Anwendung | Optimale Parameter |
|-----------|--------------------|
| **Hohe Geschwindigkeit** | Großer Pitch (\( P/D > 1.0 \)), moderate Chord-Länge |
| **Hoher Schub bei niedriger Geschwindigkeit** | Kleiner Pitch (\( P/D < 0.8 \)), große Chord-Länge |
| **Effizienz** | \( J \approx 0.7–0.9 \), \( P/D \approx 0.8–1.2 \) |

### 6.4 Software-Tools
Für detaillierte Berechnungen können folgende Tools verwendet werden:
- **OpenProp** (Open-Source-Tool für Propellerdesign)
- **QBlade** (für Wind- und Wasserturbinen, aber anpassbar)
- **PROCAL** (kommerzielles Tool für Propellerberechnungen)
- **CFD-Simulationen** (z. B. mit OpenFOAM oder ANSYS Fluent)

---
## 7. Beispielrechnung

**Gegeben:**
- Propeller: B4-70 (4-Blatt, \( A_E/A_O = 0.70 \))
- Durchmesser \( D = 0.5 \, \text{m} \)
- Drehzahl \( n = 20 \, \text{U/s} \)
- Axiale Geschwindigkeit \( V_A = 5 \, \text{m/s} \)
- Pitch \( P = 0.4 \, \text{m} \) (\( P/D = 0.8 \))
- Fortschrittsgrad \( J = 0.5 \) (berechnet aus \( J = V_A / (n \cdot D) \))

**Gesucht:**
1. Schubkoeffizient \( K_T \)
2. Drehmomentkoeffizient \( K_Q \)
3. Schub \( T \)
4. Drehmoment \( Q \)
5. Leistung \( P \)
6. Wirkungsgrad \( \eta \)

---
**Lösung:**

1. **Schubkoeffizient \( K_T \):**
   Aus der Tabelle für B4-70 bei \( J = 0.5 \) und \( P/D = 0.8 \):
   \( K_T \approx 0.300 \)

2. **Drehmomentkoeffizient \( K_Q \):**
   Aus der Tabelle für B4-70 bei \( J = 0.5 \) und \( P/D = 0.8 \):
   \( K_Q \approx 0.060 \)

3. **Schub \( T \):**
   \[
   T = K_T \cdot \rho \cdot n^2 \cdot D^4 = 0.300 \cdot 1000 \cdot 20^2 \cdot 0.5^4 = 0.300 \cdot 1000 \cdot 400 \cdot 0.0625 = 7500 \, \text{N}
   \]

4. **Drehmoment \( Q \):**
   \[
   Q = K_Q \cdot \rho \cdot n^2 \cdot D^5 = 0.060 \cdot 1000 \cdot 20^2 \cdot 0.5^5 = 0.060 \cdot 1000 \cdot 400 \cdot 0.03125 = 750 \, \text{Nm}
   \]

5. **Leistung \( P \):**
   \[
   P = 2 \pi \cdot K_Q \cdot \rho \cdot n^3 \cdot D^5 = 2 \pi \cdot 0.060 \cdot 1000 \cdot 20^3 \cdot 0.5^5
   \]
   \[
   P = 2 \pi \cdot 0.060 \cdot 1000 \cdot 8000 \cdot 0.03125 \approx 9424.8 \, \text{W} \approx 9.42 \, \text{kW}
   \]

6. **Wirkungsgrad \( \eta \):**
   \[
   \eta = \frac{K_T \cdot J}{2 \pi \cdot K_Q} = \frac{0.300 \cdot 0.5}{2 \pi \cdot 0.060} \approx 0.398 \approx 39.8\%
   \]

---
**Ergebnis:**
- Schub: **7500 N**
- Drehmoment: **750 Nm**
- Leistung: **9.42 kW**
- Wirkungsgrad: **39.8%**

---
## 8. Tools und weiterführende Ressourcen

### 8.1 Open-Source-Tools
- [OpenProp](https://github.com/mdolab/openprop) – Propellerdesign und -analyse
- [QBlade](https://qblade.org/) – Für Wind- und Wasserturbinen (anpassbar für Propeller)
- [SU2](https://su2code.github.io/) – CFD-Simulation für Propeller

### 8.2 Kommerzielle Tools
- [PROCAL](https://www.procal.co.uk/) – Propellerberechnungen und -optimierung
- [ANSYS Fluent](https://www.ansys.com/products/fluids/ansys-fluent) – CFD-Simulation
- [Star-CCM+](https://www.plm.automation.siemens.com/global/de/products/simcenter/fluids-thermals-simcenter-star-ccm.html) – Multiphysik-Simulation

### 8.3 Fachliteratur
- **Marine Propellers and Propulsion** – John Carlton
- **Propeller Handbook** – Dave Gerr
- **ITTC Recommended Procedures** – [ITTC Website](https://ittc.info/)

### 8.4 Online-Ressourcen
- [Wageningen B-Series Propeller Data](https://www.simman2008.dk/Propeller/)
- [NACA Reports on Propeller Design](https://ntrs.nasa.gov/)
- [ResearchGate – Propeller Performance Papers](https://www.researchgate.net/)

---
**Hinweis:**
Die in diesem Dokument enthaltenen Formeln und Daten sind **vereinfachte Modelle**. Für präzise Berechnungen sollten **experimentelle Daten** oder **CFD-Simulationen** verwendet werden.

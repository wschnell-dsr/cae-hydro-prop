# Chord-Verteilungen von Propellerblättern

## 1. Elliptische Verteilung
**Beschreibung:**
Die elliptische Chord-Verteilung ist eine der häufigsten Formen für hydrodynamische Propeller. Sie sorgt für eine gleichmäßige Abnahme der Blattbreite von der Nabe zur Spitze und reduziert Wirbelverluste an der Blattspitze. Die Form ähnelt einer halben Ellipse.

**Formel:**
\[
c(r) = c_0 \sqrt{1 - \left(\frac{r}{R}\right)^2}
\]

**Parameter:**
- \( c(r) \): Chord-Länge an der Position \( r \)
- \( c_0 \): Maximale Chord-Länge an der Nabe (\( r = 0 \))
- \( R \): Propellerradius (Spitzenradius)
- \( r \): Aktueller Radius entlang der Blattlänge (von \( 0 \) bis \( R \))

**Eigenschaften:**
- Hydrodynamisch effizient
- Reduziert Spitzenwirbel
- Wird oft für hochperformante Propeller verwendet

---

## 2. Lineare Verteilung
**Beschreibung:**
Bei einer linearen Verteilung nimmt die Chord-Länge gleichmäßig von der Nabe zur Spitze ab. Diese Form ist einfacher zu berechnen und herzustellen, aber weniger effizient als die elliptische Verteilung.

**Formel:**
\[
c(r) = c_0 \left(1 - \frac{r}{R}\right)
\]

**Parameter:**
- \( c(r) \): Chord-Länge an der Position \( r \)
- \( c_0 \): Maximale Chord-Länge an der Nabe (\( r = 0 \))
- \( R \): Propellerradius (Spitzenradius)
- \( r \): Aktueller Radius entlang der Blattlänge (von \( 0 \) bis \( R \))

**Eigenschaften:**
- Einfachere Herstellung
- Geringere hydrodynamische Effizienz
- Wird oft für kostengünstige oder einfache Propeller verwendet

---

## 3. Abgeschnittene elliptische Verteilung
**Beschreibung:**
Eine angepasste elliptische Verteilung, bei der die Chord-Länge an der Spitze nicht auf null abfällt, sondern einen minimalen Wert \( c_{\text{min}} \) erreicht. Dies erhöht die strukturelle Stabilität und kann die hydrodynamischen Eigenschaften weiter optimieren.

**Formel:**
\[
c(r) = c_0 \sqrt{1 - \left(\frac{r}{R}\right)^2} + c_{\text{min}}
\]

**Parameter:**
- \( c_{\text{min}} \): Minimale Chord-Länge an der Spitze
- Alle anderen Parameter wie bei der elliptischen Verteilung

**Eigenschaften:**
- Kombiniert Effizienz mit struktureller Stabilität
- Wird oft für große oder hochbelastete Propeller verwendet

---
## 4. Polynomiale Verteilung
**Beschreibung:**
Die Chord-Länge folgt einem polynomialen Verlauf, z. B. quadratisch oder kubisch. Diese Verteilung ermöglicht eine flexible Anpassung an spezifische Designanforderungen.

**Formel (quadratisch):**
\[
c(r) = c_0 \left(1 - \left(\frac{r}{R}\right)^2\right)
\]

**Eigenschaften:**
- Flexibler als lineare oder elliptische Verteilungen
- Kann an spezifische hydrodynamische Anforderungen angepasst werden

---
## 5. Trapezförmige Verteilung
**Beschreibung:**
Die Chord-Länge bleibt über einen Großteil der Blattlänge konstant und fällt dann zur Spitze hin linear oder gekrümmt ab. Diese Form wird häufig bei Schiffpropellern verwendet.

**Formel:**
\[
c(r) =
\begin{cases}
c_0 & \text{für } 0 \leq r \leq r_1 \\
c_0 \left(1 - \frac{r - r_1}{R - r_1}\right) & \text{für } r_1 < r \leq R
\end{cases}
\]

**Eigenschaften:**
- Einfache Herstellung
- Gute Balance zwischen Effizienz und struktureller Stabilität

---
### Zusammenfassung
| Verteilungstyp          | Vorteile                          | Nachteile                          | Typische Anwendung               |
|-------------------------|-----------------------------------|------------------------------------|-----------------------------------|
| **Elliptisch**          | Hohe Effizienz, geringe Wirbelverluste | Komplexere Herstellung            | Hochperformante Propeller         |
| **Linear**              | Einfache Herstellung              | Geringere Effizienz                | Kostengünstige Propeller          |
| **Abgeschnitten elliptisch** | Effizienz + Stabilität       | Komplexeres Design                 | Große oder hochbelastete Propeller|
| **Polynomial**          | Flexible Anpassung                 | Aufwendige Berechnung              | Spezialanwendungen                |
| **Trapezförmig**        | Einfache Herstellung, stabil      | Geringere Effizienz als elliptisch | Schiffpropeller                   |

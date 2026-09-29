# Blade parameter

The blade is defined as a sub dictionary of the propeller configuration

| **Term**                     | Key                        |Description                                                           |
|:-----------------------------|----------------------------|----------------------------------------------------------------------|
| **Profile points**           | profile_pnts               | Number of profile points for discretisation                          |
| **Radius points**            | radius_pnts                | Number of points along radius for discretisation                     |
| **Profile configuration**    | profile_cnf                | Configuration of the pitch distribution along the blade radius       |
| **Hub radius**               | radius_hub                 | Minimal radius of the blade                                          |
| **Tip radius**               | radius_tip                 | Radius of the tip                                                    |
| **Direction**                | rotation_direction         | Rotation direction "LEFT" or "RIGHT"                                 |
| **Pitch configuration**      | pitch_cnf                  | Configuration of the pitch distribution along the blade radius       |
| **Chord configuration**      | chord_cnf                  | Configuration of the chord distribution along the blade radius       |
| **Thicknes configuration**   | thickness_distribution_cnf | Configuration of the profile thickness along the blade radius        |
| **Skew configuration**       | skew_cnf                   | Configuration of the rake along the blade radius                     |
| **Rake configuration**       | rake_cnf                   | Configuration of the skew along the blade radius                     |

## **Pitch configuration**

There are 5 pitch distribution types
- LINEAR
- QUADRATIC
- EXPONENTIAL
- LINEAR_TABULATED
- CUBIC_SPLINE_TABULATED

The first 3 are defined by type, pitch_hub and pitch_tip:

```json
{
    "pitch_type": "LINEAR|QUADRATIC|EXPONENTIAL",
    "pitch_hub": 0.02,
    "pitch_tip": 0.02
}
```
The last 2 are defined by type, radius(list) and pitch(list):

```json
{
    "pitch_type": "LINEAR_TABULATED|CUBIC_SPLINE_TABULATED",
    "radius": [...],
    "pitch": [...]
}
```

## **Chord configuration**

There are 4 chord distribution types
- LINEAR
- ELLIPTIC
- LINEAR_TABULATED
- CUBIC_SPLINE_TABULATED

The first 2 are defined by type, chord_hub and chord_tip:

```json
{
    "chord_type": "LINEAR|ELLIPTIC",
    "chord_hub": 0.02,
    "chord_tip": 0.02
}
```
The last 2 are defined by type, radius(list) and pitch(list):

```json
{
    "chord_type": "LINEAR_TABULATED|CUBIC_SPLINE_TABULATED",
    "radius": [...],
    "pitch": [...]
}
```

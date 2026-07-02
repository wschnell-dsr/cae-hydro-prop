#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import numpy as np
import salome
from salome.geom import geomBuilder


class NacaBlade:
    """
    """
    def __init__(self, naca_profile, n_radial: int = 20,
                 radius_root: float = 0.05, radius_tip: float = 0.25,
                 root_twist: float = 45.0, tip_twist: float = 5.0,
                 chord_function=None):
        """
        Args:
            naca_profile: NACAProfile Objekt
            n_radial: Anzahl radialer Schnitte
            radius_root: Wurzelradius [m]
            radius_tip: Spitzenradius [m]
            root_twist: Verdrehung an Wurzel [°]
            tip_twist: Verdrehung an Spitze [°]
            chord_function: Optional Sehnenlänge als Funktion von r
        """
        self.naca = naca_profile
        self.n_radial = n_radial
        self.radius_root = radius_root
        self.radius_tip = radius_tip
        self.root_twist = root_twist
        self.tip_twist = tip_twist

        # Standard: Linear tapered chord
        if chord_function is None:
            self.chord_function = lambda r: 0.08 * (1 - (r - radius_root) / (radius_tip - radius_root)) ** 0.5
        else:
            self.chord_function = chord_function

        # SALOME Geom Builder
        salome.salome_init()
        self.geom = geomBuilder.New()
        self.study = salome.myStudy

    def generate_blade_sections(self, n_points_per_section: int = 100) -> list:
        """
        Generiert radiale Schnitte des NACA-Profils mit Verdrehung

        Returns:
            Liste von (x, y, z) Arrays für jeden radialen Schnitt
        """

        # 2D NACA Profil
        upper, lower = self.naca.profile_coordinates(n_points_per_section)
        x_upper, y_upper = upper
        x_lower, y_lower = lower

        # Radiale und Verdrehungs-Arrays
        radii = np.linspace(self.radius_root, self.radius_tip, self.n_radial)
        twist_angles = np.linspace(self.root_twist, self.tip_twist, self.n_radial)

        sections = []

        for r, twist_deg in zip(radii, twist_angles):
            twist_rad = np.radians(twist_deg)
            chord = self.chord_function(r)

            # Skaliere Profil
            xu = chord * x_upper
            yu = chord * y_upper
            xl = chord * x_lower
            yl = chord * y_lower

            # Kombiniere upper und lower (von TE zu TE)
            x_profile = np.concatenate([xu[::-1], xl[1:]])
            y_profile = np.concatenate([yu[::-1], yl[1:]])

            # Axiale Position (0 bis 1)
            z_axial = (r - self.radius_root) / (self.radius_tip - self.radius_root)

            # Transformation: Verdrehung + Verschiebung zu Radius r
            cos_t = np.cos(twist_rad)
            sin_t = np.sin(twist_rad)

            x_3d = z_axial * np.ones_like(x_profile)                    # Axial
            y_3d = r + y_profile * cos_t                               # Radial (mit Verdrehung)
            z_3d = x_profile + y_profile * sin_t                       # Umfang (mit Profil + Verdrehung)

            sections.append(np.array([x_3d, y_3d, z_3d]).T)

        return sections

    def create_blade_geometry(self) -> 'GEOM_Object':
        """
        Erstellt die Propellerschaufel als SALOME Geometrie-Objekt
        mittels Loft (Sweep) der Schnitte

        Returns:
            SALOME Geom Shape der Propellerschaufel
        """

        sections = self.generate_blade_sections(n_points_per_section=80)

        # Erstelle Splines für jeden Schnitt
        wires = []

        for idx, section in enumerate(sections):
            # Konvertiere zu Punkte Liste
            points_list = []
            for pt in section:
                point = self.geom.MakeVertex(float(pt[0]), float(pt[1]), float(pt[2]))
                points_list.append(point)

            # Schließe das Profil (verbinde letzten mit ersten Punkt)
            points_list.append(points_list[0])

            # Erstelle Bézier-Kurve durch die Punkte
            curve = self.geom.MakeBezier(points_list)

            # Konvertiere zu Wire
            wire = self.geom.MakeWire([curve])
            wires.append(wire)

        # Erstelle Loft (Sweep) zwischen allen Wires
        blade = self.geom.MakeLoft(wires, False, True)

        return blade

    def create_blade_with_faces(self) -> 'GEOM_Object':
        """
        Alternative: Erstellt Oberflächen zwischen benachbarten Schnitten
        Dies ist präziser für CFD-Meshes
        """

        sections = self.generate_blade_sections(n_points_per_section=60)

        all_edges = []

        for idx, section in enumerate(sections):
            # Konvertiere Schnitt zu Punkte
            points_list = []
            for pt in section:
                point = self.geom.MakeVertex(float(pt[0]), float(pt[1]), float(pt[2]))
                points_list.append(point)

            # Schließe Profil
            points_list.append(points_list[0])

            # Erstelle Kantenzug
            edges = []
            for i in range(len(points_list) - 1):
                edge = self.geom.MakeLine(points_list[i], points_list[i+1])
                edges.append(edge)

            wire = self.geom.MakeWire(edges)
            all_edges.append(wire)

        # Erstelle Flächen zwischen benachbarten Schnitten
        surfaces = []
        for i in range(len(all_edges) - 1):
            # Loft zwischen zwei aufeinanderfolgenden Wires
            surf = self.geom.MakeLoft([all_edges[i], all_edges[i+1]], False, True)
            surfaces.append(surf)

        # Kombiniere alle Flächen zu einer Shell
        blade_shell = self.geom.MakeShell(surfaces)

        # Optional: Konvertiere zu Solid für besseres Meshing
        try:
            blade_solid = self.geom.MakeSolid([blade_shell])
            return blade_solid
        except:
            # Wenn Solid nicht möglich, gib Shell zurück
            return blade_shell

    def add_to_study(self, blade_shape: 'GEOM_Object', name: str = "Propeller_Blade"):
        """
        Fügt die Geometrie zur SALOME-Studie hinzu
        """
        blade_id = self.geom.addToStudy(blade_shape, name)
        return blade_id

    def create_hub(self, hub_radius: float) -> 'GEOM_Object':
        """
        Erstellt eine Nabe (Hub) als Zylinder
        """
        hub = self.geom.MakeCylinder(
            self.geom.MakeVertex(0, 0, 0),  # Position
            self.geom.MakeDirection(1, 0, 0),  # Achse (axial)
            hub_radius,  # Radius
            self.radius_tip - self.radius_root  # Höhe (= axiale Länge)
        )
        return hub

    def create_computational_domain(self, domain_radius: float,
                                   domain_length: float = None) -> 'GEOM_Object':
        """
        Erstellt eine zylindrische Computational Domain für CFD

        Args:
            domain_radius: Radius der Domain [m]
            domain_length: Länge der Domain (Standard: 3× Blatt-Länge)
        """

        if domain_length is None:
            domain_length = 3 * (self.radius_tip - self.radius_root)

        # Erstelle Zylinder
        origin = self.geom.MakeVertex(-domain_length/2, 0, 0)
        axis = self.geom.MakeDirection(1, 0, 0)

        domain = self.geom.MakeCylinder(origin, axis, domain_radius, domain_length)

        return domain

    def export_geometry(self, filename: str):
        """
        Exportiert die Geometrie als STEP-Datei
        """
        blade = self.create_blade_with_faces()
        self.geom.ExportSTEP(blade, filename)
        print(f"✓ Geometrie exportiert: {filename}")


# === VERWENDUNGSBEISPIEL ===
if __name__ == "__main__":
    from naca import NACAProfile

    # Initialisiere SALOME (wird automatisch gemacht)
    # salome.salome_init()

    # Erstelle NACA 4412 Profil
    naca = NACAProfile("4412")

    # Erstelle Propeller-Geometrie in SALOME
    propeller = PropellerGeometrySALOME(
        naca_profile=naca,
        n_radial=15,
        radius_root=0.05,
        radius_tip=0.25,
        root_twist=45,
        tip_twist=5
    )

    # Erstelle Schaufel
    blade = propeller.create_blade_with_faces()
    propeller.add_to_study(blade, "Propeller_Blade")

    # Optional: Erstelle Hub
    hub = propeller.create_hub(hub_radius=0.04)
    propeller.add_to_study(hub, "Hub")

    # Optional: Erstelle Computational Domain
    domain = propeller.create_computational_domain(domain_radius=0.6, domain_length=1.0)
    propeller.add_to_study(domain, "Fluid_Domain")

    print("✓ Geometrie in SALOME erstellt!")

    # Exportiere falls nötig
    # propeller.export_geometry("propeller_blade.step")

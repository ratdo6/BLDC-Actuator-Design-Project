<div align="center">

# BLDC Cycloidal Actuator - Quadruped Robot Leg

Inexpensive · Teensy 4.1 · Backdrivable · 3D printed · Moteus r4.11 FOC · CAN bus · Low backlash · ROS2 · BLDC motor

![Status](https://img.shields.io/badge/status-early%20development-orange)

</div>

A custom cycloidal gearbox and actuator designed for a quadruped robot. Built around an 8308 BLDC motor, mjbots moteus r4.11, teensy 4.1, 3D printing, and ROS2. It takes advantage of the easy to manufacture cycloid geometry to create a cheap, but efficient actuator. This project is an opportunity for me to learn new skills and hone my strengths as an engineer. It is still in the early phases of development.  

![Gearbox Assembly](images/cycloid_actuator_screenshot.png)

## Goals

- **Plays nice with ROS2** — built to hook into ROS2 for the higher-level brain stuff (motion planning, orchestration, etc) 
- **Quadruped ready** — designed around a 12-DOF, 4-leg setup, but flexible enough to be repurposed
- **Precise joints** — actuator and drivetrain picks aim for minimal backlash, so movement stays accurate instead of sloppy
- **Custom electronics** — custom hub PCB handles CAN routing, power distrubution, and sensors avoiding the mess of breakout boards and jumper wires
- **3D-printable/sourceable** — Parts are deisgned to be FDM printer friendly or easily sourceable online 
- **Actually documented** — schematics, step files, firmware, design decisions, etc are all written up so I (or anyone else) can actually follow along and buid it

## Status

- [x] Cycloidal disc design, [Python visualizer](cycloidal_drive_visualizer/cycloidal_drive_visualizer.py)
- [x] Actuator design, [CAD](CAD/onshape_link.md)
- [x] [Bill of materials (BoM)](BOM/cycloidal_actuator_BOM.xlsx) (rough version available)
- [x] Calibrate Moteus r4.11 controllers to BLDC motors
- [x] 3D Printed protoype, tolerances dialed
- [ ] [KiCad PCBA schematic](Kicad-schematic/Teensy_BLDC_Build/Teensy_BLDC_Build.kicad_sch)
- [ ] Teensy 4.1 software
- [ ] Actuator efficiency and backlash testing
- [ ] Full 3DOF Leg Design
- [ ] Demo video(s)
- [ ] All CAD uploaded in .STEP & .STL formats

## Design Overview

Actuator architecture is built around a cycloid drive paired with a BLDC motor and FOC controller, chosen for its combination of high reduction ratio, low backlash, and shock tolerance. Crossed roller bearings are used at joint interface to handle combined radial and axial loads with minimal play. All design choices were picked with a legged robot in mind that has to absorb impact loads on every step.

- **Reduction ratio:** 9:1 (allows backdrivability, 10 roller pins, 9 lobes on disc)
- **E / Rr:** 0.500 (eccentricity (E) = 1.25mm)
- **Max pressure angle:** 20.03 degrees
- **Disc material:** PLA+ (future exploration into machined nylon, delrin, or aluminum planned)
- **BLDC motor:** Eagle Power 8308 90kv (cheap, powerful, and readily available)
- **FOC controller:** Moteus r4.11 (CAN bus interface, closed loop, compact form factor)

A custom built [cycloid disc parameters visualizer](cycloidal_drive_visualizer/cycloidal_drive_visualizer.py) was used to optimize variable selection before beginning CAD modeling
![Cycloidal Drive Visualizer](images/cycloidal_drive_visualizer.png)

All CAD designed in OnShape. [View OnShape Document](https://cad.onshape.com/documents/7e181885841e2c0563f5ea8b/w/eb359d6e40468758aae61fb6/e/6c3a266b2d21d51902da69a4?renderMode=0&uiState=6a44a79b4963b5aa094522b4)
![Gearbox Assembly Exploded View](images/cycloid_actuator_exploded_view_screenshot.png)

The actuator design centers on three choices that reinforce the same goal of minimal backlash, without needing industrial manufacturing access.

Cycloidal reduction was chosen over harmonic, planetary gearing, or capstan drives as the best fit for a self-built project. Harmonic drives offer great backlash performance but rely on flex-splines that are hard to source or machine yourself. Planetary gearboxes are easier to source but need precision-ground components to match cycloidal-level backlash. Capstan drives offer great performance for cost but are bulky and difficult to integrate in a compact leg assembly. Cycloidal drives split the difference — mechanically simple, tolerant of imperfect fabrication, compact, and low-backlash by design.

BLDC + FOC control (via the Moteus r4.11) keeps torque output smooth, which matters since any motor cogging gets amplified through the reduction stage. It also keeps the system modular, each joint handles its own closed-loop control over CAN, so the central hub just sends setpoints instead of managing low-level control for all 12 actuators.

Cross roller bearings at the output stage protect my backlash budget end-to-end. A precise cycloidal stage doesn't help if the output shaft has play. These bearings handle the combined radial/axial loads of stance and impact in a compact footprint, keeping joint mass reasonable for leg dynamics.

Together, these choices aim for locomotion-grade precision using parts and processes an individual builder can actually access.




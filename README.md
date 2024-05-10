# Project Feather Wing

This repository includes all the python code necessary for the sensor box, the initial structural analysis for the design, and the test analysis.

---
## Introduction

This repository contains all the code pertaining to the wing spar project that forms part of
the AE1222-I Design and Construction course of the B.Sc. Aerospace Engineering program
at TU Delft.

---
## Description

`structural-analysis.py` is a stand-alone tool that was used to verify potential
design options and have a visual representation of its performance. Additionally,
it proved useful to be able to identify where along the beam any failures were
occurring.

`IAC_DAQ_MCP2221.py` is the provided code to run the sensors on the test system
which we, as a group, had to calibrate and configure to output accurate data
in a format that is useful for further data analysis.

`andrei-test.py` was written by Andrei Tabara and was the first attempt at
programmatically determining valid design solutions. Parts of this were
ultimately merged into `structural-analysis.py`.

---
## Conclusion

Overall, this project was a success in the regard that the program worked
effectively. However, its impact in the greater project of design a wing
was less significant due to time constraints which meant the program could
not be used extensively.

In the future, priority should be placed on a working program instead of
committing more time into a program that works very well but its potential
will nevertheless go to waste as there's not enough time.


# OBC Software
This directory contains all required python software to be implemented by the OBC to control the Selfie-Sat. This software is meant to interface with the hardware built by the QSET team and the firmware written in the [qset-firmware repository](https://github.com/queens-satellite-team/qset-firmware). 

## Environment Setup

```
python3 -m venv venv-obc
source venv-obc/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## Folder Layout
### Drivers
Location for interfacing directly with hardware. Methods and classes shall be independent of hardware.

### Events
Asynchrounous routines that the OBC must perform dependent on external interupts.

### Managers
Classes that handle the execution, failures, and timing of events and tasks.

### Sub-Systems
Classes to represent each of the sub-systems present on the satellite. Each sub-system shall utilize the Drivers to interface with their respective hardware, and shall listen to the Managers before performing any functionality.

### Tasks
Synchronous routines that the OBC must perform through out the mission duration. 


# LightBurn Configuration Guide

This document provides a step-by-step guide to configure **LightBurn** for optimal use with your laser cutting machine.

---

## Table of Contents
1. [Version Notice](#version-notice)  
2. [Adding a Device](#adding-a-device)  
3. [Device Settings](#device-settings)  
4. [Laser Panel Configuration](#laser-panel-configuration)  
5. [Custom GCode Settings](#custom-gcode-settings)  
6. [General Software Settings](#general-software-settings)  

---

## Version Notice
The **LightBurn v1.7.03** version contains a bug that offsets the speed, power, and coordinates by a positive value of `1`. This issue cannot be resolved. Therefore, it is recommended to install **LightBurn v1.0.04**.  

### Key Changes in v1.0.04:
- The device must be configured **manually**.  
- Skip any unavailable options during device setup.  
- `M8` and `M9` commands cannot be edited in this version (this is not critical).  
- Other settings remain similar, with a few specific updates outlined below.

---

## Adding a Device

### Instructions for v1.7.03:
1. Open **LightBurn** and navigate to the **Laser** panel on the right side of the screen.  
2. Click on the **Devices** button to open the Devices window.  
3. In the Devices window, click **Import** and select the `device.lbdev` file from the repository.  
4. A custom device will be created with the following properties:  
   - **Workspace size:** `300mm x 300mm`.  
   - **Origin:** Set to **Front-Left**.  
   - **Auto-home laser on startup:** Disabled.  

### Changes in v1.0.04:
- Manually configure the device:
  1. In the Devices window, select **Create Manually**.  
  2. Set the workspace size to `300mm x 300mm`.  
  3. Configure the origin to **Front-Left**.  
  4. Skip options that are unavailable in this version.  

---

## Device Settings

### Instructions for v1.7.03:
1. From the top menu, go to **Edit** > **Device Settings**.  
2. In the **Basic Settings** tab, adjust the following:  
   - Set **S Value Max** to `100`.  

3. In the **Custom GCode** tab:
   - Set **Air On (M8)** to `;M8`.  
   - Set **Air Off (M9)** to `;M9`.  
     - *This disables these commands in the generated GCode, ensuring compatibility with devices that lack air control.*

### Changes in v1.0.04:
- The `M8` and `M9` commands cannot be edited in this version. This limitation does not affect functionality.  
- Set **S Value Max** to `100` in the **Device Settings** as before.

---

## Laser Panel Configuration

### Instructions for v1.7.03:
1. In the **Laser** panel, configure the following:  
   - **Start From:** Set to **Current Position**.  
   - **Job Origin:** Set to the bottom-left corner (leftmost option in the bottom row).  

### Changes in v1.0.04:
The settings remain **unchanged**.

---

## Custom GCode Settings

### Instructions for v1.7.03:
- From **Edit** > **Device Settings**, navigate to the **Custom GCode** tab.  
- Update the following values:
  - Set **Air On (M8)** to `;M8`.  
  - Set **Air Off (M9)** to `;M9`.  

### Changes in v1.0.04:
The `Custom GCode` settings cannot be modified in this version, but this has no practical impact.

---

## General Software Settings

### Instructions for v1.7.03:
1. From the top menu, go to **Edit** > **Settings**.  
2. Adjust the settings as follows:
   - In the **Editor Settings** tab:
     - Disable **Automatically Check for Updates**.  
   - In the **Import/Export** tab:
     - Set **Auto-Close Tolerance (mm)** to `0.005`.  
     - Set **Curve Tolerance (mm)** to `0.005`.  

### Changes in v1.0.04:
The settings remain **unchanged**.

---

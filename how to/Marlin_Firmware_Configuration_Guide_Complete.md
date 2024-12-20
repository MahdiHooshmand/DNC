# Marlin Framework Documentation

## Introduction
This document serves as a comprehensive guide for configuring and compiling Marlin firmware, particularly for users working with RAMPS hardware. Whether you're a beginner or an advanced user, this guide will help you optimize your firmware for your 3D printer.

## Table of Contents
1. [Compatibility with RAMPS Hardware](#1-compatibility-with-ramps-hardware)
2. [Recommended Tools for Compiling Marlin](#2-recommended-tools-for-compiling-marlin)
3. [Setting Up VSCode for Marlin](#3-setting-up-vscode-for-marlin)
    - [Installing Required Extensions](#installing-required-extensions)
    - [Opening the Marlin Project Folder](#opening-the-marlin-project-folder)
    - [Locating the Configuration Files](#locating-the-configuration-files)
    - [Disabling the Boot Screen](#disabling-the-boot-screen)
    - [Custom Boot and Status Screen Images](#custom-boot-and-status-screen-images)
4. [Configuring the Serial Port](#4-configuring-the-serial-port)
5. [Disabling Bluetooth and Wi-Fi](#5-disabling-bluetooth-and-wi-fi)
6. [Troubleshooting Common Issues](#6-troubleshooting-common-issues)
7. [Further Reading](#7-further-reading)

## 1. Compatibility with RAMPS Hardware
When using Marlin as the firmware framework alongside RAMPS as the middleware, it is recommended to utilize versions prior to Marlin 2.0.5. This is because RAMPS is an older hardware platform and exhibits better compatibility with earlier versions of Marlin firmware.  
For the best stability and performance, it is advisable to use the Marlin 2.0.x bugfix branch, as it includes important updates and fixes for enhanced functionality.

## 2. Recommended Tools for Compiling Marlin
To compile Marlin firmware, it is highly recommended to use Visual Studio Code (VSCode). Unlike other tools, such as Arduino IDE, certain versions of Marlin cannot be compiled using Arduino, and some versions are only compilable on Ubuntu operating systems. However, these limitations do not apply to VSCode, making it the preferred choice for seamless and efficient compilation across different platforms.

## 3. Setting Up VSCode for Marlin

### Installing Required Extensions
- Open VSCode and navigate to the Extensions marketplace.
- Search for and install the following extensions:
    - **Auto Build Marlin**: Provides tools and settings to streamline configuration and compilation of Marlin firmware.
    - **PlatformIO IDE Extension**:
        - A crucial tool for building and uploading the firmware, offering compatibility with various microcontroller platforms.
        - **Note**: When starting this extension, it requires a Python virtual environment (venv) with Python version 3.6 or higher. To set this up, open the Marlin project folder in the terminal and run the following command:
        ```bash
        sudo apt install python3-venv
        ```
    - **C/C++ Extension**: Enables IntelliSense, code navigation, and debugging support for Marlin’s C++ codebase.

### Opening the Marlin Project Folder
- From the VSCode menu, click on `File > Open Folder`.
- Select the folder containing the Marlin project files that you have downloaded.
- This will load the Marlin project into VSCode, allowing you to configure and compile the firmware.

### Locating the Configuration Files
- Inside the project folder, navigate to the Marlin directory.
- Locate the `Configuration.h` file. This file contains the primary configuration settings for the firmware.
- Open `Configuration.h` in the VSCode editor to begin customizing the firmware for your specific hardware and printer settings.

## 4. Configuring the Serial Port
In `Configuration.h`, set the `SERIAL_PORT` setting to 1:
```cpp
#define SERIAL_PORT 1
```

### Setting the Baud Rate
For RAMPS boards, set the baud rate to 115200:
```cpp
#define BAUDRATE 115200
```

### Enabling Serial Ports in New Marlin Versions
If using Marlin versions older than 2.0.5, avoid enabling additional serial ports. Leave their settings commented out to avoid issues.

## 5. Disabling Bluetooth and Wi-Fi
For simplicity and compatibility, it is recommended not to enable Bluetooth or Wi-Fi features unless specifically required.

## Finalizing and Building the Firmware

### Saving the Configuration File
After completing all the necessary changes in the `Configuration.h` file:
- Save the file to ensure your modifications are retained.

### Using the Auto Build Marlin Extension
- Open the Auto Build Marlin extension in VSCode.
- Locate and click the Build button within the extension interface.

### Verify the Build Output
- Allow the build process to complete.
- Review the displayed output to ensure there are no errors and that all configurations have been applied correctly.

## Setting the Motherboard

### Changing the Motherboard Setting
In the `Configuration.h` file, change the `#define MOTHERBOARD` setting to match your board. For example:
```cpp
#define MOTHERBOARD BOARD_RAMPS_14_EFB
```
- This configuration is for a RAMPS 1.4 EFB motherboard, which is the most commonly used board in this setup. The EFB designation refers to controlling 3 relays for the extruder, fan, and heated bed.

## Final Thoughts
- This guide has provided the necessary steps to set up Marlin firmware for use with RAMPS hardware and laser systems. Follow the instructions carefully to ensure proper configuration, and always test the firmware after making changes to verify functionality.

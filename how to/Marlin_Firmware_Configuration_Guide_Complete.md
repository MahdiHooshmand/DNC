
### Custom Boot and Status Screen Images
To display your custom start-up image (e.g., a logo or a welcome screen), enable the following options in `Configuration.h`:
```cpp
#define SHOW_CUSTOM_BOOTSCREEN
#define SHOW_CUSTOM_STATUS_SCREEN_IMAGE
```
- Prepare your custom image as a PNG file and place it in the `/marlin/pictures` folder within your Marlin project directory.

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

## Filament Diameter Configuration

### Default Filament Diameter
The default filament diameter setting in the `Configuration.h` file does not require any changes.  
There is no need to specify or modify this value, as it has no impact on the functionality of the device in the current setup.  
Leaving this setting as-is ensures that the firmware remains compatible with its default configurations without introducing unnecessary changes.

## PSU Configuration

### Power Supply Unit (PSU) Settings
The PSU settings in the `Configuration.h` file should remain unchanged.  
There is no need to modify these settings as the default configuration is sufficient for most setups, including the current one.  
By keeping the PSU settings unchanged, you ensure stable and reliable firmware behavior without introducing unnecessary complexity.

## Thermistor Settings

### Thermistor Configuration
Since the system will also be using a laser, there is no need to configure or specify thermistor settings in the `Configuration.h` file.  
The default thermistor settings can be left unchanged, as they will not affect the laser functionality.  
By keeping the default thermistor values, you ensure that the configuration remains simple and functional without unnecessary modifications.

## Endstop Settings

### Activating Endstop Pins for X, Y, and Z Axes
In the `Configuration.h` file, ensure the following three lines are enabled (not commented out):
```cpp
#define USE_XMIN_PLUG
#define USE_YMIN_PLUG
#define USE_ZMIN_PLUG
```
- Even though only two axes (X and Y) are used in this project, it is not necessary to disable the Z-axis.  
- Leaving the Z-axis endstop active will not cause any issues and ensures the firmware remains compatible with different setups.

### Activating Endstop Pullups for X, Y, and Z Axes
In the `Configuration.h` file, ensure the following three lines are enabled (not commented out):
```cpp
#define ENDSTOPPULLUP_XMIN
#define ENDSTOPPULLUP_YMIN
#define ENDSTOPPULLUP_ZMIN
```
- These settings enable pull-up resistors for the endstops of the X, Y, and Z axes.  
- Enabling these pull-ups ensures proper signal detection for the endstops, improving the reliability of the system.

### Configuring Endstop Inversion for Optical Sensors
Since optical sensors are being used in this project and they are normally open, the endstop logic needs to be inverted.  
In the `Configuration.h` file, update the following lines to set the endstop logic inversion to true:
```cpp
#define X_MIN_ENDSTOP_INVERTING true  // Set to true to invert the logic of the endstop.
#define Y_MIN_ENDSTOP_INVERTING true  // Set to true to invert the logic of the endstop.
```
This configuration ensures that the optical sensors are correctly recognized, and the system operates as intended.

## Default 3D Printing Settings

### Leaving 3D Printing Settings Unchanged
The remaining settings in the `Configuration.h` file are primarily related to standard 3D printing functionality. Since they are not needed for this specific project, no modifications will be made to these parameters.  
These default settings are suitable for general 3D printing operations and do not need to be altered for the current use case.  
By leaving these settings unchanged, the firmware maintains compatibility with typical 3D printing configurations while focusing only on the necessary adjustments for this project.

## Setting the Motherboard

### Changing the Motherboard Setting
In the `Configuration.h` file, change the `#define MOTHERBOARD` setting to match your board. For example:
```cpp
#define MOTHERBOARD BOARD_RAMPS_14_EFB
```
- This configuration is for a RAMPS 1.4 EFB motherboard, which is the most commonly used board in this setup. The EFB designation refers to controlling 3 relays for the extruder, fan, and heated bed.

## Final Thoughts
- This guide has provided the necessary steps to set up Marlin firmware for use with RAMPS hardware and laser systems. Follow the instructions carefully to ensure proper configuration, and always test the firmware after making changes to verify functionality.

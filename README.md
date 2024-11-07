# SAEJ1979 Standard PIDs

This repository contains the Parameter IDs (PIDs) from the SAE J1979 standard, commonly used for onboard diagnostics (OBD) and vehicle telematics. The data provided here enables users to query and interpret various parameters related to engine performance, emissions, and other critical functions in compliance with the SAE J1979 standard.

## Overview

**SAE J1979**, also known as OBD-II, is a standard developed by the Society of Automotive Engineers (SAE). It provides a universal way to access diagnostic data from a vehicle's onboard computer through a standardized set of **Parameter IDs (PIDs)**. The primary purpose of this standard is to ensure that all vehicles manufactured for use in the United States (and many other regions) support a consistent set of data points, which can be accessed via a compatible scan tool.

For more information, please refer to [SAE J1979 on Wikipedia](https://en.wikipedia.org/wiki/OBD-II_PIDs).

## Purpose of this Repository

The repository aims to provide a comprehensive list of PIDs specified by the SAE J1979 standard. This can be useful for:

- Automotive engineers and technicians who need to access specific diagnostic information.
- Developers creating diagnostic tools and software for reading OBD-II data.
- Enthusiasts interested in understanding vehicle performance data.

## SAE J1979 PIDs and Commands

The SAE J1979 standard includes a range of Parameter IDs (PIDs) that are used to request specific data from a vehicle's Engine Control Module (ECM). In this repository, we organize these PIDs as **Commands** - structured requests that include both the PID and additional metadata needed to properly communicate with the vehicle.

### Commands and Signals

Each Command represents a complete OBD-II message that can be sent to the vehicle and includes:

- **PID Code**: The specific Parameter ID being requested
- **Header (HDR)**: The command's 11-bit identifier for CAN communication
- **Frequency**: How often the command can be safely sent to the vehicle
- **Signals**: The data points that the vehicle returns in response to this command

When a Command is sent to the vehicle, it responds with one or more **Signals**. While PIDs are often thought of as representing specific data points, it's more accurate to think of them as requests that can return multiple pieces of information (Signals). 
For example, a single PID command might return multiple Signals such as:
- Engine RPM
- Throttle position
- Engine load

Each Signal includes:

- **Identifier**: A unique name for the data point
- **Format**: Instructions for interpreting the raw bytes from the vehicle's response
- **Units**: The measurement units for the decoded value
- **Description**: What the data represents

### Example Structure

```json
{
  "commands": [{
    "hdr": "7E0",
    "cmd": {"01": "0C"},
    "freq": 0.1,
    "signals": [{
      "id": "ENGINE_RPM",
      "fmt": {
        "len": 16,
        "max": 16383.75,
        "mul": 0.25,
        "unit": "revolutionsPerMinute"
      },
      "name": "Engine RPM"
    }]
  }]
}
```

## Contributing

Contributions are welcome! If you find any discrepancies or have suggestions for improvements, feel free to open an issue or submit a pull request.

## Resources

- [Wikipedia - OBD-II PIDs](https://en.wikipedia.org/wiki/OBD-II_PIDs)
- [Wikipedia - On-board diagnostics](https://en.wikipedia.org/wiki/On-board_diagnostics)
- [SAE International](https://www.sae.org/)

## License

This repository is licensed under the Attribution-ShareAlike 4.0 International (CC-BY-SA-4.0) License. Please see the LICENSE file for more details.
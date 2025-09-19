# SteamVR Integration for Home Assistant
Integration that lets you monitor and control your SteamVR setup (HTC Vive, Valve Index, HP REVERB, Oculus Rift and more) from Home Assistant.

## Features
- Sensors:
    - SteamVR status
    - Current game
    - Headset status (In use/Standby/Idle)
    - Controllers (is connected, battery level, is charging)
- Notifications to headset
- Displaying images (even animated) in headset - via notifications with `imageUrl` / `imagePath` / `imageData`(`base64`)
- Listening for SteamVR events - button click, switching passthrough and more
- Triggering controllers vibration from Home Assistant


## Getting started

### Prerequisites

Install [Home Assistant Agent for SteamVR](https://github.com/Antoni-Czaplicki/SteamVR.HA-Agent) on the PC that you are using with your VR

### HACS installation (Recommended)

Open HACS and search for `SteamVR` under integrations.
You can choose to install a specific version or from master (Not recommended).

### Manual Installation

<details>
<summary><b>View instructions</b></summary>

1. Open the directory with your Home Assistant configuration (where you find `configuration.yaml`,
   usually `~/.homeassistant/`).
2. If you do not have a `custom_components` directory there, you need to create it.

#### Git clone method

This is a preferred method of manual installation, because it allows you to keep the `git` functionality,
allowing you to manually install updates just by running `git pull origin master` from the created directory.

Now you can clone the repository somewhere else and symlink it to Home Assistant like so:

1. Clone the repo.

   ```shell
   git clone https://github.com/Antoni-Czaplicki/SteamVR.HA.git
   ```

2. Create the symlink to `steamvr` in the configuration directory.
   If you have non-standard directory for configuration, use it instead.

   ```shell
   ln -s SteamVR.HA/custom_components/steamvr ~/.homeassistant/custom_components/steamvr
   ```

#### Copy method

1. Download [ZIP](https://github.com/Antoni-Czaplicki/SteamVR.HA/archive/master.zip) with the code.
2. Unpack it.
3. Copy the `custom_components/toyota/` from the unpacked archive to `custom_components`
   in your Home Assistant configuration directory.

</details>

### Integration Setup

- Browse to your Home Assistant instance.
- In the sidebar click on [Configuration](https://my.home-assistant.io/redirect/config).
- From the configuration menu select: [Integrations](https://my.home-assistant.io/redirect/integrations).
- In the bottom right, click on the [Add Integration](https://my.home-assistant.io/redirect/config_flow_start?domain=steamvr) button.
- From the list, search and select “SteamVR”.
- Follow the instruction on screen to complete the set-up.
- After completing, the SteamVR integration will be immediately available for use.

#### Configuration options

If you are experiencing frequent state changes between `standby` and `idle` you can enable `Replace headset standby status with idle` configuration option.

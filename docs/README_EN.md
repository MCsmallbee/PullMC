<div align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="img/logo_dark.svg">
    <img alt="PullMC Logo" src="img/logo.svg" width="100">
  </picture>
<h1>PullMC</h1>

**English** &nbsp;|&nbsp; [简体中文](../README.md) &nbsp;|&nbsp; [日本語](README_JP.md)

<p>Lightweight, clean Minecraft Java Edition version download tool</p>
</div>

> [!IMPORTANT]
> **Important**: A large portion of the code in this project is written using **Vibe Coding**.
>
> If you are averse to such projects, please ignore this project. Thank you.

> [!NOTE]
> The main features of this project are **under development**; currently only the basic UI framework is complete.
>
> **Stay tuned!**

## 📖 Project Overview

PullMC is an open-source, unofficial Minecraft: Java Edition download and deployment tool for players who want a lighter, more transparent way to manage game versions and files.

It focuses on three things:

- Fetching version metadata
- Downloading and verifying game files
- Deploying files to a directory you choose

PullMC does not provide game accounts, a launcher, or multiplayer services, and it does not host or mirror game resources. The desktop app is built with Python, PySide6, QML, and RinUI; it supports Simplified Chinese, Traditional Chinese, English, and Japanese, and follows the Windows theme.

The project is currently in the `base` stage: the desktop UI, first-run onboarding, and settings are complete; the version library, downloads, verification, and deployment are still in development.

## 🗺️ Todo

- [x] Basic window UI layout implementation
- [x] Settings page, About page, localization and version naming
- [ ] Minecraft version manifest fetching and version library
- [ ] Game file downloading, verification and deployment
- [ ] Download task queue and progress
- [ ] Download source, mirror and proxy settings
- [ ] Mod loader and mod downloading
- [ ] Modpack installation support

## ⚠️ Disclaimer

PullMC is an open-source Minecraft: Java Edition download and deployment tool. It only fetches version metadata, downloads game files, and verifies local files; it does not provide game accounts, servers, or multiplayer services.

- This project does not host or operate any game-resource download site, nor does it mirror game files. All download requests are sent directly by your device to the source you select (Mojang's official sources, public mirrors such as BMCLAPI, or loader-official sources) and written to the local directory you choose.
- This project is not affiliated with, endorsed by, sponsored by, or authorized by Microsoft, Mojang Studios, or their affiliates or agents.
- Minecraft is a trademark of Mojang Studios. The project name is used only to describe compatibility and does not imply endorsement by Mojang Studios.
- Before using this project, you must have legally obtained a Minecraft: Java Edition license through official channels and comply with the applicable end-user license agreement.
- This project is provided "as is", without any warranty regarding the availability, stability, or security of third-party download sources. You use it at your own risk.

## ⚖️ License

Copyright (c) 2026 MCsmallbee

This project uses the MIT License. See the [LICENSE](../LICENSE) file for details.

In short: you are free to use, copy, modify, and distribute the code of this project, provided that you retain the copyright notice, and the author assumes no liability.

## ⭐ Star History

<a href="https://www.star-history.com/?repos=mcsmallbee%2Fpullmc&type=date&legend=bottom-right">
 <picture>
   <source media="(prefers-color-scheme: dark)" srcset="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&theme=dark&legend=bottom-right" />
   <source media="(prefers-color-scheme: light)" srcset="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&legend=bottom-right" />
   <img alt="Star History Chart" src="https://api.star-history.com/chart?repos=mcsmallbee/pullmc&type=date&legend=bottom-right" />
 </picture>
</a>

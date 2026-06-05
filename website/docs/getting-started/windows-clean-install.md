---
sidebar_position: 3.5
title: "Windows Clean Install"
description: "A clean, step-by-step Windows install for the latest Lil Skrrt code or the latest release"
---

# Windows Clean Install

Use this guide when you want a clean Windows install that starts from scratch and ends with a verified, up-to-date Lil Skrrt setup.

## What to use

- Use `main` if you want the newest code immediately.
- Use a tagged GitHub release if you want a pinned version.
- If you already had a previous install, clean it out first so you don't inherit stale config or PATH entries.

## Clean removal of an old install

1. Open PowerShell.
2. If Lil Skrrt is already installed, run:
   ```powershell
   lil-skrrt uninstall
   ```
3. Remove the disposable install directory if you want a full reset:
   ```powershell
   Remove-Item -Recurse -Force "$env:LOCALAPPDATA\lil-skrrt" -ErrorAction SilentlyContinue
   ```
4. If you want a truly clean user state as well, back up anything you care about and then remove the data directory:
   ```powershell
   Remove-Item -Recurse -Force "$env:USERPROFILE\.hermes" -ErrorAction SilentlyContinue
   ```

That removes local binaries, portable Git, Node, venv state, and cached installer artifacts. Only do step 4 if you really want to erase config, sessions, memories, and skills.

## Install the latest code from GitHub

1. Open a fresh PowerShell window.
2. Allow the installer script to run for this session only:
   ```powershell
   Set-ExecutionPolicy -Scope Process Bypass -Force
   ```
3. Run the installer directly from the repository on `main`:
   ```powershell
   iex (irm https://raw.githubusercontent.com/SkrrtSkerrt/lil-skrrt/main/scripts/install.ps1)
   ```

This is the fastest way to get the latest code from GitHub.

## Install a pinned release instead

If you want a specific tagged release, use the scriptblock form so you can pass `-Tag`:

```powershell
& ([scriptblock]::Create((irm https://raw.githubusercontent.com/SkrrtSkerrt/lil-skrrt/main/scripts/install.ps1))) -Tag v1.0.1
```

Replace `v1.0.1` with whichever release tag you want from the GitHub Releases page.

## What the installer should do

On a clean machine, the Windows installer should:

- install or reuse Git for Windows / Git Bash
- install `uv`
- install Python 3.11 into a user-scoped venv
- install Node.js 22 when needed
- install `ripgrep` and `ffmpeg`
- clone Lil Skrrt into `%LOCALAPPDATA%\lil-skrrt\hermes-agent`
- set `HERMES_HOME` and `HERMES_GIT_BASH_PATH`
- write the launcher shim into `%LOCALAPPDATA%\lil-skrrt\bin`
- run the first-time setup wizard unless you pass `-SkipSetup`

## Verify the install

After the installer finishes, close PowerShell and open a fresh window, then check:

```powershell
lil-skrrt --version
lil-skrrt doctor
lil-skrrt status
```

If those three commands work, the install landed correctly.

## Common cleanup for a broken install

If you ran into a bad state, the cleanest recovery is:

1. Remove `%LOCALAPPDATA%\lil-skrrt`
2. Remove `%USERPROFILE%\.hermes` only if you want to wipe all data
3. Re-run the installer from `main`
4. Re-open the shell before testing again

## Related pages

- [Installation](./installation.md)
- [Windows (Native) Guide](../user-guide/windows-native.md)
- [Updating & Uninstalling](./updating.md)

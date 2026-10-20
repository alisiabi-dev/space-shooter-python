# Space Shooter (Python + Pygame)

A 2D space-shooter game built independently with Python and Pygame. The player can select a ship, dodge incoming obstacles, fire projectiles, progress through five levels, and face a boss encounter. The game includes custom image and audio assets, score tracking, and win/game-over screens.

## Features

- Three selectable player ships
- Five levels with increasing score targets
- Moving obstacles and player projectiles
- Boss encounter with changing projectile speed
- Sound effects and background audio
- Main menu, information screen, win screen, and game-over screen

## Requirements

- Python 3.11 or another Python version supported by the installed Pygame release
- Pygame (installed from `requirements.txt`)

## Run on Windows

Open PowerShell in this folder and run:

```powershell
py -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe main.py
```

Using the virtual environment's Python executable directly avoids the need to activate the environment in PowerShell.

## Optional: build a Windows executable

On Windows, after installing the project requirements, install PyInstaller and build a standalone executable:

```powershell
.\.venv\Scripts\python.exe -m pip install pyinstaller
.\.venv\Scripts\pyinstaller.exe --noconfirm --onefile --windowed --name SpaceShooter --add-data "Assets;Assets" main.py
```

The executable will be created in `dist/`. Build the Windows executable on Windows, and test it on the target machine before sharing it.

## Run on macOS / Linux

```bash
python3 -m venv .venv
./.venv/bin/python -m pip install --upgrade pip
./.venv/bin/python -m pip install -r requirements.txt
./.venv/bin/python main.py
```

## Controls

- **Arrow keys:** move the player ship
- **Space:** fire a projectile
- **Mouse:** navigate menus and select a ship or level

## Project structure

```text
space-shooter/
├── Assets/
│   ├── Audio/
│   ├── Backgrounds/
│   ├── Levels/
│   ├── Ships/
│   ├── Stones/
│   └── UI/
├── data.py
├── main.py
├── requirements.txt
├── README.md
├── ASSET_NOTES.md
└── .gitignore
```

## Tests

Run the asset-path checks with:

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```

## Notes

- Assets are loaded relative to the project directory, so the game can be launched from another working directory as long as the project files remain together.
- Images and sounds are cached to avoid loading the same files repeatedly during gameplay.
- The project uses original game logic and asset files supplied with the source archive. Confirm you have permission to redistribute every bundled image and sound before making the repository public.
- The supplied archive did not contain a standalone `.exe`; this repository includes the Python source and instructions for building a Windows executable with PyInstaller.

# 🎵 Music Player in Python (Pygame Edition)

A stylish audio player with a custom graphical interface and no standard window borders (Frameless UI), developed in **Python** using the **Pygame** and **Keyboard** libraries.

The application scans a specified directory, automatically converting nested folders into playlists, and supports advanced control via global hotkeys.

---

## ✨ Key Features

* **Frameless UI & Dynamic Background:** A modern minimalist borderless interface with an animated twinkling stars effect in the background.
* **Custom Interactive Cursor:** The system cursor is hidden. Instead, it uses `cursor_static.png` (normal mode) and `cursor_load.png` textures (when hovering over clickable buttons).
* **Smart Playlists:** The player automatically scans the target folder. Each subfolder becomes a separate playlist, and `.mp3`, `.wav`, and `.ogg` files inside it become tracks.
* **Global Hotkeys:** Control playback from anywhere in the system, even if the player window is minimized.
* **"Fixed" Mode:** Ability to loop the current track so it plays continuously instead of automatically switching to the next one.

---

## 🎮 Controls and Hotkeys

You can control the player either with your mouse using the GUI buttons or via the keyboard. Global hotkeys trigger **only when the Ctrl modifier key is held down**.

| Action | GUI Button | Hotkey (Hold `Ctrl` + ...) |
| :--- | :---: | :--- |
| **Pause / Play** | `pause` / `unpause` | `Space` |
| **Next Track** | `>` | `Right` (Right Arrow) |
| **Previous Track** | `<` | `Left` (Left Arrow) |
| **Next Playlist** | `>>` | `Alt` + `Right` |
| **Previous Playlist** | `<<` | `Alt` + `Left` |
| **Volume Up (+10%)** | `+` | `Up` (Up Arrow) |
| **Volume Down (-10%)** | `-` | `Down` (Down Arrow) |
| **Loop / Unloop Track** | `fixed` / `unfixed` | `` ` `` (Tilde Key / Backtick) |

---

## 📂 Project Structure

```text
📁 space-audio-player/
│
├── 📁 build/                   # Pre-compiled application folder
│   ├── 📁 _internal/           # Binary dependencies and core libraries
│   ├── 📄 main.exe             # Executable file for Windows
│   ├── 📄 pygame_addiction.py  # Custom engine wrapper and GUI components
│   ├── 📄 colors.py            # Color palette and converters
│   ├── 📄 data.json            # Configuration file
│   ├── 📄 font.ttf             # Custom font asset for the user interface
│   ├── 🖼️ cursor_static.png    # Normal cursor texture (20x20)
│   └── 🖼️ cursor_load.png      # Hover cursor texture (20x20)
│
├── 📄 main.pyw               # Main player script (UI, playlist logic)
├── 📄 pygame_addiction.py    # Custom engine wrapper and GUI components
├── 📄 colors.py              # Color palette and converters
├── 📄 font.ttf               # Custom font asset for the user interface
├── 🖼️ cursor_static.png      # Normal cursor texture (20x20)
│   📄 data.json              # Configuration file
└── 🖼️ cursor_load.png        # Hover cursor texture (20x20)

```

---

## 🚀 Quick Start

### 📦 Option A: Pre-built Executable (No Python Required)

#### 1. Open the Application Folder
Go straight into the `build` folder.

#### 2. Configuration Setup (`data.json`)
Before running the player for the first time, make sure your `data.json` file points to the correct path of your music collection:

```json
{
    "path": "C:/path/to/your/music/folder",
    ...
}
```

#### 3. Launch the Player
Run `main.exe` from the folder.

---

### 💻 Option B: Running from Source Code (Python Environment)

#### 1. Installing Dependencies
The application requires the `pygame` and `keyboard` libraries. Install them using the terminal commands:

```bash
pip install pygame keyboard
pip install pygame pygame
```

> ⚠️ **Important:** The `keyboard` module intercepts keystrokes globally at the system level. Because of this, on some operating systems (like Linux or under strict Windows policies), running the script with administrator privileges might be required for the hotkeys to work.

#### 2. Configuration Setup (`data.json`)
Before running the player for the first time, make sure your `data.json` file points to the correct path of your music collection:

```json
{
    "path": "C:/path/to/your/music/folder",
    ...
}
```

#### 3. Launching the Player
Run the main file. The `.pyw` extension allows the program to run in the background without opening a black Windows console window:

```bash
python main.pyw
```

---

## 🛠️ Architecture and Custom Modules

* **Safety (`pygame_addiction.py`):** The custom `Root` class catches critical runtime errors inside your `main()` function using a `try-except` block and safely prints them to the console via `input(err.args)`, preventing the program from silently crashing.
* **Palette Testing (`colors.py`):** You can check the display of all built-in colors by running this module directly:

```bash
python colors.py
```

## 🛠️ Troubleshooting

### 1. Global hotkeys are not working
* **Reason:** The `keyboard` library requires low-level system access to intercept keystrokes when the application window is minimized. Windows 11 security policies often block this by default.
* **Solution:** Close the player and run `main.exe` (or your terminal/VS Code) **as Administrator**.

### 2. The player window closes silently without any message
* **Reason:** A corrupted or unsupported audio file layout inside your music directories might be crashing the `pygame.mixer`.
* **Solution:** Check the terminal input prompt. The custom engine wrapper catches runtime exceptions and dumps the crash logs into `input(err.args)` instead of crashing silently.

### 3. Application shows "No playlists found"
* **Reason:** The path specified in your local `data.json` file is incorrect, or the folder does not contain any subdirectories.
* **Solution:** Open `data.json` and verify that the `"path"` value uses proper forward slashes (e.g., `C:/Users/Name/Music`) and points to folders containing `.mp3`, `.wav`, or `.ogg` tracks.

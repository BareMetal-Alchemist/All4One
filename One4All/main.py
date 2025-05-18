import os
import re
import json
import tkinter as tk

def parse_vdf(filepath):
    try:
        with open(filepath, encoding='utf-8') as f:
            text = f.read()

        # Grab all paths that look like directories
        # New Steam format example: "path"  "D:\\SteamLibrary"
        paths = re.findall(r'"path"\s+"(.*?)"', text)
        if not paths:
            # fallback default Steam install location
            return ['C:\\Program Files (x86)\\Steam']
        return paths
    except Exception as e:
        print(f"Error parsing libraryfolders.vdf: {e}")
        return ['C:\\Program Files (x86)\\Steam']

def parse_manifest(manifest_path):
    try:
        with open(manifest_path, encoding='utf-8') as f:
            data = f.read()

        name_match = re.search(r'"name"\s+"(.+?)"', data)
        install_dir_match = re.search(r'"installdir"\s+"(.+?)"', data)

        if name_match and install_dir_match:
            return {
                "name": name_match.group(1),
                "install_dir": install_dir_match.group(1),
                "manifest_path": manifest_path
            }
    except Exception as e:
        print(f"Error reading {manifest_path}: {e}")
    return None

def get_steam_games():
    steam_path = "C:\\Program Files (x86)\\Steam"
    vdf_path = os.path.join(steam_path, "steamapps", "libraryfolders.vdf")
    libraries = parse_vdf(vdf_path)

    games = []

    for lib in libraries:
        steamapps = os.path.join(lib, "steamapps")
        if not os.path.exists(steamapps):
            print(f"Skipping invalid path: {steamapps}")
            continue
        for file in os.listdir(steamapps):
            if file.startswith("appmanifest") and file.endswith(".acf"):
                manifest_path = os.path.join(steamapps, file)
                game = parse_manifest(manifest_path)
                if game:
                    game["full_path"] = os.path.join(lib, "steamapps", "common", game["install_dir"])
                    games.append(game)

    return games

games = get_steam_games()
print("Installed Steam Games:")
for game in games:
    print(f"- {game['name']} at {game['full_path']}")
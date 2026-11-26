SURVIVAL WORLD — browser/mobile prototype

PROJECT FILES
- index.html: main GitHub Pages entry point. Upload this file to the root of the SurvivalWorld repository and replace the previous index.html.
- SurvivalWorld.html: matching backup copy of the main page.
- SurvivalWorld-devlog.txt: development journal.
- test-survivalworld.py: static and JavaScript syntax checks (requires Python 3 and Node.js).
- MULTIPLAYER-NOTES.md: current multiplayer/security status and next architecture steps.

PUBLISH TO GITHUB PAGES
1. Open https://github.com/ssoriniulian-lang/SurvivalWorld
2. Add file -> Upload files.
3. Upload the new index.html and choose to replace the existing file.
4. Commit changes.
5. Wait for GitHub Pages deployment.

PLAY LINK
https://ssoriniulian-lang.github.io/SurvivalWorld/

CONTROLS
- PC: WASD or arrow keys to move; E collect; Space attack; F place building; B use bandage.
- Mobile: left joystick moves the player; drag on the right side of the 3D view to rotate the camera; on-screen buttons perform actions.

CURRENT PROTOTYPE FEATURES
- Third-person Three.js scene, day/night cycle and procedural resource nodes.
- Articulated, procedurally generated human-like player and zombie models with basic walk/attack motion.
- Zombie chase and contact damage; melee combat; axe and spear crafting.
- Wood, stone, food, hunger, health, bandages, XP, levels and missions.
- Craftable walls, doors, storage chests and campfires.
- Chests can store and return wood, stone and food when the player stands nearby.
- Local save/load includes collected resources, inventory, placed structures, chest contents and camera orientation.
- Local-only records, survival race, resource contest, practice duel and unlockable outfit colors.

IMPORTANT LIMITATIONS
This is still a single-player prototype, not a finished commercial game. The models are procedural and stylized rather than photorealistic scanned assets. The local leaderboard is stored only in this browser/device; it is not an online leaderboard. PvP, online tournaments, accounts, authoritative anti-cheat and real multiplayer servers are not implemented. Three.js is loaded from jsDelivr, so the browser needs internet access. Browser rendering and touch behavior still require a live-device test after publication; this environment blocks local Chromium navigation, so only syntax/static tests were verified in this run.

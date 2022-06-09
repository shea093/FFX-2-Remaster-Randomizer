## Pre-requisites
- Dressphere randomization currently only works when playing the game on ***English***. Hard Mode works on all languages.
- You need [VBFBrowser](https://www.nexusmods.com/finalfantasy12/mods/3) to inject the files.

### Warning
Installation isn't particularly user-friendly, and I recommend that you backup your "FFX2_Data.vbf" file if you aren't confident. (Unfortunately this file is very big)
This will overwrite values in your game that will be present even if you reload your old saved games. I highly recommend only using this for a fresh New Game save. 

## Randomization features
- Dressphere abilities
- Dressphere "Ability Trees" (abilities that unlock other abilities are randomized)
- Dressphere stat growths
#### Dressphere "Spoiler" Tool 
Can be used to view abilities + their required abilities in their respective "learning trees". This is currently in a very early state and doesn't have much functionality other than that.

## Edited abilities to prevent randomization being overpowered
- Nerfs to normal attacks (0.6x)
- Nerfs to some strong abilities
- Big potency nerfs to ignore-defence attacks such as Sparkler
- Most magic now uses the "Special Magic" formula, which means it'll be comparable to Phys damage in endgame

## Hard-Mode Enemy differences
I highly recommend using this to prevent the game from being too easy, as getting overpowered skills is always a possibility. I have tested this up to early Chapter 5 and it never reaches insane difficulty, but is probably decently challenging depending on what your seed gives you.
- 0.5x EXP (This is the most severe difference, doing sidequests made it too easy to become overpowered)
- 2.45x HP
- 0.7x DEF and MDEF (Indirect nerf on Ignore-Defence abilities, compensated with more HP)
- 1.5x STR
- 1.7x MAG
#### Other hard mode differences
- Most skills require ~1.6x more AP to learn
- All captured creatures are also nerfed and size S, and none have overpowered stats. These stat growths are also randomized but with a cap that prevents them from having uber stats before feeding them.



# Installation instructions
(Make sure you know which directory the .exe file is in)
1. Open "FFX-2 Randomizer.exe" and set the seed to any integer of your choosing (option 4). 
2. Pick one of the executable options of your choosing (1, 2, or 3)
3. A folder with the seed name should be made with a "ffx_ps2" folder inside of it
4. Open VBFBrowser. As far as I'm aware, this is the only way to inject the files right now. Download here https://www.nexusmods.com/finalfantasy12/mods/3
![image](https://user-images.githubusercontent.com/66511873/172754711-b0e1c734-7645-4fb8-9189-1b5dbda96944.png)
5. Press the "Open" button on the top left and navigate to where the ***FFX2_Data.vbf*** file is, and open it.
It should be in the **<steamprogramfolder>\steamapps\common\FINAL FANTASY FFX&FFX-2 HD Remaster\data** directory. 
![image](https://user-images.githubusercontent.com/66511873/172755083-0ffceadf-c7c4-419f-aaae-f9d7f7a99de7.png)
6. Collapse the tree view on the Left Pane (click the "+" icon) and then click on "ffx_ps2" so it turns blue. The window should now look like this:
7. Click the "Inject" button at the bottom of the Left Pane. When you get a prompt for "Are you injecting a whole folder?", click ***Yes***.
![image](https://user-images.githubusercontent.com/66511873/172756531-45411596-c592-49ca-9cd7-aa25931cfc8c.png)
8. Navigate to where your seed output folder is, and click on the "ffx_ps2" folder so it turns blue. Do NOT click on the seed number folder, as you want to match the folder name shown in the VBF Browser view ("ffx_ps2")
9. Press OK and wait until you see a "Done." dialogue box. 
  
You can click "Log" on the bottom-right of the program to see if it actually patched anything. It should should look something like this:
  ![image](https://user-images.githubusercontent.com/66511873/172756681-b3febc1d-f6a8-4f82-a766-13fd03b08626.png)

## Resetting game back to the default state
If you want to delete the modded binaries from your game and restore the defaults, then follow these same instructions but choose the "Get default files (Reset)" option. The default files will be in a folder called "reset", and you can inject the ffx_ps2 folder from it.

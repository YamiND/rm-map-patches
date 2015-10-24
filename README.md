Info
==============

Extensions for Nexuiz maps to be used with the [RocketMinsta](https://github.com/nexAkari/RocketMinsta) mod. These patches are entirely server-side and don't require clients to download anything. They alter the placement of entities only, modifying the map layout this way is impossible. To install these on your server, simply copy the **maps** folder into your Nexuiz data directory (typically ~/.nexuiz/data/), or place them selectively.

List of alterations (alphabetical order):
* **blackcathedral-cra_v3**: Added a Nadget pickup [_Akari_]
* **castle-beta2**: Fixed the angle of the terminal in the blue base, set "spawninarena" "1" for the tuba.  [_Hanzo_]
* **cpm19_nex_r1**: Added mapinfo, enabled g_walljump_playerclip [_J0k3r_]
* **desertfactory**: Added teamspawnpoints, buffs, terminals, dom-cps; removed the secret door. [_Hanzo_]
* **dieselpower**: Added a Nadget pickup [_Akari_]
* **dustylolis-beta6**: Added Buffs, added netnames for Jailbreak control points. [_Akari_]
* **dusty_v2**: Made it fun 30% of the time. [_Akari_]
* **EquinoxV1R4**: Added: 10 teamspawnpoints/team, 4 buffs/team, 1 common buff in the middle, 6 domination controlpoints [_Hanzo_]
* **Japanese_Castles_q3wcp1**: Removed func_trains (they were as broken as the room they lead to) [_Akari_]
* **medieval**: Added Buffs. Note: this patch is for medieval_v1r0 (accident doesn't like to version his maps) [_Hanzo_]
* **oilrig-beta2**: Set "spawninarena" "1" for the tuba.  [_Hanzo_]
* **ospdm8_nex_r1**: Added Buffs, Terminal [_J0k3r_]
* **phantq3dm3_nex**: Added mapinfo, enabled g_walljump_playerclip [_J0k3r_]
* **q2edge-nex-beta6**: Added Buffs, added 2 extra Domination control points, fixed a blue Jailbreak controlpoint having no target [_Akari_]
* **q2warehouse-jb-beta3**: Fixed missing Red Arc Buff spawn [_Akari_]
* **q2warehouse-jb-beta4**: Added Nadget pickups [_Akari_]
* **q2warehouse-nex-beta2**: Added Buffs, added Terminals, sealed jail doors for non-Jailbreak gametypes. [_Akari_]
* **q3dust2-jb-beta4**: Added Buffs. [_Akari_]
* **roof-beta2**: Added: 2 buffs/team, 2 terminals, more pickups (health/armor); now 7 dom-cps, 2 red jb-cps, 2 blue jb-cps, 1 neutral jb-cp; [_Hanzo_]
* **showdown_v2r0**: Added additional Jailbreak control points. [_Akari_]
* **silvercity**: Remove global fog [_J0k3r_]
* **solarae-nex-v2**: Move Terminals to more hidden locations [_J0k3r_]
* **tortured**: Added mapinfo, enabled g_walljump_playerclip [_Akari_]
* **vectorwars-jb-beta2**: Fixed CTF flag spawns (for VIP soulgems, they were unreachable) [_Hanzo_]
* **warehouse-beta15**: Removed the cosmetic blue lasers to save some FPS [_Akari_]:
* **whorehouse**: fixed a secret button missing the NOSPLASH spawnflag [_Akari_]

Contributing
==============

If you want to contribute, you will need to have some basic **NetRadiant** skills. To make a new patch, you need to edit the source **.map** file and make your changes, modify entities only. If the map you're editing doesn't have a .map file in the pk3, you can decompile the BSP:

    q3map2 -game nexuiz -convert -format map mapname.bsp

Decompiling isn't 100% accurate, but it will keep ingame entities intact, which is the only thing you're interested in. When you're finished editing, you can use the **map2ent.py** script found in this repository to generate the .ent file:

    ./map2ent.py rip mapname.map mapname.ent

Alternatively, you can compile the new entity data into the bsp, run it in Nexuiz and use the **sv_saveentfile** command. It will save the .ent file to ~/.nexuiz/data/maps/.

If you want to modify an already existing patch, you have to apply it to the original/decompiled .map and then proceed with editing it and generating a new .ent file. Use the following command to do that:

    ./map2ent.py fuse mapname.map mapname.ent newmapname.map

**WARNING:** maps using the **func_group** pseudo-entity are not yet supported and will most likely end up broken!

After you're finished, [fork](https://help.github.com/articles/fork-a-repo) the repository unless you've already done so and [send me a pull request](https://help.github.com/articles/using-pull-requests). It's prefered that you test your patch before that, but it's not required because I will do it anyway. To test, you will need to have the latest unstable version of [RocketMinsta](https://github.com/nexAkari/RocketMinsta) installed. You can get an autobuild [here](http://rocketminsta.net/) if you don't want to compile it yourself (if it hangs, try again).

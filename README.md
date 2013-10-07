Info
==============

Extensions for Nexuiz maps to be used with the [RocketMinsta](https://github.com/nexAkari/RocketMinsta) mod. These patches are entirely server-side and don't require clients to download anything. They alter the placement of entities only, modifying the map layout this way is impossible. To install these on your server, simply copy the **maps** folder into your Nexuiz data directory (typically ~/.nexuiz/data/), or place them selectively.

List of alterations (alphabetical order):
* **dustylolis-beta6**: Added Buffs, added netnames for Jailbreak control points. [_Akari_]
* **medieval**: Added Buffs. Note: this patch is for medieval_v1r0 (accident doesn't like to version his maps) [_Hanzo_]
* **q2warehouse-nex-beta2**: Added Buffs, sealed jail doors for non-Jailbreak gametypes. [_Akari_]
* **q3dust2-jb-beta4**: Added Buffs. [_Akari_]
* **showdown_v2r0**: Added additional Jailbreak control points. [_Akari_]

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

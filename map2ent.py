#!/usr/bin/env python2

import sys

# Converts a Quake map to an .ent file by stripping all brush data, leaving just the entity definitions.
# This is silly and relies on NetRadiant's formatting, it doesn't properly parse the map.
# Preserves references to brush models, so stuff like doors and triggers should work.

M_NOTHING, M_ENTITY, M_BRUSH = range(3)
def map2ent(mapdata, stripclasses=["light"]):
    mode = M_NOTHING
    entdata = ""
    entbuf = ""
    model = 1
    entnum = 0
    level = 0
    modelfound = False
    skipent = False
    
    for line in mapdata.split("\n"):
        line = line.strip()
        
        if not line:
            continue
        
        if mode == M_NOTHING:
            if line.startswith("// entity"):
                mode = M_ENTITY
                entbuf = ""
                skipent = False
                continue
            else:
                raise Exception("Got garbage while looking for entity: " + repr(line))
        elif mode == M_ENTITY:
            if line.startswith("// brush"):
                mode = M_BRUSH
                if entnum and not modelfound:
                    entbuf += '"model" "*%i"\n' % model
                    model += 1
                modelfound = True
                continue
            elif line == "}":
                mode = M_NOTHING
                modelfound = False
                entnum += 1
                
                if not skipent:
                    entdata += entbuf + line + "\n"
            elif not skipent and line.startswith('"classname"') and line[13:-1] in stripclasses:
                skipent = True
            
            entbuf += line + "\n"
        elif mode == M_BRUSH:
            if line == "}":
                level -= 1
                if level < 1:
                    mode = M_ENTITY
            elif line == "{":
                level += 1
            continue
    
    return entdata

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.stderr.write("Usage: %s input.map [output.ent]\n" % sys.argv[0])
        exit(1)
    
    with open(sys.argv[1], "r") as mapfile:
        ent = map2ent(mapfile.read())
        if len(sys.argv) > 2:
            with open(sys.argv[2], "w") as output:
                output.write(ent)
        else:
            sys.stdout.write(ent + "\n")
    

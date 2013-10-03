#!/usr/bin/env python2

import sys, re

Q3MAP2_ENTITIES = ["light", "lightJunior", "misc_model", "func_group", "_decal", "_skybox"]

# Converts a Quake map to an .ent file by stripping all brush data, leaving just the entity definitions.
# This is silly and relies on NetRadiant's formatting, it doesn't properly parse the map.
# Preserves references to brush models, so stuff like doors and triggers should work.

M_NOTHING, M_ENTITY, M_BRUSH = range(3)
def map2ent(mapdata, stripclasses=Q3MAP2_ENTITIES):
    mode = M_NOTHING
    entdata = ""
    entbuf = ""
    model = 1
    entnum = 0
    level = 0
    modelfound = False
    skipent = False
    
    for n, line in enumerate(mapdata.split("\n")):
        line = line.strip()
        
        if not line or line.startswith("//"):
            continue
        
        if mode == M_NOTHING:
            if line == "{":
                mode = M_ENTITY
                entbuf = line + "\n"
                skipent = False
                continue
            else:
                raise Exception("Got garbage on line %i (level %i) while looking for entity: %s" % (n, level, repr(line)))
        elif mode == M_ENTITY:
            if line == "{":
                mode = M_BRUSH
                level += 1
                if entnum and not modelfound and not skipent:
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

# Grabs brush data from a Quake map and returns it as a list
# The indicies are the same as the numbers specified by the 'model' keys in the ent file and the values are the raw brush definitions
# Worldspawn brushes have an index of 0

def getbrushes(mapdata):
    level = 0
    bnum = 0
    buf = ""
    brushes = []
    
    for n, line in enumerate(mapdata.split("\n")):
        line = line.strip()
        
        if not line or line.startswith("//"):
            continue
            
        if line == "{":
            level += 1
            
            if level == 2:
                line = "// brush %i\n%s" % (bnum, line)
                bnum += 1
        
        if level > 1:
            buf += line + "\n"
        
        if line == "}":
            level -= 1
            if level < 0:
                raise Exception("Unmatched '}' on line %i" % n)
            elif level < 1 and buf:
                brushes.append(buf)
                buf = ""
                bnum = 0
                
    return brushes

def fuse(mapdata, entdata, preserve=Q3MAP2_ENTITIES):
    brushes = getbrushes(mapdata)
    finaldata = ""
    buf = ""
    inent = 0
    enum = 0
    mnum = 0
    skipent = False
    
    mexpr = re.compile('"model" "\*([0-9]+)"')
    
    # First, we will go over entfile and populate it with brushes from the map
    
    for n, line in enumerate(entdata.split("\n")):
        line = line.strip()
        
        if not line or line.startswith("//"):
            continue
        
        if line == "{":
            if inent:
                raise Exception("Nested { in ent file on line %i" % n)
            buf += "// entity %i\n" % enum
            inent = True
            mnum = 0
        elif line == "}":
            if not inent:
                raise Exception("Unmatched } in ent file on line %i" % n)
            inent = False
            
            if not enum or mnum:        # worldspawn is special: it's not going to have a model key in the ent file, but will always have brushes.
                buf += brushes[mnum]
            
            finaldata += buf + line + "\n"
            buf = ""
            enum += 1
            continue
        elif inent:
            if line.startswith('"classname"'):
                cls = line[13:-1]
                if cls in preserve:
                    preserve.remove(cls)
            else:
                o = mexpr.findall(line)
                if o:
                    mnum = int(o[0])
                    continue
        else:
            raise Exception("Got garbage on line %i while looking for entity in entfile: %s" % (n, repr(line)))
        
        buf += line + "\n"
    
    # Now, we're going to copy specific entities such as lights from the original map
    
    inent = 0
    buf = ""
    for n, line in enumerate(mapdata.split("\n")):
        line = line.strip()
        
        if not line or line.startswith("//"):
            continue
        
        if line == "{":
            inent += 1
            buf = line + "\n"
            skipent = True
            continue
        elif line == "}":
            inent -= 1
            if not inent:
                if not skipent:
                    finaldata += ("// entity %i\n" % enum) + buf + line + "\n"
                    enum += 1
                    continue
        elif not inent:
            raise Exception("Got garbage on line %i while looking for entity in mapfile: %s" % (n, repr(line)))
        elif skipent and line.startswith('"classname"') and line[13:-1] in preserve:
            skipent = False
        
        buf += line + "\n"
    
    return finaldata

def usage():
    sys.stderr.write("""
Usage: %s rip input.map [output.ent]
            Generates an .ent file out of a given map. 
            Will try to not save q3map2-specific entities, but will keep q3map2-specific keys.
                                       
       %s fuse input.map input.ent [output.map]
            Replaces all entities in a map using the provided ent file. 
            This will destroy all q3map2-specific keys unless they are present in the ent file.
            Will try to preserve q3map2-specific entities, such as light and misc_model, unless they are present in the ent file.
            WARNING: maps using func_group are currently not supported and will end up broken!
       
       If output is not specified, will write to stdout.
""" % (sys.argv[0], sys.argv[0]))
    exit(1)

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        usage()
    
    data = ""
    cmd = sys.argv[1]
    outfile = None
    
    if cmd == "rip":
        with open(sys.argv[2], "r") as mapfile:
            data = map2ent(mapfile.read())        
        if argc > 3:
            outfile = sys.argv[3]
    elif cmd == "fuse":
        if argc < 4:
            usage()
        
        with open(sys.argv[2], "r") as mapfile:
            with open(sys.argv[3], "r") as entfile:
                data = fuse(mapfile.read(), entfile.read())
                
        if argc > 4:
            outfile = sys.argv[4]
    else:
        usage()
    
    if outfile is None:
        sys.stdout.write(data + "\n")
    else:
        with open(outfile, "w") as fp:
            fp.write(data + "\n")
            

import re
re_id_illegal = re.compile("[^a-z^\d^A-Z]+")
def id_create(filename, type_,id_):
    if id_ is not None:
        if ":" in id_:
            values = id_.split(":")
            type_ = values[0]
            name = "_".join(values[1:])
        elif type_ is not None:
            name = id_
        else:
            print (filename, "type not defined for",id)
            sys.exit()
    else:
        print (filename, "id not defined")
        sys.exit()
    if type_ == "presentation":
        type_ = "media"

    if type_ == "person":
        if "__" in name or "," in name:
            if "__" in name:
                names = name.split("__")
            else:
                names = name.split(",")
            for i,name in enumerate(names):
                name = re_id_illegal.sub("_",name)
                names[i] = re.sub("_+$","",re.sub("^_+","",name))
        else:
            parts = name.split("_")
            for i,part in enumerate(parts):
                parts[i] = re_id_illegal.sub("_",part)
            
            if len(parts) > 1:
                names = [parts[0],"_".join(parts[1:])]
            else:
                names = parts
        name = "__".join(names)

    else:
        name = re_id_illegal.sub("_",name)
        name = re.sub("_+$","",re.sub("^_+","",name))
    return type_.lower()+":"+name.lower()

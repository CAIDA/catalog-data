import re
import sys
import traceback
import unidecode
import json

re_id_illegal = re.compile("[^a-z^\d^A-Z]+")

def id_create(filename, type_,id_):
    id_ = unidecode.unidecode(id_)

    if id_ is not None:
        if ":" in id_:
            values = id_.split(":")
            type_ = values[0]
            name = "_".join(values[1:])
        elif type_ is not None:
            name = id_
        else:
            raise Exception(filename+" "+id_+" has key 'type, but 'type' is None")
    else:
        raise Exception(filename+" id is None")

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

person_seen = {}
person_seen_fname = {}

def person_seen_add(fname,person):
    #if "id" in person:
    #    person_seen[person["id"]] = person
    
    names = [person]
    if "names" in person:
        for name in person["names"]:
            names.append(name)
            
    for name in names:
        i = id_create(fname, "person", name["nameLast"].lower()+"__"+name["nameFirst"].lower())
        if i not in person_seen:
            person_seen[i] = person
            person_seen_fname[i] = fname
        else:
            print ("duplicate",person["id"])
            print ("    ",person_seen_fname[i])
            print ("    ",fname)


def person_seen_check(nameLast, nameFirst):
    ## Check for names and if in names, return the person_seen's id, not the name
    #n = nameLast.lower()+";"+nameFirst.lower()
    i = id_create("", "person", nameLast+"__"+nameFirst)
    if i in person_seen:
        return person_seen[i]
    return None


re_year = re.compile("^\s*(\d\d\d\d)[^\d]*(.*)")
re_num = re.compile("(\d{1,2})[^\d]*(.*)")

def date_parse(value):
    t = type(value)
    if t != str:
        return None
    m = re_year.search(value)
    if m:
        year, rest = m.groups()
        mon, day = None, None
        m = re_num.search(rest)
        if m:
            mon, rest = m.groups()
            if len(mon) < 2:
                mon = "0"+mon
            m = re_num.search(rest)
            if m:
                day, rest = m.groups()
                if len(day) < 2:
                    day = "0"+day
                return year+"-"+mon+"-"+day
            else:
                return year+"-"+mon
        else:
            return year
    return None


re_section = re.compile("^\s*([=~]{3})\s*(.+)")
re_tool = re.compile("^tool[_-]")
re_not_white_space = re.compile(r"[^\s]")
re_html = re.compile(r"\.html$", re.IGNORECASE)
re_md = re.compile(r"\.md$", re.IGNORECASE)

def parse_markdown(filename):
    section_ender = None
    section_format = None
    section_name = None
    section_buffer = None

    metadata = None
    with open(filename) as file:
        for line in file:
            #print (section_name, section_ender,"|",line.rstrip())
            # everything after '=== content ===' is placed inside content unprocessed
            if section_buffer is not None:
                if section_ender == line.rstrip():
                    if "metadata" == section_name:
                        try:
                            metadata = json.loads(section_buffer)
                            metadata["filename"] = filename
                        except json.decoder.JSONDecodeError as e:
                            print ("   json parse error in metadata",filename, e,file=sys.stderr)
                            return None
                    elif metadata is None:
                        print("found section '"+line.rstrip()+"' before '~~~metadata' in",filename, file=sys.stderr)
                        return None
                    else:
                        section_process(metadata, section_ender, section_name, section_buffer, section_format)
                    section_name = None
                    section_buffer = None
                    section_ender = None
                    section_format = None
                else:
                    section_buffer += line
            ## This is equivalent to ===tabs=content
            elif "=== content ===" == line.rstrip():
                section_ender = "==="
                section_name = "tabs=content"
                section_buffer = ""
                section_format = "html"
            else:
                m = re_section.search(line)
                if m:
                    # split group 2 by semi colon
                    split_group = m.group(2).split(";")
                    # if there is a semi colon, there is a specified format
                    if len(split_group) > 1:
                        section_name =  split_group[0].strip()
                        if split_group[1].split("=")[0] == "format":
                            section_format = split_group[1].split("=")[1].strip()
                            if section_format not in ["html", "markdown", "text"]:
                                print(f'\nWARNING: Unrecognized format "{section_format}" in {filename}, acceptable formats are markdown, html, or text')
                                section_format = "html"
                        else:
                            print(f'\nWARNING: Unrecognized parameter "{split_group[1].split("=")[0]}" in {filename} tab')
                            section_format = "html"
                    else:
                        # default format is html
                        section_format = "html"
                        section_name = m.group(2)
                    section_buffer = ""
                    section_ender = m.group(1)

        ## Adds content tab
        if section_buffer is not None:
            if re_not_white_space.search(section_buffer):
                section_process(metadata, section_ender, section_name, section_buffer, section_format)
            else:
                print(f'   DID NOT ADD empty: {section_name:25} tab in {filename}' )
        ## adds each file as a tab
        if "files" in metadata:
            for name,content in metadata["files"].items():
                ## set format as text for files
                ## TODO: Add different file formats based on file extension
                if re_not_white_space.search(content):
                    section_process(metadata, "~~~", "tabs~"+name, content, "text")
                else:
                    print(f'   DID NOT ADD empty: {name:25} tab in {filename}' )  
        
        if "tabs" in metadata:
            tabs = []
            for tab in metadata["tabs"]:
                if re_not_white_space.search(tab["content"]):
                    tabs.append(tab)
                else:
                    print(f'   DID NOT ADD empty: {tab["name"]:25} tab in {filename}' )

            if len(tabs) > 0:
                metadata["tabs"] = tabs

    return metadata

def section_process(metadata, ender, name, buffer, format):
    if name[:5] == "tabs"+ender[0]:
        if "tabs" not in metadata:
            metadata["tabs"] = []
        
        f = "text"
        ## set format if it doesn't exist, (would not exist for files that turned into tabs)
        if format is not None:
            f = format
        metadata["tabs"].append({
            "name":name[5:],
            "format":f,
            "content":buffer
        })
    else:
        current = metadata
        parts = name.split(ender[0])
        i = 0
        while i < len(parts)-1:
            if parts[i] not in current:
                current[parts[i]] = {}
            current = current[parts[i]]
            i += 1
        name = parts[-1]
        if name in current:
            value = current[name]
            if type(value) == "list":
                value.append(buffer)
            else:
                current[name] = [value, buffer]
        else:
            current[name] = buffer

import re
import sys
import traceback
import unidecode
import json
import yaml
from jsonschema import validate

re_id_illegal = re.compile("[^a-z^\d^A-Z]+")

def id_create(filename, type_, id_=None):
    if id_ is None:
        raise Exception(filename+" id is None")

    id_ = unidecode.unidecode(id_)
    if ":" in id_:
        values = id_.split(":")
        type_ = values[0]
        name = "_".join(values[1:])
    elif type_ is not None:
        name = id_
    else:
        raise Exception(filename+" "+id_+" has key 'type, but 'type' is None")

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
    section_name = None
    section_buffer = None

    obj = None
    with open(filename) as file:
        for line in file:
            #print (section_name, section_ender,"|",line.rstrip())
            # everything after '=== content ===' is placed inside content unprocessed
            if section_buffer is not None:
                if section_ender == line.rstrip():
                    if "metadata" == section_name:
                        try:
                            obj = json.loads(section_buffer)
                            obj["filename"] = filename
                        except json.decoder.JSONDecodeError as e:
                            print ("   json parse error in metadata",filename, e,file=sys.stderr)
                            return None
                    elif obj is None:
                        print("found section '"+line.rstrip()+"' before '~~~metadata' in",filename, file=sys.stderr)
                        return None
                    else:
                        section_process(filename, obj, section_ender, section_name, section_buffer)
                    section_name = None
                    section_buffer = None
                    section_ender = None
                else:
                    section_buffer += line
            elif "=== content ===" == line.rstrip():
                section_ender = "==="
                section_name = "tabs=content"
                section_buffer = ""
            else:
                m = re_section.search(line)
                if m: 
                    section_ender = m.group(1)
                    section_name = m.group(2)
                    section_buffer = ""

        if section_buffer is not None:
            section_process(filename, obj, section_ender, section_name, section_buffer)

        if "files" in obj:
            for name,content in obj["files"].items():
                if type(content) == str and re_not_white_space.search(content):
                    section_process(filename, obj, "~~~", "tabs~"+name, content)

        if "tabs" in obj:
            tabs = []
            for tab in obj["tabs"]:
                if re_not_white_space.search(tab["content"]):
                    tabs.append(tab)
                else:
                    warning_add(filename,f'tab empty named:{tab["name"]}' )

            if len(tabs) > 0:
                obj["tabs"] = tabs
            else:
                del obj["tabs"]
    return obj

def section_process(filename, obj, ender, name, buffer):
    data = {} 
    if ";" in name:
        name_old = name
        key_values = name.split(";")
        name = key_values[0]
        for key_value in key_values[1:]:
            if "=" not in key_value:
                error_add(filename,"unable to parse key_value in "+name_old)
                sys.exit(-1)
            key, value = key_value.split("=")
            data[key] = value

    if "format" in data:
        f = data["format"].lower()
        if f == "yaml":
            try: 
                tables = []
                for table in list(yaml.load_all(buffer,Loader=yaml.Loader)):
                    tables.append(table)
            except Exception as e:
                error_add(filename, "YAML:"+e.__str__())
                return 

            for table in tables:
                try:
                    if name.lower() == "datatables":
                        validate(instance={}, schema=table)
                except Exception as e:
                    error_add(filename, "YAML:"+e.__str__())
                    return 
            buffer = tables

        elif f == "fields":
            buffer = fields_parser(filename, buffer)
            if buffer is None:
                return
            

    if name[:5] == "tabs"+ender[0]:
        if "tabs" not in obj:
            obj["tabs"] = []

        data["name"] = name[5:]
        data["content"] = buffer
        if "format" not in data:
            f = "text"
            if ender[0] == "=":
                f = "html"
            elif ender[0] == "~":
                f = "text"
            elif re_html.search(buffer):
                f = "html"
            elif re_md.search(buffer):
                f = "markdown"
            data["format"] = f
        else:
            data["format"] = data["format"].strip()
        obj["tabs"].append(data)
    else:
        current = obj
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

def fields_parser(filename, buffer):
    try: 
        tables = []
        for table in yaml.load_all(buffer,Loader=yaml.Loader):
            fields = []
            if "fields" in table:
                fields_parser_helper(table["fields"],"",fields)
            if len(fields) > 0:
                table["fields"] = fields
                if "anchors" in table:
                    del table["anchors"]
                tables.append(table)
            else:
                if "name" in table:
                    error_add(filename, "field's table: "+table["name"]+" has no fields")
                else:
                    error_add(filename, "field's table has no name or fields")
        if len(tables) > 0:
            return tables
        else:
            return None
    except Exception as e:
        error_add(filename, "YAML:"+e.__str__())
        return None

def fields_parser_helper(fields_dic,label,fields):
    for key,value in fields_dic.items():
        if key[0] == ".":
            if type(value) is dict:
                fields_parser_helper(value,label+key,fields)
            else:
                field = {
                    "name":label+key
                }
                if value != "_":
                    field["dataType"] = value
                fields.append(field)

###########################
filename_errors = {}
def error_add(filename, message):
    if filename not in filename_errors:
        filename_errors[filename] = []
    filename_errors[filename].append(["  error",message])

def warning_add(filename, message):
    if filename not in filename_errors:
        filename_errors[filename] = []
    filename_errors[filename].append(["warning",message])

def error_print():
    if len(filename_errors) > 0:
        print ("")

    for filename,type_messages in filename_errors.items():
        print (filename)
        for t,m in type_messages:
            if "error" in t:
                color_code = "31" # red
            else:
                color_code = "1" # black
            print ("    \033["+color_code+"m",t+":",m,"\033[0m")

    if len(filename_errors) > 0:
        print ("")


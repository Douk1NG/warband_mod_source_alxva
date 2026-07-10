# -*- coding: utf-8 -*-
import os
import re

def parse_scripts_list(filepath):
    with open(filepath, 'r') as f:
        content = f.read()

    # Find where 'scripts = [' starts
    match = re.search(r'^scripts\s*=\s*\[\s*\n', content, re.MULTILINE)
    if not match:
        raise Exception("Could not find 'scripts = [' in " + filepath)
    
    start_idx = match.end()
    preamble = content[:start_idx]
    
    # We now parse the list elements. 
    # An element starts with '(' and ends with the matching ')'.
    # We also want to capture preceding comments/whitespace.
    
    elements = []
    i = start_idx
    length = len(content)
    
    while i < length:
        # Find the next '(' or ']' (end of list)
        # We must skip comments and strings.
        
        # Simple parser to find the start of the next tuple or end of list
        start_of_element = i
        in_string = False
        string_char = ''
        in_comment = False
        bracket_level = 0
        element_str = ""
        
        # Fast forward to next '(' that is at bracket_level 0, or ']'
        found_start = False
        while i < length:
            c = content[i]
            if in_comment:
                if c == '\n':
                    in_comment = False
                i += 1
                continue
            if in_string:
                if c == '\\':
                    i += 2
                    continue
                if c == string_char:
                    in_string = False
                i += 1
                continue
            
            if c == '#':
                in_comment = True
                i += 1
                continue
            if c in ('"', "'"):
                in_string = True
                string_char = c
                i += 1
                continue
                
            if c == '(':
                found_start = True
                break
            elif c == ']':
                # End of scripts list
                break
            i += 1
            
        if not found_start:
            break
            
        # We found '(', now find matching ')'
        tuple_start_idx = i
        bracket_level = 1
        i += 1
        while i < length and bracket_level > 0:
            c = content[i]
            if in_comment:
                if c == '\n':
                    in_comment = False
                i += 1
                continue
            if in_string:
                if c == '\\':
                    i += 2
                    continue
                if c == string_char:
                    in_string = False
                i += 1
                continue
            
            if c == '#':
                in_comment = True
                i += 1
                continue
            if c in ('"', "'"):
                in_string = True
                string_char = c
                i += 1
                continue
                
            if c == '(':
                bracket_level += 1
            elif c == ')':
                bracket_level -= 1
            i += 1
            
        tuple_end_idx = i
        # Now consume trailing whitespace and comma
        while i < length:
            c = content[i]
            if c in ' \t\r\n,':
                i += 1
            elif c == '#':
                # A comment after the comma, let's consume it too until newline
                while i < length and content[i] != '\n':
                    i += 1
                if i < length:
                    i += 1 # consume newline
                break
            else:
                break
                
        element_text = content[start_of_element:i]
        
        # Extract name
        tuple_text = content[tuple_start_idx:tuple_end_idx]
        name_match = re.search(r'^\(\s*["\'](\w+)["\']', tuple_text)
        if name_match:
            name = name_match.group(1)
        else:
            name = None
            
        elements.append({
            'name': name,
            'text': element_text
        })
        
    postamble_start = i
    postamble = content[postamble_start:]
    
    return preamble, elements, postamble

def extract_domain(source_file, dest_file, var_name, script_names):
    print("Parsing {}...".format(source_file))
    preamble, elements, postamble = parse_scripts_list(source_file)
    
    print("Total scripts parsed:", len(elements))
    
    # We must ensure that any scripts following a target script that are "aux" or "fix" etc
    # are also extracted if they were part of the cluster. The user gave us a list of names.
    # We will strictly extract what is in the list, but maintain their relative order.
    
    target_names_set = set(script_names)
    
    extracted = []
    remaining = []
    
    for el in elements:
        if el['name'] in target_names_set:
            extracted.append(el)
        else:
            remaining.append(el)
            
    if not extracted:
        print("No scripts matched for extraction.")
        return
        
    print("Extracting {} scripts...".format(len(extracted)))
    
    # Write destination file
    dest_dir = os.path.dirname(dest_file)
    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)
        
    # Create __init__.py if missing
    init_path = os.path.join(dest_dir, '__init__.py')
    if not os.path.exists(init_path):
        with open(init_path, 'w') as f:
            f.write("# -*- coding: cp1254 -*-\n")
            
    with open(dest_file, 'w') as f:
        f.write("# -*- coding: cp1254 -*-\n")
        f.write("from header_common import *\n")
        f.write("from header_operations import *\n")
        f.write("from module_constants import *\n")
        f.write("from module_constants import *\n")
        f.write("from header_parties import *\n")
        f.write("from header_skills import *\n")
        f.write("from header_mission_templates import *\n")
        f.write("from header_items import *\n")
        f.write("from header_triggers import *\n")
        f.write("from header_terrain_types import *\n")
        f.write("from header_music import *\n")
        f.write("from header_map_icons import *\n")
        f.write("from ID_animations import *\n\n")
        f.write("{} = [\n".format(var_name))
        for el in extracted:
            f.write(el['text'])
        f.write("]\n")
        
    # Write back source file
    with open(source_file, 'w') as f:
        f.write(preamble)
        for el in remaining:
            f.write(el['text'])
        f.write(postamble)
        
    print("Done. Extracted to {}".format(dest_file))

if __name__ == '__main__':
    # Example usage:
    # extract_domain('source/module/module_scripts.py', 'source/module/native/scripts/music/music_scripts.py', 'music_scripts', ['music_set_situation_with_culture', 'play_victorious_sound'])
    pass

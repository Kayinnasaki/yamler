#!/usr/bin/env python3

import os
import sys
import yaml

default_ext = ["jpg", "png", "webp", "gif", "mp4"]
base_yaml = ".meta.yaml"


def gen_yaml(files):
    count = 0
    for file in files:
        meta_file = file + base_yaml
        if not os.path.isfile(meta_file):
            print("Generating YAML for " + file)
            with open(meta_file, 'w') as f:
                f.write('')
                count += 1
    return count


def modify_yaml(command, tags, files):
    count = 0
    for filepath in files:
        # Track if a file is actually changed
        modified = False
        # Tracks which tags were modified
        mtags = []
        with open(filepath, 'r') as file:
            data = yaml.safe_load(file) or {}

        if 'tags' not in data:
            data['tags'] = []
            modified = True
        elif data['tags'] is None:
            data['tags'] = []

        if command == 'add':
            for tag in tags:
               if tag not in data['tags']:
                    data['tags'].append(tag)
                    mtags.append(tag)
                    modified = True

        if command == 'remove':
            for tag in tags:
               if tag in data['tags']:
                    data['tags'].remove(tag)
                    mtags.append(tag)
                    modified = True

        with open(filepath, 'w') as file:
            yaml.dump(data, file, default_flow_style=False)
        
        # Increase Count if it actually was changed
        if modified == True :
            verb = " added tags: " if command == "add" else " removed tags: "

            print("File " + filepath + verb + str(mtags) )
            count += 1

    return count


def get_filelist(locations, extensions):
    # Defaults to local folder with no arguments
    if len(locations) == 0:
        locations.append(os.getcwd())

    filelist = []

    for location in locations:
        # Is it a Directory? Crawl it!
        if os.path.isdir(location):
            for root, dirs, files in os.walk(location):
                for file in files:
                    # Skip Thumbs and Header files
                    if file.startswith('_') or 'mp4.thumb' in file:
                        continue
                    
                    if file.split(".")[-1].lower() in extensions:
                        filelist.append(os.path.join(root, file))

        # Is it a File? Check the extension and then add it!
        elif os.path.isfile(location) and location.split(".")[-1].lower() in extensions:
            filelist.append(location)

    return filelist


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python yamler.py <add|remove|gen> <tags> <files/directory>")
        sys.exit(1)

    if sys.argv[1] == "gen" :
        print("Generating YAML files")
        files = get_filelist(sys.argv[2:], default_ext)
        count = gen_yaml(files)
        print(str(count) + " YAML files Generated")
        sys.exit(1)
    
    # Exit Early if there aren't enough inputs for add and remove
    if len(sys.argv) < 3:
        print("Additional Parameters Required")
        sys.exit(1)       
    
    if sys.argv[1] == "add" :
        tags = sys.argv[2].split(',')
        print("Adding YAML tags: " + str(tags))
        files = get_filelist(sys.argv[3:], base_yaml)
        count = modify_yaml("add", tags, files)
        print(str(count) + " YAML files Modified")
        sys.exit(1)
    
    if sys.argv[1] == "remove" or sys.argv[1] == "rem" :
        tags = sys.argv[2].split(',')
        print("Removing YAML tags: " + str(tags))
        files = get_filelist(sys.argv[3:], base_yaml)
        count = modify_yaml("remove", tags, files)
        print(str(count) + " YAML files Modified")
        sys.exit(1)
    
    print("No Valid Command Given")
    sys.exit(1)
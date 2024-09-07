# YAMLer

A simple script that uses the python YAML libraries to do some big sweeping tagging operations.

This script is used to manage a Grav gallery and the many pictures that get added to it, but bits and pieces might be useful to someone else. It is doubtful this file will be useful to you as is, but if you modify it or expand on it, please let me know!

## Usage

`yamler [gen/add/remove] [tags(for add and remove)] [files] [or] [folders]`

Files matching the extension rules will be added. Folders will be crawled for all valid content.

`yamler gen` will generate .meta.yaml files for every valid image or video.

`yamler add/remote [tags]` will add or remove an array of tags, formatted like `tag1,tag2,tag3` to every profiled yaml file.

The provided file also skips some files, like ones that begin with `_` or contain `mp4.thumb`. This is to serve my own use-case and you could easily just cut out the check.
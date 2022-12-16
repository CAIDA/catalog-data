# conediff

For analyzing changes in a specific customer cone between two points in time.

## Files in this project

### filter_paths.ipynb

Jupyter notebook with code segments that do the following:

- loads two customer cone files and compares them to find which ASes were gained and which were lost from the customer cone of a specific AS
- goes through an `all-paths` file and stores a list of paths containing the target AS and any AS(es) on a given list (e.g. a list of gained/lost ASes from the previous segment)
- counts frequency of how often each gained/lost AS shows up in the filtered list of paths, and counts the frequencies themselves (and prints them)
- saves the filtered list of paths

### print_paths.ipynb

Another Jupyter notebook with code segments that do the following:

- create lists of gained/lost ASes like in `filter_paths.ipynb`
- go through AS relationships file and make a dict of relationships between ASes that are found in the filtered list of paths (for faster processing)
- annotate the filtered list of paths with the relationships between adjacent ASNs (producing a list of lists which alternate ASNs as ints and single chars representing relationships)
- "crop" the paths by shortening them to only the part after (and including) the first provider-to-customer relationship, then again to only the part after (and excluding) the target AS
- go through the cropped paths and, for each ASN, make a list of every unique gained/lost ASN that comes after it
- tally up the lists and display the top n ASNs

### 20220801.gained_from_5511.txt

A filtered list of paths produced by `filter_paths.ipynb`; it's all of the paths that contain ASNs that appeared in AS5511's customer cone between June and August 2022

### 20220801.lost_from_3257.txt

Another filtered list of paths; ones containing ASNs lost from AS3257's cone from August to September 2022 (I think I need to fix the name)

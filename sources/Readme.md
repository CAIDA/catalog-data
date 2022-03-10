## sources/[type]/[short_id].json (everything but recipes)

Except for recipes,  all objects exist as a single JSON file in the sources/(type) directory.  The type and file name need to match the type an short_id respectively.

For now Papers and parts of Media are stored and maintained in the pubDB directory, so their JSON files are created programmatically from pubDB.
A Media or Paper's short_id are the same as the paper's part of the URL.

## sources/recipe/[short_id]/Readme.md (recipe)

Recipes are stored as a directory with the same name as the short_id with the content in the Readme.md as markdown in that directory. <br>
More details are [outlined here](metadata-:-recipe).

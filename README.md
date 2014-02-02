gmod-wiki-npp
=============

Scrapes http://wiki.garrysmod.com for useful autocomplete hints and tosses them into Notepad++ autocomplete format

## Requirements
- python 2.7
- https://github.com/lxml/lxml
- https://github.com/earwig/mwparserfromhell
- https://github.com/mwclient/mwclient

## Bugs
- autocomplete list too big for notepad++ (takes multiple seconds to process)
- Does not parse/handle incomplete data
 - This means not all functions get processed (about 10 in the current wiki)
- Does not cache wiki content

## TODO
- Enums Category
- Include Examples
- Add download caching
- Notepad++: Use RapidXML instead of TinyXML for speedup

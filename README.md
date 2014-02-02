gmod-wiki-npp
=============

Scrapes http://wiki.garrysmod.com for useful autocomplete hints and tosses them into Notepad++ autocomplete format. This does NOT generate syntax highlighting.

## Instructions
Download GMod Syntax Highlight plugin (http://code.google.com/p/npp-gmod-lua/) from Notepad++ plugin manager and update the xml file with this:
http://facepunch.com/showthread.php?t=1274235&p=43718059&viewfull=1#post43718059

Save latest scrape https://github.com/Python1320/gmod-wiki-npp/raw/master/GMod%20Lua.xml
 to Notepad++/plugins/APIs/ and enabled auto-complete on Settings->Preferences->Auto-Completion


#### References
- http://sourceforge.net/apps/mediawiki/notepad-plus/?title=Auto_Completion
- http://code.google.com/p/npp-gmod-lua/

#### Requirements
- python 2.7
- https://github.com/lxml/lxml
- https://github.com/earwig/mwparserfromhell
- https://github.com/mwclient/mwclient

#### Bugs
- autocomplete list too big for notepad++ (takes multiple seconds to process)
- Does not parse/handle incomplete data
 - This means not all functions get processed (about 10 in the current wiki)
- Does not cache wiki content

#### TODO
- Enums Category
- Include Examples
- Add download caching
- Notepad++: Use RapidXML instead of TinyXML for speedup

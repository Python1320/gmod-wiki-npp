#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
import mwclient,sys,mwparserfromhell
from lxml import etree
from textwrap import TextWrapper
from textwrap import fill
from textwrap import wrap


# Initialize the XML Tree
NotepadPlus  = etree.Element('NotepadPlus')
AutoComplete = etree.SubElement(NotepadPlus,'AutoComplete')
AutoComplete.set("language","GMod Lua")

Environment = etree.SubElement(AutoComplete,'Environment')
Environment.set("ignoreCase", "yes")
Environment.set("startFunc", "(")
Environment.set("stopFunc", ")")
Environment.set("paramSeparator", ",")
Environment.set("terminal", ";")
Environment.set("additionalWordChar", ":.")

# Helper for creating autocompletes
class Keyword:
	Overload=False
	def __init__(self,Simple=False):
		global AutoComplete
		self.KeyWord = etree.SubElement(AutoComplete,'KeyWord')
		if Simple:
			self.name(Simple)
		else:
			self.KeyWord.set("func", "yes")
			self.overload()
			
		
	def name(self,name):
		self.KeyWord.set("name", name)
		
	def overload(self):
		assert(self.Overload==False)
		self.Overload = etree.SubElement(self.KeyWord,'Overload')
		self.ret("")
		self.desc("")
		
	def param(self,name):	
		Param = etree.SubElement(self.Overload,'Param')
		Param.set("name", name)
		return Param
		
	def ret(self,retVal):
		self.Overload.set("retVal", retVal)
		
	def desc(self,descr):
		self.Overload.set("descr", descr)
		
	def desc_add(self,descr):
		cur=self.Overload.get("descr")
		if len(cur)>0:
			self.Overload.set("descr", cur+"\n"+descr)
		else:
			self.Overload.set("descr", descr)
	
	def fin(self):
		assert(self.Overload!=None)
		self.KeyWord.get("name")
		pass


# Parse the wiki input
class PARSE:
	
	def setKW(self,kword):
		self.kw=kword
		
	def addinfo(self,desc):
		self.kw.desc_add(desc)
		
	def parse_Example(self, b):
		pass
		
	def parse_Ret(self, b):
		type = b.get("type").value.strip()
		desc = b.get("desc").value.strip()
		#print "","Returns",type,"(",desc,")"
		self.kw.ret(type)
		
	def parse_Hook(self, b):
		Name = b.get("Name").value.strip()
		Parent = b.get("Parent").value.strip()
		Description = b.get("Description").value.strip()
		Realm = b.get("Realm").value.strip()
		sig = Parent+":"+Name
		self.kw.name(sig)
		self.addinfo( "http://wiki.garrysmod.com/page/"+Parent+"/"+Name )
		self.addinfo( Realm )
		self.addinfo( fill(Description,100) )
		
		
	def parse_Func(self, b):
		Name = b.get("Name").value.strip()
		Parent = b.get("Parent").value.strip()
		Description = b.get("Description").value.strip()
		Realm = b.get("Realm").value.strip()
		IsClass = b.get("IsClass").value.strip()==u"Yes"
		sig = Parent+(IsClass and ":" or ".")+Name
		self.kw.name(sig)
		self.addinfo( "http://wiki.garrysmod.com/page/"+Parent+"/"+Name )
		self.addinfo( Realm )
		self.addinfo( fill(Description,100) )
		
	def parse_Arg(self, b):
		type = b.get("type").value.strip()
		name = b.get("name").value.strip()
			
		self.kw.param(type+u" "+name)

		desc = False
		try:
			desc = b.get("desc").value.strip()
		except:
			pass
			
		if desc:
			wrapdesc=TextWrapper(initial_indent="",subsequent_indent="  ",width=93)
			desc = wrapdesc.fill( desc )
			self.addinfo( "\n"+type+" "+name+": " + desc )

		
	def Parse(self, blob):
		blobtype = blob.name.strip() 
		f=getattr(self, 'parse_' + blobtype, None)
		if f==None:
			print "Warning: Unknown blobtype: ",blobtype
			return
		try:
			f(blob)
		except:
			print "Warning: Failed parsing blobtype: ",blobtype
parser=PARSE()

site = mwclient.Site('wiki.garrysmod.com',path = '/')
#site.login(username, password)  # Optional
print "Connected!"


def parse_category(cat):
	global site,parser,mwparserfromhell,Keyword
	print"Parsing ",cat,"..."
	cat=site.Pages[cat]
	asd=9999
	
	# Iter all functions
	for m in cat.members():
		kw = Keyword()
		parser.setKW(kw)
		
		if asd==0:
			break
		else:
			asd=asd-1
		sys.stdout.write(".") 
		sys.stdout.flush()
		txt = m.edit(readonly=True)
		parsed = mwparserfromhell.parse(txt)
		
		# function properties
		for infoblob in parsed.filter_templates(recursive=False):
			parser.Parse(infoblob)
	print""
parse_category('Category:Hooks')
parse_category('Category:Functions')

	
#sort that shit
def getkey(elem):
	e=elem.get("name")
	if e:
		return e.lower()
AutoComplete[:] = sorted(AutoComplete, key=getkey)

# Save
s = etree.tostring(NotepadPlus, pretty_print=True, encoding='Windows-1252').replace("&#13;","&#xD;").replace("&#10;","&#xA;")
f = open('GMod Lua.xml', 'w')
f.write(s)

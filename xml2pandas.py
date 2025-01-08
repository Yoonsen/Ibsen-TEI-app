#!/usr/bin/env python
# coding: utf-8

# In[1]:


file = "DRVIT_Fo_Foht.xml"


# In[24]:


import dhlab as dh
from dhlab.nbtokenizer import tokenize
import pandas as pd


# In[3]:


with open(file, encoding="utf-8") as fp:
    txt = fp.read()


# In[4]:


len(tokenize(txt))


# In[5]:


from lxml import etree


# In[ ]:





# In[6]:


# Load the XML data without the encoding declaration
xml_data = txt.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
tree = etree.fromstring(xml_data)  # tree is actually the root element here


# In[7]:


# Define both namespaces explicitly
namespaces = {
    'tei': 'http://www.tei-c.org/ns/1.0',
    'HIS': 'http://www.example.org/ns/HIS'
}

# Example: Extracting characters from <tei:castItem> and dialogues from <HIS:hisSp>
character_ids = [
     item.xpath('string()').strip()
    for item in tree.xpath('//tei:castItem', namespaces=namespaces)
]

# Extract dialogue or other elements in the HIS namespace
dialogues = [
    element.xpath('string()').strip()
    for element in tree.xpath('//HIS:hisSp', namespaces=namespaces)
]

#print("Characters:", character_ids)
#print("Dialogues:", dialogues)


# In[8]:


characters = [x.split(",")[0] for x in character_ids]


# In[9]:


characters


# In[10]:


def clean_dialogue(d):
    # Split by newlines and strip extra whitespace
    parts = [part.strip() for part in d.split('\n') if part.strip()]
    character = parts[0]  # First line is likely the character
    text = " ".join(parts[1:])  # Join the rest as dialogue text
    return character, text

def clean_dialogue_no_stage(d):
    # Remove all <HIS:hisStage> elements from the dialogue element
    for stage in d.xpath('.//HIS:hisStage', namespaces=namespaces):
        stage.getparent().remove(stage)
    
    # Now get the dialogue text as before, ignoring removed parts
    text_content = d.xpath('string()').strip()
    
    # Split and clean as before
    parts = [part.strip() for part in text_content.split('\n') if part.strip()]
    character = parts[0]  # First line as character name
    text = " ".join(parts[1:])  # Remaining lines as dialogue
    return character, text
# Example usage


# In[11]:


processed_dialogues = [clean_dialogue_no_stage(d) for d in tree.xpath('//HIS:hisSp', namespaces=namespaces)]


# In[25]:


pd.DataFrame(processed_dialogues, columns=["speaker", "content"])


# In[20]:


with open('Folkefiende.json', "w") as fp:
    json.dump(acts, fp)


# In[ ]:





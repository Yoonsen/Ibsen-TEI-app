import streamlit as st
from lxml import etree
import pandas as pd
import io
import base64

def clean_dialogue_no_stage(d, namespaces):
    # Remove all <HIS:hisStage> elements from the dialogue element
    for stage in d.xpath('.//HIS:hisStage', namespaces=namespaces):
        stage.getparent().remove(stage)
    
    # Get the dialogue text
    text_content = d.xpath('string()').strip()
    
    # Split and clean
    parts = [part.strip() for part in text_content.split('\n') if part.strip()]
    character = parts[0] if parts else ""  # First line as character name
    text = " ".join(parts[1:]) if len(parts) > 1 else ""  # Remaining lines as dialogue
    return character, text

def process_xml(xml_content):
    try:
        # Remove XML declaration if present
        xml_content = xml_content.replace('<?xml version="1.0" encoding="UTF-8"?>', '')
        
        # Parse the XML
        tree = etree.fromstring(xml_content.encode('utf-8'))
        
        # Define namespaces
        namespaces = {
            'tei': 'http://www.tei-c.org/ns/1.0',
            'HIS': 'http://www.example.org/ns/HIS'
        }
        
        # Process dialogues
        processed_dialogues = [
            clean_dialogue_no_stage(d, namespaces) 
            for d in tree.xpath('//HIS:hisSp', namespaces=namespaces)
        ]
        
        # Create DataFrame
        df = pd.DataFrame(processed_dialogues, columns=["speaker", "content"])
        return df, None
    
    except Exception as e:
        return None, str(e)

def get_download_link(df):
    """Generate a download link for the Excel file"""
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
    excel_data = output.getvalue()
    b64 = base64.b64encode(excel_data).decode()
    return f'<a href="data:application/vnd.openxmlformats-officedocument.spreadsheetml.sheet;base64,{b64}" download="processed_dialogue.xlsx">Download Excel file</a>'

def main():
    st.title("TEI XML Dialogue Processor")
    
    st.write("""
    This app processes TEI XML files containing dialogue data from the Henrik Ibsen's Writings project. 
    You can find the TEI XML files at [The Henrik Ibsen's Writings](https://www.ibsen.uio.no/skuespill.xhtml).
    
    To use this app:
    1. Download a TEI XML file from the Ibsen repository
    2. Either upload the file here or paste its content directly
    """)
    
    # File upload
    uploaded_file = st.file_uploader("Upload XML file", type=['xml'])
    
    # Text area for pasting XML
    xml_text = st.text_area("Or paste XML content here", height=200)
    
    # Process button
    if st.button("Process XML"):
        # Get XML content either from file or text area
        xml_content = None
        if uploaded_file is not None:
            xml_content = uploaded_file.getvalue().decode('utf-8')
        elif xml_text:
            xml_content = xml_text
        
        if xml_content:
            df, error = process_xml(xml_content)
            
            if error:
                st.error(f"Error processing XML: {error}")
            else:
                st.success("XML processed successfully!")
                
                # Display the DataFrame
                st.write("Preview of processed data:")
                st.dataframe(df.head())
                
                # Provide download link
                st.markdown(get_download_link(df), unsafe_allow_html=True)
        else:
            st.warning("Please either upload a file or paste XML content")

if __name__ == "__main__":
    main()

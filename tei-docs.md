# TEI XML Processor Documentation

## Current Functionality

The application processes TEI XML files from the Ibsen repository, extracting dialogue information into a structured format. Here's how it works:

### XML Processing
- Uses `lxml` for XML parsing, which is faster than Python's built-in XML parser
- Handles TEI-specific namespaces:
  - `tei`: http://www.tei-c.org/ns/1.0
  - `HIS`: http://www.example.org/ns/HIS
- Removes XML declaration to prevent parsing issues
- Main processing happens in `clean_dialogue_no_stage()` function

### Data Extraction
- Currently extracts two main elements:
  - Speaker (character name)
  - Content (dialogue text)
- Removes stage directions using XPath: `.//HIS:hisStage`
- Creates clean DataFrame with two columns: "speaker" and "content"

### User Interface
- Built with Streamlit for easy interaction
- Provides two input methods:
  - File upload for XML files
  - Text area for pasting XML content
- Includes preview of processed data
- Allows downloading results as Excel file

## Planned Extensions

### 1. Adding Act Separators
To implement act separation, we'll need to:
- Identify act markers in the TEI XML (typically `<div type="act">`)
- Add act number to the DataFrame
- Modified structure could look like:
```python
def process_acts(tree, namespaces):
    acts = []
    for act in tree.xpath('//tei:div[@type="act"]', namespaces=namespaces):
        act_number = act.get('n')
        for speech in act.xpath('.//HIS:hisSp', namespaces=namespaces):
            # Process speech and include act number
            character, text = clean_dialogue_no_stage(speech, namespaces)
            acts.append({
                'act': act_number,
                'speaker': character,
                'content': text
            })
    return acts
```

### 2. Including Stage Instructions
To preserve stage instructions:
- Modify `clean_dialogue_no_stage()` to capture rather than remove stage directions
- Create separate column for stage instructions
- Example implementation:
```python
def extract_dialogue_with_stage(d, namespaces):
    # Get stage directions before removing them
    stage_directions = [
        stage.xpath('string()').strip()
        for stage in d.xpath('.//HIS:hisStage', namespaces=namespaces)
    ]
    
    # Get main dialogue as before
    text_content = d.xpath('string()').strip()
    parts = [part.strip() for part in text_content.split('\n') if part.strip()]
    character = parts[0]
    text = " ".join(parts[1:])
    
    return character, text, "; ".join(stage_directions)
```

## Future Considerations

### Performance Optimization
- For large XML files, consider implementing batch processing
- Could add progress bars for longer operations
- Potential for caching processed results

### Error Handling
- Add validation for XML structure
- Implement more detailed error messages for specific TEI elements
- Add warnings for missing or malformed elements

### Additional Features
- Text analysis tools (word frequency, dialogue length, etc.)
- Character interaction networks
- Visualization of speaker distributions
- Export to different formats (CSV, JSON, etc.)
- Custom namespace handling for different TEI variants

## Usage Tips

### Working with the Data
After processing, the DataFrame can be used for various analyses:
```python
# Example analyses
speaker_counts = df['speaker'].value_counts()
dialogue_lengths = df['content'].str.len()
```

### Modifying the Processing
To modify how the text is processed, focus on these functions:
- `process_xml()`: Main entry point for XML processing
- `clean_dialogue_no_stage()`: Handles individual dialogue elements
- `get_download_link()`: Manages file export

## Dependencies
- streamlit
- lxml
- pandas
- openpyxl (for Excel export)

## Installation
```bash
pip install streamlit lxml pandas openpyxl
```

## Running the App
```bash
streamlit run app.py
```

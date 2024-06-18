import fitz
from flask_cors import CORS
import pandas as pd
import os
def extract_text_above_below_margins(pdf_file, top_margin, bottom_margin):
    data = []
    try:
        doc = fitz.open(pdf_file)
        for page_number in range(len(doc)):
            page = doc.load_page(page_number)
            text = page.get_text()
            above_margin = []
            below_margin = []
            for line in text.split('\n'):
                bbox_list = page.search_for(line)
                if bbox_list:  # Check if the list is not empty
                    bbox = bbox_list[0]  # Get bounding box of line
                    y_coordinate = bbox[3]  # Y-coordinate of top-right corner
                    if y_coordinate > bottom_margin:
                        below_margin.append(line)
                    elif y_coordinate < top_margin:
                        above_margin.append(line)
            data.append({
                "PageNumber": page_number + 1,  # Add 1 to start from page 1
                "Header": "".join(above_margin),
                "Footer": "".join(below_margin)
            })
    except Exception as e:
        print("Error: {e}")
        return None
    df = pd.DataFrame(data)
    
    return df
    




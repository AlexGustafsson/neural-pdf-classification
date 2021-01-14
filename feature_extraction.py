# Run with: python3 -m feature_extraction "/path/to/file.pdf" > features.txt

import sys

import fitz

filename = sys.argv[1]

# List of tuples containing features:
# page_index, top, left, width, height, font, font_size, text
all_features = []

document = fitz.open(filename)
for page_index, page in enumerate(document):
    features = page.getText(option="dict")
    for block in features["blocks"]:
        for line in block["lines"]:
            for span in line["spans"]:
                # Location on page
                x1, y1, x2, y2 = span["bbox"]
                top = y1
                left = x1
                width = x2 - x1
                height = y2 - y1
                # Font
                font = span["font"]
                font_size = span["size"]
                # Content
                text = span["text"]

                all_features.append((page_index, top, left, width, height, font, font_size, text))

for feature in all_features:
    print(feature)

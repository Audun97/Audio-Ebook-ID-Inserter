from bs4 import BeautifulSoup, NavigableString
import re

def add_ids_to_spans(html_file):
    """
    This function takes a given HTML file and adds span with an unique IDs to each senetence clause. The IDs are generated by 
    incrementing a counter starting from 1 and formatted as "fXXX" where "XXX" is the zero-padded count. If a string of text in a 
    p element contains no punctuation, comma, semi-colon, exclamation mark or question mark and at least one letter, a new 
    span is created to wrap around the text and assigned the next ID. If the text contains a punctuation, comma, semi-colon, 
    exclamation mark or question mark, the text is split into separate clauses based on that and each sentence is wrapped in a 
    separate span with the next ID. The processed HTML file is saved with "_processed.xhtml" added to the original file name.

    Parameters:
    html_file (str): The path to the HTML file to be processed.

    Returns:
    None
    """
    
    # Define the output file name by splitting the input file name and adding "_processed.xhtml" to it
    outputfile = html_file.rsplit(".", 1)[0] + "_processed.xhtml"
    
    # Open the input file in read mode with UTF-8 encoding
    with open(html_file, "r", encoding="utf-8") as file:
        # Use BeautifulSoup to parse the file
        soup = BeautifulSoup(file, "lxml")

    # Get all the p elements in the file
    p_elements = soup.find_all("p")

    # Initialize a counter for the "id" values
    id_counter = 1

    # Loop through each p element
    for p in p_elements:
        
        # Get all the descendants of the current "p" element. Not feeding it directly into the next loop to prevent an endless loop
        children = list(p.descendants)
        
        # Initialize a span for the case that multiple child.strings will share a span
        current_span = None
        
        # Loop through each child of the "p" element
        for child in children:
            
            # Skip if the child is a NavigableString
            if isinstance(child, NavigableString):
                continue
            
            # Skip if the child has no string value. I.e. the child has multiple children of its own
            elif child.string is None:
                continue
            
            elif child.string is not None:
                
                # If there is no punctuation and there are alphabetical characters in the string, wrap the child in a new "span" tag
                if not re.search(r'[:;!,?.]', child.string) and re.search(r'[a-zA-Z]', child.string):
                    if current_span is None:
                        current_span = soup.new_tag("span")
                        current_span["id"] = f"f{str(id_counter).zfill(3)}"
                        id_counter += 1
                    child.wrap(current_span)
                    print("no comma \n")
                    
                # If there is alphabetical characters in the string, split the string into clauses and wrap each sentence in a new "span" tag
                elif re.search(r'[a-zA-Z]', child.string):
                    current_span = None
                    sentences = re.split(r'(?<=[.?!;:,])\s+(?=[A-Za-z])', child.string)
                    child.clear()
                    for sentence in sentences:
                        span = soup.new_tag("span")
                        span["id"] = f"f{str(id_counter).zfill(3)}"
                        span.string = sentence + " "
                        child.append(span)
                        id_counter += 1
                        print("with comma /n")
                        
                else:
                    # Printing what was not caught
                    print("this was caught" + str(child.string))
                        
    with open(outputfile, "w", encoding="utf-8") as file:
        # Write the processed soup object to the output file with no extra formatting
        file.write(soup.decode(formatter=None))

add_ids_to_spans(r"Ch0002.xhtml")
print("process has completed successfully")
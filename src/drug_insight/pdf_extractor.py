import pymupdf

def doc_extractor(doc_path: str, output_path: str, start_page = None, end_page = None):
  """
  Extracts information from a document and saves it to a text file.

  Args:
    doc_path: path to the document
    output_path: path to the output file
    start_page: page number to start extracting from, defaults to None if all pages should be extracted
    end_page: page number to end extracting at, defaults to None if all pages should be extracted
  """

  doc = pymupdf.open(doc_path) # open a document
  if start_page != None and end_page!= None:
    extract_extent = [x_page for x_page in range(start_page - 1, end_page)] # pages to be extracted
    doc.select(extract_extent)
  out = open(output_path, "wb") # create a text output
  for page in doc: # iterate the document pages
      text = page.get_text().encode("utf8") # get plain text (is in UTF-8)
      out.write(text) # write text of page
      out.write(bytes((12,))) # write page delimiter (form feed 0x0C)
  out.close()
from lxml import etree
import pandas as pd
import zipfile
import numpy as np
import glob
from lxml.etree import tostring
import re


ooXMLns = {'w':'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

def strip_list(input_list):
    """
    Strips whitespace for all individual strings in a list
    Parameters:
        input_list, a list of strings
    Returns:
        output_list, a list of strings
    """

    output_list = []
    for item in input_list:
        output_list.append(item.strip())
    return output_list

def process_code(rawcode, text, code_replace_dict=None):
    """
    Helper function to parse a single code and quoted text to support the hierarchical index.
    Used by json_to_df(), not usually called directly by users.
    Parameters:
        rawcode, a string containing the text of the code (the comment text)
        text, a string containing the quoted text (the document text that is coded)
        code_replace_dict, a dictionary of strings (from:to) for renaming codes
    Returns:
        return_list, a list of tuples (code, text) for each unique code
    Usage:
        process_code("top: subcode1, subcode2", "quoted text")
        [('top: subcode1', 'quoted text'), ('top: subcode2', 'quoted text')]
    """

    text = text.replace("&#39;", "'")
    rawcode = rawcode.lower()
    # print("rawcode before: ", rawcode)
    if code_replace_dict is not None:

        replace_pattern = re.compile(r'\b(' + '|'.join(code_replace_dict.keys()) + r')\b')
        rawcode = replace_pattern.sub(lambda x: code_replace_dict[x.group()], rawcode)


    rawcode_sep = rawcode.split(":")
    # print(rawcode_sep)

    num_parts = len(rawcode_sep)
    # print(num_parts)

    output_list = []

    if num_parts == 1:
        if rawcode_sep[0].find(";") == -1:
            output_list.append((rawcode, text))
            return output_list

        else:
            return_list = []
            for item in strip_list(rawcode_sep[0].split(";")):
                return_list.append((item, text))
            return return_list

    if num_parts == 2:
        rawcode_sep = strip_list(rawcode_sep)

        if rawcode_sep[1].find(";") == -1:
            output_list.append((rawcode, text))
            return output_list

        else:
            return_list = []
            for item in strip_list(rawcode_sep[1].split(";")):
                code_concat = rawcode_sep[0] + ": " + item
                return_list.append((code_concat, text))
            return return_list

    if num_parts == 3:

        rawcode_sep = strip_list(rawcode_sep)
        main_code = rawcode_sep[0]
        subcode = rawcode_sep[1]
        sub_subcode = rawcode_sep[2]

        if sub_subcode.find(";") == -1:
            output_list.append((rawcode, text))
            return output_list

        else:
            return_list = []
            for item in strip_list(sub_subcode.split(";")):
                code_concat = main_code + ": " + subcode + ": "+ item
                return_list.append((code_concat, text))
            return return_list


def cleanhtml(raw_html):
  cleanr = re.compile('<.*?>')
  cleantext = re.sub(cleanr, '', raw_html)
  return cleantext

def get_scope(wid, doc):
  #s = '//w:r[preceding-sibling::w:commentRangeStart[@w:id='+wid+'] and following-sibling::w:commentRangeEnd[@w:id='+wid+']]'
  s = tostring(doc)
  s = s.decode('utf-8')
  myrange = re.search('<w:commentRangeStart w:id="'+wid+'"/>(.*)<w:commentRangeEnd w:id="'+wid+'"/>', s).group(1)
  myscope = cleanhtml(myrange)
  #print myscope
  return myscope



def get_comments(docxFileName, codes_df, code_replace_dict=None):
  docxZip = zipfile.ZipFile(docxFileName)

  nl = docxZip.namelist()

  if 'word/document.xml' in nl:
    docXML = docxZip.read('word/document.xml')
  elif 'word/document2.xml' in nl:
    print(2)
    docXML = docxZip.read('word/document2.xml')
  else:
    return codes_df
  doc = etree.XML(docXML)
  if 'word/comments.xml' in nl:
    commentsXML = docxZip.read('word/comments.xml')
  else:
    return codes_df
  et = etree.XML(commentsXML)
  comments = et.xpath('//w:comment',namespaces=ooXMLns)



  for c in comments:

    comment_id = c.xpath('@w:id',namespaces=ooXMLns)[0]
    coded_text = get_scope(comment_id, doc)
    # print(coded_text)
    raw_codes = c.xpath('string(.)',namespaces=ooXMLns)

    comment_date = c.xpath('@w:date',namespaces=ooXMLns)
    comment_author = c.xpath('@w:author',namespaces=ooXMLns)[0]
    name = docxFileName

    #print(coded_text)

# --------------------------change to add separator ";" in comments--------------------------

    multiplecode_sep = raw_codes.split(";")
    # print(multiplecode_sep)
    multplecode_parts = len(multiplecode_sep)
    # print(multplecode_parts)

    while(multplecode_parts !=0):
      multplecode_parts = multplecode_parts - 1

      process_result = process_code(multiplecode_sep[multplecode_parts], coded_text, code_replace_dict)
      # print(process_result)

      if process_result is not None:
        for result in process_result:
          codes_dict = {'code':result[0], 'name':name, 'text':result[1], "coder":comment_author, 'comment_id': comment_id}
          codes_df = codes_df.append(pd.Series(codes_dict), ignore_index=True)

  for row, items in codes_df.iterrows():
      #print(items['code'].split(":"))
      count = 0

      code_split = items['code'].split(":")

      for i in code_split:
          i = i.lstrip()
          if count == 0:
              codes_df.ix[row]['code'] = i
          elif count == 1:
              codes_df.ix[row]['subcode'] = i
          elif count == 2:
              codes_df.ix[row]['sub_subcode'] = i
          else:
              assert True is False
          count = count + 1

  codes_df = codes_df.replace(np.nan, "")
  return codes_df
  #print(codes_df)



codes_df = pd.DataFrame(columns=["code","subcode","sub_subcode", "name", "text", "coder", "comment_id"])
files = glob.glob('./Copy of Room 13.docx')
#files = glob.glob('./k*.docx')
for fi in files:
  if 'Workshop' in fi:
    print(fi)
    codes_df = get_comments(fi, codes_df)

#print codes_df
codes_df = codes_df.set_index(['code', 'subcode', 'sub_subcode', 'text','name', 'coder']).sort_index()

codes_df.to_csv('outputworkshps.csv', encoding='utf-8-sig')

from lib.helpers.stocks import extract_stocks
from lib.helpers.read_xml_file import get_stocks_data



def stock_extraction_validation():

    pdf_count_data = len(extract_stocks()[0]['data'])
    xml_count_data = len(get_stocks_data())

    data = [ pdf_count_data, xml_count_data, (pdf_count_data == xml_count_data) ]
    json_data = []
    json_data.append( {"description": "Stock Extraction Validation", "data": data, "headers": ["PDF Extraction Count", "XML Validation Count", "Result"], "type": 'single'})
    return json_data

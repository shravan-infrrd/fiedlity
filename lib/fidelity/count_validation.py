
from lib.fidelity.stocks import extract_common_stocks, extract_preferred_stocks
from lib.fidelity.read_xml_file import get_stocks_data, get_preferred_stocks_data



def stock_extraction_val():

    pdf_count_data = len(extract_common_stocks()[0]['data'])
    xml_count_data = len(get_stocks_data())

    data = [ pdf_count_data, xml_count_data, (pdf_count_data == xml_count_data) ]
    json_data = []
    json_data.append( {"description": "Stock Extraction Validation", "data": data, "headers": ["PDF Extraction Count", "XML Validation Count", "Result"], "type": 'single'})
    return json_data


def preferred_stock_extraction_val():

    pdf_count_data = len(extract_preferred_stocks()[0]['data'])
    xml_count_data = len(get_preferred_stocks_data())

    data = [ pdf_count_data, xml_count_data, (pdf_count_data == xml_count_data) ]
    json_data = []
    json_data.append( {"description": "Stock Extraction Validation", "data": data, "headers": ["PDF Extraction Count", "XML Validation Count", "Result"], "type": 'single'})
    return json_data

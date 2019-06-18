from lib.fidelity.stocks import extract_common_stocks
from lib.fidelity.read_xml_file import get_stocks_data



def compare_stock_values():
    pdf_data = extract_common_stocks()[0]['data']
    xml_data = get_stocks_data()

    data = []
    headers = ['Description', 'BB Mkt Val(PDF)', 'BB Mkt Val(XML)', 'End Mkt Val(PDF)', 'End Mkt Val(XML)', 'EAI(PDF)', 'EAI(XML)']
    for i, d in enumerate(pdf_data):
        #values = []
        data.append( [ pdf_data[i][0], pdf_data[i][1], xml_data[i][2], pdf_data[i][4], xml_data[i][1], pdf_data[i][5], xml_data[i][3] ])
   

    json_data = []
    json_data.append({"description": "Stocks", "data": data, "headers": headers, 'type': 'multiple'})
    return json_data


from lib.helpers.holdings import compare_xml_with_pdf_data
from lib.helpers.account_summary import net_value_validation
from lib.helpers.stocks import extract_stocks
from lib.helpers.overlap import extract_overlaps
from lib.helpers.count_validation import stock_extraction_validation
from lib.helpers.compare_extraction import compare


#fidelity_2
from lib.fidelity.stocks import extract_common_stocks
from lib.fidelity.identify_footnote import get_footnotes
from lib.fidelity.count_validation import stock_extraction_val, preferred_stock_extraction_val
from lib.fidelity.sub_total_validation import total_common_stock, total_preferred_stock, total_stock
from lib.fidelity.compare_extraction import compare_stock_values


def get_test_data():
                return { "name": "Test", "arr_data": [1,2,3]}

def get_extraction():

    data = []
    data.append( { "name": 'Account Summary', "tables": net_value_validation() }  )
    data.append( { "name": 'Holdings', "tables": compare_xml_with_pdf_data() } )
    data.append( { "name": 'Stocks', "tables": extract_stocks() } )
    data.append( { "name": 'Overlap', "tables": extract_overlaps()} )
    data.append( { "name": 'Total Stock Extraction Validation', "tables": stock_extraction_validation() } )
    data.append( { "name": 'Compare Stocks values', "tables": compare() } )

    #print(data)

    return {'name': "Fiedelity", 'sections': data }


def get_fidelity_extraction():
    data = []
    data.append( { "name": 'Footnote', "tables": get_footnotes() }  )
    data.append( { "name": 'Stocks', "tables": extract_common_stocks() } )
    data.append( { "name": 'Total Stock Extraction Validation', "tables": stock_extraction_val() } )
    data.append( { "name": 'Total Preferred Stock Extraction Validation', "tables": preferred_stock_extraction_val() } )
    data.append( { "name": 'Total Common Stock', "tables": total_common_stock() }  )
    data.append( { "name": 'Total Preferred Stock', "tables": total_preferred_stock() }  )
    data.append( { "name": 'Total Stock', "tables": total_stock() }  )
    #data.append( { "name": 'Compare Stocks values', "tables": compare_stock_values() } )


    return {'name': "Fiedelity", 'sections': data }




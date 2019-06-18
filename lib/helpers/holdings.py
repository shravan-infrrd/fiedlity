from constant import PROJECT_ROOT
from lib.helpers.read_xml_file import get_holdings_data, get_stocks_data
import re

def get_contents():
                text_file_path = PROJECT_ROOT + "/temp_files/page-5.txt"

                with open( text_file_path ) as fp:
                                contents = fp.readlines()

                return contents


def find_pattern(str_1, str_2):
                try:
                                match = re.compile(r'\b({0})\b'.format( str_1 ), flags=re.IGNORECASE).search(str_2)
                                if match is None:
                                                return False
                                else:
                                                return True
                except:
                                #print("Error--")
                                return False


def compare_xml_with_pdf_data():
                print("===Compare XML Data===")
                flag = False
                table_data = []
                table_data_1 = []
                data = get_holdings_data()
                print("Holding_data--->", data)


                contents = get_contents()
                for content in contents:
        
                                if 'Holdings' in content:
                                                flag = True
                                if 'Stocks' in content:
                                                break
                                
                                holdings_columns = ['Beginning Market Value Mar 20, 2019', 'Quantity Mar 21, 2019', 'Price Per Unit Mar 21, 2019', 'Ending Market Value Mar 21, 2019'] 
                                val_data = {}
                                if flag:
                                                if content.strip() != "":
                                                                words = content.split('  ')
                                                                values = list( filter( None, words ) )
                                
                                                                if len(values) >= len(data['holdings']['values'])+1 :
                                
                                                                                if find_pattern(values[0].lower().strip(), data['holdings']['description'].lower().strip()):
                                
                                                                                                for i, value in enumerate(data['holdings']['values']):
                                                                                                                arr_d = []
                                                                                                                val_data = {}
                                                                                                                val_data['xml_value'] = float(value)
                                
                                                                                                                val_data['extracted_value'] = float(re.sub("[^\d\.]", "", values[ i + 1]))
                                                                                                                arr_d.append(holdings_columns[i])       
                                                                                                                arr_d.append(float(value))
                                                                                                                arr_d.append(float(re.sub("[^\d\.]", "", values[ i + 1])))

                                                                                                                #print(f"Values------->{value}")
                                                                                                                #print( re.sub("[^\d\.]", "", values[ i + 1]) )
                                                                                                                if float(value) != float(re.sub("[^\d\.]", "", values[ i + 1])):
                                                                                                                                print(False)
                                                                                                                                val_data['validation'] = False
                                                                                                                                arr_d.append('failed')
                                                                                                                else:
                                                                                                                                val_data['validation'] = True
                                                                                                                                arr_d.append('pass')
                                                                                                                                print(True)
                                
                                                                                                                table_data.append(val_data)     
                                                                                                                table_data_1.append(arr_d)

                json_data = []
                json_data.append( {"description": data['holdings']['description'], "data": table_data_1, "headers": ['Description', 'XML Data', 'Extraction', 'Result'], 'type': 'multiple' } )
                return json_data
                #return {"holdings": data}
                #return {"holdings": table_data}



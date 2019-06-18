from constant import PROJECT_ROOT
import xmltodict
import pprint
import json


#file_path = "/home/ubuntu/fidelity/working/temp_files/test.xml"
#file_path = "/Users/shravanc/learning_pyt/test.xml"
file_path = PROJECT_ROOT + "/temp_files/test.xml"


with open(file_path) as fd:
                doc = xmltodict.parse(fd.read())


file_data = json.loads( json.dumps( doc ) )
sections = file_data['FILE']['ICLR0203-HOLDING-VIEW']




def get_holdings_data():
                #sections = file_data['FILE']['ICLR0203-HOLDING-VIEW']
                data = {}

                for i, sec in enumerate(sections):
                                #CRA
                                if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'CRA':
                                                
                                                #H
                                                if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'H':
                                                                data['holdings'] = {}
                                                                data['holdings']['description'] = ''
                                                                for k, v in sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-DSC-TXT'].items():
                                                                                if v is not None:
                                                                                                data['holdings']['description'] = data['holdings']['description'] + ' ' + v
                                                
                                                                data['holdings']['values'] = []
                                                                data['holdings']['values'].append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'] )
                                                                data['holdings']['values'].append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-SD-QT'] )
                                                                data['holdings']['values'].append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'] )
                                                                data['holdings']['values'].append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'] )
                                                #TT
                                                if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'TT':
                                                                data['holding_core_account'] = {}
                                                                data['holding_core_account']['description'] = "Total Core Account"
                                                                data['holding_core_account']['market_value'] = sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE']
                                                                        
                print("from the function****************")
                print(data)
                return data     


def get_stocks_data():
    #sections = file_data['FILE']['ICLR0203-HOLDING-VIEW']
    #data = {}


    stocks = []
    for i, sec in enumerate(sections):
        stock_values = []
        data = {}
        if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'STK':
            if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'C':
                #print(sec)
                data['stocks'] = {}
                data['stocks']['description'] = ''
                for k, v in sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-DSC-TXT'].items():
                    if v is not None:
                        data['stocks']['description'] = data['stocks']['description'] + ' ' + v



                data['stocks']['values'] = []
                data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'] )
                data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'] )
                data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'] )
                data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'] )

                stock_values.append(data['stocks']['description'])
                stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'])
                #stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'])
                #stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'])
                #stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'])
                stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-MKT-VAL'])
                stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-EST-ANNUAL-INCOME'])

                stocks.append(stock_values)

    return stocks

"""
def get_stocks_data():
                #sections = file_data['FILE']['ICLR0203-HOLDING-VIEW']
                data = {}

                for i, sec in enumerate(sections):
                                if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'STK':
                                                if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'C':
                                                                #print(sec)
                                                                data['stocks'] = {}
                                                                data['stocks']['description'] = ''
                                                                for k, v in sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-DSC-TXT'].items():
                                                                                if v is not None:
                                                                                                data['stocks']['description'] = data['stocks']['description'] + ' ' + v
                                        
                                                                data['stocks']['values'] = []
                                                                data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'] )
                                                                break
                                                                #data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'] )
                                                                #data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'] )
                                                                #data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'] )

                return data


"""

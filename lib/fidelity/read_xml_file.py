from constant import PROJECT_ROOT
import xmltodict
import pprint
import json

file_path = PROJECT_ROOT + "/temp_files/fidelity_2/fidelity_2.xml"
with open(file_path, mode="r", encoding="utf-8") as fd:
		#print(fd.read())
		doc = xmltodict.parse(fd.read())


file_data = json.loads( json.dumps( doc ) )
sections = file_data['FILE']['ICLR0203-HOLDING-VIEW']

stocks_sections = []
for sec in sections:
		if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == "STK":
				stocks_sections.append(sec)
print(stocks_sections)



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




def xml_total_common_stock():
		stocks = []
		for i, sec in enumerate(sections):
				stock_values = []
				data = {}
				if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'STK':
						if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'CS':
								return sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE']

def get_stocks_data():


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
	
								footnote = ""
								if sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-NBR-FOOTNOTES'] != "0":
										for fn in sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-FOOTNOTE-SYMBOL']:
												if fn['ICLR0203-SYMBOL-STRING']:
														if footnote:
																footnote = footnote + ", " + fn['ICLR0203-SYMBOL-STRING']
														else:
																footnote = fn['ICLR0203-SYMBOL-STRING']

								#print(sec['ICLR0203-EXTRACT-VIEW'])								
								data['stocks']['values'] = []
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-MKT-VAL'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-TLA-INFO']['ICLR0203-COST-BASIS'] )
								data['stocks']['values'].append(footnote)

								stock_values.append(data['stocks']['description'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-MKT-VAL'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-TLA-INFO']['ICLR0203-COST-BASIS'])
								stock_values.append(footnote)
								stocks.append(stock_values)

		return stocks

def xml_total_preferred_stock():
		stocks = []
		for i, sec in enumerate(sections):
				stock_values = []
				data = {}
				if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'STK':
						if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'PS':
								return sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE']

def get_preferred_stocks_data():


		stocks = []
		for i, sec in enumerate(sections):
				stock_values = []
				data = {}
				if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'STK':
						if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'P':
								#print(sec)
								data['stocks'] = {}
								data['stocks']['description'] = ''
								for k, v in sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-DSC-TXT'].items():
										if v is not None:
												data['stocks']['description'] = data['stocks']['description'] + ' ' + v
													

								#print(sec['ICLR0203-EXTRACT-VIEW'])								
								data['stocks']['values'] = []
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-MKT-VAL'] )
								data['stocks']['values'].append( sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-TLA-INFO']['ICLR0203-COST-BASIS'] )

								stock_values.append(data['stocks']['description'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-TD-QT'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-NUM-SHRS'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-PRC-AMT'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-BB-MKT-VAL'])
								stock_values.append(sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-TLA-INFO']['ICLR0203-COST-BASIS'])

								stocks.append(stock_values)

		return stocks


def xml_total_stocks():
		stocks = []
		for i, sec in enumerate(sections):
				stock_values = []
				data = {}
				if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP1'] == 'STK':
						if sec['ICLRP001-PREFIX-RECORD']['ICLRP001-RECORD-SUB-TYP2'] == 'TT':
								return sec['ICLR0203-EXTRACT-VIEW']['ICLR0203-HLD-MKT-VALUE']

#data = get_preferred_stocks_data()
#for d in data:
#		print(d)
#print(data)
#print(f"Total Stocks===>{len(data)}")

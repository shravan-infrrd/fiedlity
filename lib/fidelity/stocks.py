from constant import PROJECT_ROOT
import re
from lib.fidelity.identify_footnote import only_footnotes
from lib.fidelity.read_xml_file import get_stocks_data

def extract_foot_note(footnotes, description):
		footnote = description.split(' ')[0]
		if len(footnote) > 2:
				return ['NA', '-']
		if footnote:
				valid_footnote = footnote in footnotes
				return [footnote, valid_footnote]
		else:
				return ['NA', '-']


def append_total_cost_basis(data):
		stocks = get_stocks_data()
		for i, d in enumerate(data):
				d.append(stocks[i][7])
				d.append(stocks[i][6])
				d.append(stocks[i][5])
				
		return data

def extract_preferred_stocks():
		data = []
		footnotes = only_footnotes()
		#for i in range(5,10):
		for i in range(16,18):
				text_file_path = f"{PROJECT_ROOT}/temp_files/fidelity_2/page-{i}.txt"
				with open( text_file_path ) as fp:
						contents = fp.readlines()
				
				flag = False
				page = []
				for content in contents:
						if 'Bonds' in content:
								break
						if 'Preferred Stock' in content:
								flag = True
								continue
						else:
								if not flag:
										continue
						
						
						if flag:
								words = content.strip().split('  ')
								values = list( filter( None, words ) )
								
								if values:
										#print(f"data---->{data}")
										if len(values) == 1:
												if not re.findall(r"\d+ of \d+", values[0]):
														if page:
																page[-1][0] = page[-1][0] + " " + values[0]
										else:
												if len(values) >= 5:
														page.append(values)
														if len(values) == 7:
																values.pop()
																#data.append(values)
														elif len(values) == 5:
																values.append("")
																#data.append(values)
														#elif len(values) == 6:
																#data.append(values)
														
														values.extend( extract_foot_note(footnotes, values[0])  )
														data.append(values)

				flag = False


		#data = append_total_cost_basis(data)
		json_data = []
		#json_data.append({"description": "Common Stocks", "data": data, 'type': 'multiple', 'headers': ['Description', 'Beginning Market Value Mar 20, 2019', 'Quantity Mar 21, 2019', 'Price Per Unit Mar 21, 2019', 'Ending Market Value Mar 21, 2019', 'EAI (S$)/ EY (%)']} )
		json_data.append({"description": "Preferred Stocks", "data": data, 'type': 'multiple', 'headers': ['Description', 'Beginning Market Value Mar 20, 2019', 'Quantity Mar 21, 2019', 'Price Per Unit Mar 21, 2019', 'Ending Market Value Mar 21, 2019', 'EAI (S$)/ EY (%)']} )
		return json_data


def extract_common_stocks():
		data = []
		footnotes = only_footnotes()
		#for i in range(5,10):
		for i in range(11,18):
				print("PAGENUMBER**********>", i)	
				text_file_path = f"{PROJECT_ROOT}/temp_files/fidelity_2/page-{i}.txt"
				with open( text_file_path ) as fp:
						contents = fp.readlines()
				
				flag = False
				page = []
				for content in contents:
						if 'Preferred Stock' in content:
								break
						if 'Common Stock' in content:
								flag = True
								continue
						else:
								if not flag:
										continue
						
						
						if flag:
								words = content.strip().split('  ')
								values = list( filter( None, words ) )
								
								if values:
										#print(f"data---->{data}")
										if len(values) == 1:
												if not re.findall(r"\d+ of \d+", values[0]):
														if page:
																page[-1][0] = page[-1][0] + " " + values[0]
										else:
												if len(values) >= 5:
														page.append(values)
														if len(values) == 7:
																values.pop()
																#data.append(values)
														elif len(values) == 5:
																values.append("")
																#data.append(values)
														#elif len(values) == 6:
																#data.append(values)
														
														values.extend( extract_foot_note(footnotes, values[0])  )
														data.append(values)

				flag = False


		data = append_total_cost_basis(data)
		json_data = []
		#json_data.append({"description": "Common Stocks", "data": data, 'type': 'multiple', 'headers': ['Description', 'Beginning Market Value Mar 20, 2019', 'Quantity Mar 21, 2019', 'Price Per Unit Mar 21, 2019', 'Ending Market Value Mar 21, 2019', 'EAI (S$)/ EY (%)']} )
		json_data.append({"description": "Common Stocks", "data": data, 'type': 'multiple', 'headers': ['Description', 'Beginning Market Value Mar 20, 2019', 'Quantity Mar 21, 2019', 'Price Per Unit Mar 21, 2019', 'Ending Market Value Mar 21, 2019', 'EAI (S$)/ EY (%)', 'Footnote', 'Footnote Validation', 'XML Footnote', 'Total Cost Basis', 'BB-Mkt-Val']} )
		return json_data


#data = extract_stocks()

#for d in data[0]['data']:
#		print(d)

#print(len(data[0]['data']))

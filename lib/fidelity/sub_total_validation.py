from constant import PROJECT_ROOT

from lib.fidelity.read_xml_file import xml_total_common_stock, xml_total_preferred_stock, xml_total_stocks

def get_data():
		text_file = PROJECT_ROOT + "/temp_files/fidelity_2/page-17.txt"
		with open( text_file ) as fp:
				contents = fp.readlines()

		return contents

def total_common_stock():
		lines = get_data()
		val = None
		for line in lines:
				if "Total Common Stock" in line:
						words = line.split('  ')
						valid_words = list( filter( None, words ) )
						val = valid_words[-2]
						break

		json_data = []
		json_data.append( {"description": "Common Stock", "data": [val.replace('$', ''), xml_total_common_stock()] , "headers": ["PDF Value", "XML Value" ], "type": "single"} )
		return json_data


def total_preferred_stock():
		lines = get_data()
		val = None
		for line in lines:
				if "Total Preferred Stock" in line:
						words = line.split('  ')
						valid_words = list( filter( None, words ) )
						val = valid_words[-2]
						break

		json_data = []
		json_data.append( {"description": "Preferred Stock", "data": [val.replace('$', ''), xml_total_preferred_stock()], "headers": ["PDF Value", "XML Value" ], "type": "single"} )
		return json_data

def total_stock():
		lines = get_data()
		val = None
		for line in lines:
				if "Total Stocks" in line:
						words = line.split('  ')
						valid_words = list( filter( None, words ) )
						val = valid_words[-2]
						break

		json_data = []
		json_data.append( {"description": "Total Stock", "data": [val.replace('$', ''), xml_total_stocks()], "headers": ["PDF Value", "XML Value" ], "type": "single"} )
		return json_data



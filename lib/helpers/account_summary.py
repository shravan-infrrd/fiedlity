import re
from constant import PROJECT_ROOT

text_file_path = PROJECT_ROOT + "/temp_files/page-4.txt"
text_file_path_14 = PROJECT_ROOT + "/temp_files/page-14.txt"


with open( text_file_path ) as fp:
    contents = fp.readlines()

with open( text_file_path_14 ) as fp1:
    fourteenth_contents = fp1.readlines()

def find_pattern(str_1, str_2):
    try:
        match = re.compile(r'\b({0})\b'.format( str_1 ), flags=re.IGNORECASE).search(str_2)
        if match is None:
            return False
        else:
            return True
    except:
        print("Error--")
        return False

def net_value_validation():
		net_value_data = {}
		data = []
		table_1 = []
		table_2 = []
		pie_chart = []
		account_validation = []
		market_value_validation = []
		#total_holdings = ""
		for content in fourteenth_contents:
				if 'Total Holdings' in content:
						words = content.strip().split('  ')
						values = list( filter(None, words))
						#print(values)
						total_holdings = values[1]
						#market_value_validation['Total Holdings'] = values[1]
						#market_value_validation.append({"key": "Total Holdings", "value": values[1]})
						market_value_validation.append(values[1])
						break
				
		net_value = ending_net_value = market_value = ""
		account_validation_flag = True
		market_value_validation_flag = True
		for content in contents:

				content = content.strip()

				bond_percent = re.findall(r"\d+% Bonds", content)
				if bond_percent:
						#table_1.append({"key": "Bond Percentage", "value": bond_percent[0]})
						pie_chart.append(["Bonds", bond_percent[0]])
						#pie_chart.append(bond_percent[0])
						#pie_chart["Bond Percentage"] = bond_percent[0]

				stock_percent = re.findall(r"\d+% Stocks", content)
				if stock_percent:
						#table_1.append({"key": "Stock Percentage", "value": stock_percent[0]})
						#pie_chart["Stock Percentage"] = stock_percent[0]
						pie_chart.append(["Stocks", stock_percent[0]])
						#pie_chart.append(stock_percent[0])

				core_account = re.findall(r"\d+% Core Account", content)
				if core_account:
						#table_1.append({"key": "Core Account", "value": core_account[0]})
						#pie_chart["Core Account"] = core_account[0]
						pie_chart.append(["Core Account", core_account[0]])
						#pie_chart.append(core_account[0])

				#print("***1***")
				if 'Ending Net Account Value' in content and not ending_net_value:
						#print(content)
						words = content.split('  ')
						values = list( filter(None, words) )
						ending_net_value = values[1]
						#account_validation.append(  {"key": "Ending Net Account Value", "value": values[1]} )
						#account_validation.append("Ending Net Account Value")
						account_validation.append(values[1].strip())
						#account_validation['Ending Net Account Value'] = values[1]
						continue

				#print("***2***")
				if 'Net Account Value' in content and not net_value:
						words = content.split('  ')
						values = list( filter(None, words) )
						net_value = values[1]
						#account_validation['Net Account Value'] = values[1]
						#account_validation.append(  {"key": "Net Account Value", "value": values[1]} )
						account_validation.append(values[1].strip())
						continue
						#print(values)

				#print("***3***")
				if 'Market Value of Holdings' in content and not market_value:
						#print(content)
						words  = content.split('  ')
						values = list( filter( None, words) )
						market_value = values[1]
						#market_value_validation['Market Value of Holdings'] = values[1]
						#market_value_validation.append({"key": "Market Value of Holdings", "value": values[1]})
						market_value_validation.append(values[1].strip())
						continue
				
				#print(f"***4***net_value={net_value}****ending_net_value={ending_net_value}")
				if net_value and ending_net_value:
	
						#print("------ACCOUNT_VALIDATION-----", net_value)
						if account_validation_flag:
								net_value = float(re.sub("[^\d\.]", "", str(net_value)))
								ending_net_value = float(re.sub("[^\d\.]", "", str(ending_net_value)))
								
								if net_value == ending_net_value:
										#account_validation['result'] = 'pass'
										#account_validation.append(  {"key": "Result", "value": 'pass'} )
										#account_validation.append(net_value)
										#account_validation.append(ending_net_value)
										account_validation.append('pass')
								else:
										#account_validation['result'] = 'failed'
										#account_validation.append(  {"key": "Result", "value": 'failed'} )
										account_validation.append('failed')
								print(True)
								account_validation_flag = False
		 
				if market_value and total_holdings:
						if market_value_validation_flag:
								market_value = float(re.sub("[^\d\.]", "", str(market_value) ) )
								total_holdings = float(re.sub("[^\d\.]", "", str(total_holdings) ) )
								if market_value == total_holdings:
										#market_value_validation['result'] = 'pass'
										#market_value_validation.append({"key": "result", "value": 'pass'})
										market_value_validation.append('pass')
								else:
										#market_value_validation['result'] = 'failed'
										#market_value_validation.append({"key": "result", "value": 'failed'})
										market_value_validation.append('failed')
	
								market_value_validation_flag = False

				#print("***5***")
		#data.append({"description": "validation", "data": [account_validation, market_value_validation ], "headers": ['field_name_1', 'field_name_2', 'Result'] })
		#data.append(market_value_validation)

		data.append( {"description": "Account Validation", "data": account_validation, "headers": ["Ending Net Account", "Net Account", "Result"], 'type': 'single' })
		data.append( {"description": "Market Value Validation", "data": market_value_validation, "headers": ["Total Holdings", "Market Value of Holdings", "Result"], 'type': 'single' } )
		data.append( {"description": "Pie Chart", "data": pie_chart, "headers": ["Description", "Percentage"], 'type': 'multiple' })
		return data

#def market_value_validation():


#data = net_value_validation()
#print(data)


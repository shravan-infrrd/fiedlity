from constant import PROJECT_ROOT
import re


def extract_stocks():
		data = []
		for i in range(5,10):
	
				text_file_path = f"{PROJECT_ROOT}/temp_files/page-{i}.txt"
				with open( text_file_path ) as fp:
						contents = fp.readlines()
				
				flag = False
				page = []
				for content in contents:
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
																data.append(values)
														elif len(values) == 5:
																values.append("")
																data.append(values)
														elif len(values) == 6:
																data.append(values)
														
									

				flag = False

		json_data = []
		json_data.append({"description": "Common Stocks", "data": data, 'type': 'multiple', 'headers': ['Description', 'Beginning Market Value Mar 20, 2019', 'Quantity Mar 21, 2019', 'Price Per Unit Mar 21, 2019', 'Ending Market Value Mar 21, 2019', 'EAI (S$)/ EY (%)']} )
		return json_data


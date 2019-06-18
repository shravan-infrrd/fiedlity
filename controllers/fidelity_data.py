import logging
import time
from flask import Flask, request
from flask import jsonify
from flask_restful import Resource

from controllers.scanned_to_machined import read_scanned_pdf, read_scanned_image
from exceptions.exceptions_handler import *
from constant import PDF_UPLOAD_DIRECTORY, PROJECT_ROOT, REFERENCE_FILE
from os import path
import os
import subprocess
import copy 

from lib.common_methods import populate_missing
from lib.parse_data import get_test_data, get_extraction, get_fidelity_extraction
#from openpyxl import Workbook
#import openpyxl
import uuid

class FidelityData(Resource):


		def get(self):
				return jsonify({"data": get_extraction()})
				#return jsonify({"hello":"wassup!!"})


		def post(self):
				try:
						ts = time.time()
						save_path = PDF_UPLOAD_DIRECTORY
						file = request.files['file']

						file_name = file.filename.replace(' ', '_')
						file_name_without_ext = os.path.basename(file_name).split('.')[0]
						file_name_without_ext = file_name_without_ext + "_" + str(uuid.uuid1())
						extension = path.splitext(file_name)[1]
						file_name = file_name_without_ext + extension #path.splitext(file_name)[1]
						doc_dir_location = os.path.join(save_path, file_name_without_ext)
						if not os.path.exists(doc_dir_location):
								os.makedirs(doc_dir_location)
						file_location = os.path.join(doc_dir_location, file_name)
						file.save( file_location ) 


						#erosion_val = [0, 3, 2, 4]
						erosion_val = [0]
						#erosion_val = [0]
						max_try = len(erosion_val) - 1
						for index, e_val in enumerate(erosion_val):
								print("EROSION_VALUE-------->", e_val)

								
								if extension.lower() in ['.jpg', '.jpeg', '.png']:
										result = read_scanned_image( file_location, doc_dir_location, e_val )
								else:
										result = read_scanned_pdf( file_location, doc_dir_location, e_val )

                
								text_file_path = os.path.join(PDF_UPLOAD_DIRECTORY, file_name_without_ext, 'texts', 'stitched.txt')
								#with open( text_file_path ) as fp:
								#		contents = fp.readlines() 
               
								#result = get_extraction() 
								result = get_fidelity_extraction() 
								result['pdf_file_path'] = 'pdf_file/'		+ file_name_without_ext
								result['excel_file_path'] = 'text_file/' + file_name_without_ext
								#parse_all_fields(contents, result) 

								te = time.time()
								print(f"Time Taken---->{ts - te}")
								#print(f"Time Taken---->{result}")
								return jsonify( {"data": result} )


				except CustomClassifierException as e:
						print("1***ERROR***", e)
						logging.error("Error {} has occurred in controller".format(e))
						return e.response, e.http_code

				except Exception as e:
						print("2***ERROR***", e)
						logging.error("Error in service = {}".format(e), exc_info=True)
						return InternalServerErrorException(error_code=500,
																								error_message="Data Extraction failed!").response, 500

				finally:
						logging.info("API Call Finished Successfully - 200")


		def create_template(self, template_path):
				sample_copy_path = "/Users/shravanc/flask/aditya_birla/ocr-pdf-aditya-malaysia/sample_copy/sample.xlsx"
				

				a = ['cp', sample_copy_path, template_path]
				template_file = os.path.join(template_path, 'sample.xlsx')
				res = subprocess.check_output(a)
				print(res)
				return template_file


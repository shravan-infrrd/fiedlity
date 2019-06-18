
import time
from flask import Flask, request
from flask import send_from_directory
from flask import jsonify
from flask_restful import Resource

#from lib.common_methods import populate_missing
#from lib.parse_data import parse_all_fields

class AccountSummary(Resource):

		def get(self):
				print("===Account Summary intitiated===")
				data = parse_all_fields()
				print(data)
				resp = send_from_directory("static", "account_summary.html")
				return resp
				#return jsonify(data)

		def post(self):
				print("===Account Summary intitiated===")
				data = parse_all_fields()
				print(data)
				return jsonify(data)

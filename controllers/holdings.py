import time
from flask import Flask, request
from flask import jsonify
from flask_restful import Resource

from lib.parse_data import parse_holding_data

class Holdings(Resource):
		def get(self):	
				print("====Holdings Initiated====")
				data = parse_holding_data()
				return jsonify(data)


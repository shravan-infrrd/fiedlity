
import time
from flask import Flask, request
from flask import jsonify
from flask_restful import Resource

from lib.parse_data import parse_stock_data

class Stocks(Resource):
		def get(self):
				print("====Stock Initiated====")
				data = parse_stock_data()
				return jsonify(data)

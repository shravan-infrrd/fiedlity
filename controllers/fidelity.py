import time
from flask import Flask, request
from flask import send_from_directory
from flask import jsonify
from flask_restful import Resource

#from lib.common_methods import populate_missing
from lib.parse_data import get_extraction

class Fidelity(Resource):

		def get(self):
				return jsonify(get_extraction())

		def post(self):
				return jsonify(get_extraction())


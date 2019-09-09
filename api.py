from flask import Flask, request,Blueprint, jsonify
import logging
import json
import pymysql
import pickle
import pandas as pd
import numpy as np


connection = pymysql.connect(host='database-1.cshajwbkyfv1.ap-southeast-1.rds.amazonaws.com',
                             port=3306,
                             user='BT3101',
                             password='password',
                             db='appareldb')
cursor = connection.cursor()

api = Flask(__name__)
@api.route('/api/test_api', methods = ['POST'])
def index():
    return json.dumps({'testing':'hello world!'})

@api.route('/customerAge', methods =['GET'])
def getMeanAge():
    sql = '''Select AVG(CustomerAge) from `measurements_data`'''
    cursor.execute(sql)
    result = cursor.fetchone()
    return {'result':result[0]}

api.run(host="0.0.0.0", port=8000, debug=True)

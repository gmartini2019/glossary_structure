from flask import Flask, request, jsonify
import redis
import csv
import msgpack
import pandas as pd
import time
import argparse

app = Flask(__name__)

@app.route('/store', methods=['POST'])
def store():
    csv_file = request.form['csv_file']
    
    # Read data from CSV
    df = pd.read_csv(csv_file)
    
    # Store data in Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    start = time.time()
    r.set("key", msgpack.packb(df.to_dict('records')))
    end = time.time()
    elapsed = end - start
    
    return jsonify({'message': f'Data stored successfully. Time elapsed: {elapsed:.2f} seconds'})

@app.route('/get', methods=['GET'])
def get():
    # Retrieve data from Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    binary_data = r.get('key')
    
    if binary_data:
        # Unpack data from Redis and convert to DataFrame
        data = msgpack.unpackb(binary_data, raw=False)
        df = pd.DataFrame(data)
        
        return jsonify(df.to_dict('records'))
    else:
        return jsonify({'error': 'Data not found.'})

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Store CSV data in Redis and retrieve it as a JSON.')
    parser.add_argument('csv_file', type=str, help='path to the CSV file')
    args = parser.parse_args()

    # Read data from CSV
    df = pd.read_csv(args.csv_file)

    # Store data in Redis
    r = redis.StrictRedis(host='localhost', port=6379, db=0)
    start = time.time()
    r.set("key", msgpack.packb(df.to_dict('records')))
    end = time.time()
    elapsed = end - start

    print(f'Data stored successfully. Time elapsed: {elapsed:.2f} seconds')

    # Retrieve data from Redis and print as JSON
    binary_data = r.get('key')
    if binary_data:
        # Unpack data from Redis and convert to DataFrame
        data = msgpack.unpackb(binary_data, raw=False)
        df = pd.DataFrame(data)
        print(df.to_json(orient='records'))
    else:
        print('Data not found.')

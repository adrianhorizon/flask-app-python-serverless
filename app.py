import os

import boto3

from flask import Flask, jsonify, request

app = Flask(__name__)

USERS_TABLE = os.environ['USERS_TABLE']
IS_OFFLINE = os.environ.get('IS_OFFLINE')

if IS_OFFLINE:
    client = boto3.client(
        'dynamodb',
        region_name='localhost',
        endpoint_url='http://localhost:8000'
    )
else:
    client = boto3.client('dynamodb')


@app.route(r"/contacts", methods=["GET"])
def list_books():
    resp = client.scan(TableName=USERS_TABLE)

    return jsonify(resp.get('Items'))


@app.route(r"/contacts/<string:user_id>")
def get_book(user_id):
    resp = client.get_item(
        TableName=USERS_TABLE,
        Key={
            'userId': {'S': user_id}
        }
    )
    item = resp.get('Item')
    if not item:
        return jsonify({'error': 'Contact does not exist'}), 404

    return jsonify({
        'userId': item.get('userId').get('S'),
        'name': item.get('name').get('S'),
        'phone': item.get('phone').get('N'),
        'email': item.get('email').get('S')
    })


@app.route(r"/contacts", methods=["POST"])
def add_book():
    user_id = request.json.get('userId')
    name = request.json.get('name')
    phone = request.json.get('phone')
    email = request.json.get('email')
    if not user_id or not name:
        return jsonify({'error': 'Please provide userId and name, phone, email'}), 400

    resp = client.put_item(
        TableName=USERS_TABLE,
        Item={
            'userId': {'S': user_id},
            'name': {'S': name},
            'phone': {'N': phone},
            'email': {'S': email}
        }
    )

    return jsonify({
        'userId': user_id,
        'name': name,
        'phone': phone,
        'email': email,
    })


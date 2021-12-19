import datetime
import json

import requests
from flask import render_template, redirect, request

from app import app

port = 9000
CONNECTED_NODE_ADDRESS = "http://127.0.0.1:{}".format(port)

posts = []

#this function gets the data from the node’s /chain endpoint, parses the data, and stores it locally.

def fetch_posts():
    
    get_chain_address = "{}/chain".format(CONNECTED_NODE_ADDRESS)
    respons = requests.get(get_chain_address)
    if respons.status_code == 200:
        content = []
        chain = json.loads(respons.content)
        for block in chain['chain']:
            for tx in block['transactions']:
                tx['index'] = block['index']
                tx['hash']=block['previous_hash']
                content.append(tx)
            
        global posts
        posts = sorted(content,key=lambda k:k['timestamp'],reverse=True)
    
@app.route('/submit',methods=['POST'])
def submit_textarea():
    region = request.form["region"]
    constituency = request.form["constituency"]
    author = request.form["author"]
    post_content = request.form["party"]
    vote_number= request.form['vote_in_number']
    vote_words= request.form['vote_in_words']
    rejected_ballot= request.form['rejected_ballot']
    post_object = {region:{constituency:{author:{post_content:vote_number,'vote_in_words':vote_words,'rejected_ballot':rejected_ballot}}}}
    # post_object = {'author': author,'party':post_content,'vote_in_number':vote_number,'vote_in_words':vote_words,'rejected_ballot':rejected_ballot,'region':region,"constituency":constituency}
    new_tx_address = "{}/new_transaction".format(CONNECTED_NODE_ADDRESS)
    print(new_tx_address)
    requests.post(new_tx_address,json=post_object,headers={'Content-type': 'application/json'})
    return redirect('/')

@app.route('/')
def home():
    return render_template('/index.html')


if __name__ == '__main__':
    app.run( host='127.0.0.1',port=port)
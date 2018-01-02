#Basic FB Messenger chatbot implementation via API-AI (Dialogflow) using Python Flask - Python - Jose Ahirton Lopes (FCamara)

"""
__author__ = "Ahirton Lopes"
__copyright__ = "Copyright 2017/2018, FCamara/Duratex"
__credits__ = ["Ahirton Lopes"]
__license__ = "None"
__version__ = "1.0"
__maintainer__ = "Ahirton Lopes"
__email__ = "ahirtonlopes@gmail.com"
__status__ = "Beta"
"""

import requests
import json
from flask import Flask, request
import apiai

# Credenciais de acesso ao FB messenger
ACCESS_TOKEN = ""

# Credenciais de acesso referentes ao API.AI
CLIENT_ACCESS_TOKEN = ""
ai = apiai.ApiAI(CLIENT_ACCESS_TOKEN)

app = Flask(__name__)

@app.route('/', methods=['GET'])
def verify():

    # O endpoint deve ecoar o valor especificado de 'hub.challenge' ao setarmos o webhook
    
    if request.args.get("hub.mode") == "subscribe" and request.args.get("hub.challenge"):
        if not request.args.get("hub.verify_token") == 'foo':
            return "Problema na verificacao do token de seguranca", 403
        return request.args["hub.challenge"], 200

    return 'Hello world, bem vindo ao teste de chatbot básico no messenger (Tamo junto!)', 200

def reply(user_id, msg):
    data = {
        "recipient": {"id": user_id},
        "message": {"text": msg}
    }
    resp = requests.post("https://graph.facebook.com/v2.6/me/messages?access_token=" + ACCESS_TOKEN, json=data)
    print(resp.content)


@app.route('/', methods=['POST'])
def handle_incoming_messages():
    data = request.json
    sender = data['entry'][0]['messaging'][0]['sender']['id']
    message = data['entry'][0]['messaging'][0]['message']['text']

    # Preparando requisição ao API.ai
    
    req = ai.text_request()
    req.lang = 'pt-BR'
    req.query = message

    # Aquisição de resposta via API.ai
    
    api_response = req.getresponse()
    responsestr = api_response.read().decode('utf-8')
    response_obj = json.loads(responsestr)
    if 'result' in response_obj:
        response = response_obj["result"]["fulfillment"]["speech"]
        reply(sender, response)

    return "ok"

if __name__ == '__main__':
    app.run(debug=True)
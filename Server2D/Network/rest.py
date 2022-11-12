from flask import Flask, jsonify, request
from flask import make_response, abort
import os
import Database.database as db

def Init():
    global _app
    _app = Flask(__name__)

    @_app.route('/newgame/<int:id>', methods=['GET'])
    def get_newgame(id=0):
        print("Starting new game")
        db.SetCharPos(id, 320, 240)
        return db.GetCharData(id)

    # @_app.route('/savepos/<int:id>', methods=['POST'])
    # def set_savepos(id=0):
    #     print("Saving game")
    #     if not request.json or not 'x' in request.json or not 'y' in request.json:
    #         abort (400)
    #     db.SetCharPos(id, int(request.json['x']), int(request.json['y']))
    #     return db.GetCharData(id)

    @_app.route('/savepos/<int:id>', methods=['POST'])
    def update_savepos(id=0):
        print("Updating gamesave")
        if not request.json or not 'x' in request.json or not 'y' in request.json:
            abort (400)
        db.SetCharPos(id, int(request.json['x']), int(request.json['y']))
        return db.GetCharData(id)
    
    @_app.route('/savepos/<int:id>', methods=['GET'])
    def get_savepos(id=0):
        print("Loading game")
        db.GetCharPos(id)
        return db.GetCharData(id) ##GetPos

def Run():
    global _app
    _app.run(port='5005', threaded = True)
    pass
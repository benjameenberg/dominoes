#!/usr/bin/env python
import logging
import os
import random
import sys
import traceback

#from google.appengine.api import app_identity
#from google.appengine.ext import ndb
import flask
from flask import Flask, render_template, request
from make_dominoes import mkhtml_str

from dominoes import Player, Board, Game
from strategies import Player_Input_Strategy, Block_If_Possible_Strategy, Bota_Gorda

# from google.appengine.ext import users         NOT FOUND< WHAT IS THIS FOR?

logging.basicConfig(level=logging.DEBUG)
logging.info('Loaded %s', __name__)

# Add any libraries installed in the "lib" folder.
#from google.appengine.ext import vendor
# vendor.add('lib')

#from model import AppDescription, SojoinApp, Category

# cloudstorage.set_default_retry_params(
#    cloudstorage.RetryParams(
#        initial_delay=0.2, max_delay=5.0, backoff_factor=2, max_retry_period=15
#        ))

# Bootstrapping.  Better way?
#JOINT_KEY = ndb.Key(Category, 'joint')
#jointCategory = JOINT_KEY.get()
# if not jointCategory:
#    jointCategory = Category(key=JOINT_KEY,name='joint')
#    JOINT_KEY = jointCategory.put()

app = Flask('dominoes-ui')  # not __name__ sojoinery.sojoinery
# flask_cors.CORS(app) To allow cross origin requests

p1 = Player("Ben")
p2 = Player("Kitty")
p3 = Player("Lucio")
p4 = Player("Harry")

p1.assign_strategy(Block_If_Possible_Strategy())
p3.assign_strategy(Block_If_Possible_Strategy())
p4.assign_strategy(Bota_Gorda())

players = [p1, p2, p3, p4]
game = Game([p1, p2, p3, p4])


@app.after_request
def add_header(response):
    response.cache_control.max_age = 300
    response.add_etag()
    return response


@app.route('/', methods=['GET'])
def main():
    global game
    sys.stderr.write("Get %s\n" % request)
    logging.info('main()')

    try:
        headers = {'Content-Type': 'text/html'}
        return (mkhtml_str(game.board.board_dominoes), headers)
    except Exception as e:
        logging.exception('/ root path %s', e)
        tb = traceback.format_exc()
        return (tb, 500, {})


@app.route('/next', methods=['GET'])
def advance_board():
    game.next()
    print(game.play_msg)
    print(game.round_msg)


@app.route('/game/<player_name>', methods=['GET'])
def player_board(player_name):
    logging.info('player_board(%s)', player_name)

    # is p has the player name we want
    for p in players:
        if p.name == player_name:
            player_dominoes = p.dominoes
            break
    else:
        return code_404('No player {}'.format(player_name))

    headers = {'Content-Type': 'text/html'}

    data = mkhtml_str(player_dominoes, title=player_name)
    return (data, headers)


@app.errorhandler(404)
def code_404(error):
    return code_err(error, msg='Not found', code=404)


@app.errorhandler(400)
def code_400(error):
    return code_err(error, msg='Invalid', code=400)


@app.errorhandler(500)
def code_500(error):
    return code_err(error,  msg='Unexpected error', code=500)


def code_err(error, msg, code):
    exc_type, _value, _tb = sys.exc_info()
    if exc_type is not None:
        logging.exception('Error %s handling request', code)
        msg = exc_type.__name__
    return '''
<html><body>
<div style="align: center;text-align: center">
<img src="/static/404.png" width=100 height=100 />
<br><hr><b>{}: {} {}: {}
</div>
</body></html>'''.format(flask.current_app.name, code, msg, error), code


if __name__ == '__main__':
    app.run()

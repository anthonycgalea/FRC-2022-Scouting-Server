from flask import (
    Flask
    , render_template
    , redirect
    , request
    , jsonify
    , url_for
)
from flask_sqlalchemy import SQLAlchemy
import os, requests
from models import constants
from requests.exceptions import HTTPError

basedir = os.path.abspath(os.path.dirname(__file__))
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir, 'data/ScoutingData.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Team(db.Model):
    '''
    Database model for a Team table. Only includes rudimentary team information to not clutter.
    '''
    teamNumber = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    teamName = db.Column(db.String(50), nullable=False)
    teamCity = db.Column(db.String(50))
    teamState = db.Column(db.String(50))

class Match(db.Model):
    '''
    Database model for a Match table. Only includes match number and team members of an alliance.
    '''
    matchNo = db.Column(db.Integer, primary_key=True, nullable=False, unique=True)
    red_1 = db.Column(db.Integer, nullable=False)
    red_2 = db.Column(db.Integer, nullable=False)
    red_3 = db.Column(db.Integer, nullable=False)
    blue_1 = db.Column(db.Integer, nullable=False)
    blue_2 = db.Column(db.Integer, nullable=False)
    blue_3 = db.Column(db.Integer, nullable=False)

class TeamMatch(db.Model):
    '''
    Database model for recording a team's performance in a match.
    '''
    teamMatchId = db.Column(db.Integer, primary_key=True) #tuid
    matchNo = db.Column(db.Integer, db.ForeignKey('Match.matchNo'), nullable=False)
    teamNo = db.Column(db.Integer, db.ForeignKey('Team.teamNumber'), nullable=False)
    #TODO: Insert game-specfic data here
    
    #Autonomous
    autoTaxi = db.Column(db.Integer) #this is an integer to make data handling in Tableau easier
    autoLow = db.Column(db.Integer)
    autoHigh = db.Column(db.Integer)
    autoPickedUp = db.Column(db.Integer)
    autoNotes = db.Column(db.String(255))
    
    #Teleop
    teleLow = db.Column(db.Integer)
    teleHigh = db.Column(db.Integer)
    telePickedUp = db.Column(db.Integer)
    didDefense = db.Column(db.Boolean)
    teleDefense = db.Column(db.Integer)
    teleNotes = db.Column(db.String(255))
    
    #Endgame
    attemptedClimb = db.Column(db.Boolean)
    levelClimbed = db.Column(db.Integer)
    endgameNotes = db.Column(db.String(255))
    
    #generic game data
    brokenBot = db.Column(db.Boolean)
    noShow = db.Column(db.Boolean)
    fouls = db.Column(db.Integer)
    generalNotes = db.Column(db.String(255))

class TeamPitScout(db.Model):
    '''
    Database model for pit scouting information for a team.
    '''
    TeamPitScoutId = db.Column(db.Integer, primary_key=True)
    teamNo = db.Column(db.Integer, db.ForeignKey('Team.teamNumber'), nullable=False)
    #TODO: Insert game-specific data here

#TODO: replace this with a 
def getTeamInfo(teamNo):
    url = f"{constants.tba_base}{teamNo}.json?key={constants.tba_key}"
    res = requests.get(url)
    res_json = res.json()
    info = tuple(
        [
            res_json["results"][0]["nickname"],
            res_json["results"][0]["city"],
            res_json["results"][0]["state_prov"],
        ]
    )
    return info

@app.route("/")
def index():
    '''
    Flask method for returning homepage.
    '''
    return render_template("index.html")

from flask import Flask, jsonify
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station
#################################################
# Flask Setup
#################################################


app = Flask(__name__)

#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/precipitation")
def precipitation():
    """Return the precipiation data as json"""
    # Create our session (link) from Python to the DB
    session = Session(engine)
   # Design a query to retrieve the last 12 months of precipitation data and plot the results
    precipitation=session.query(Measurement.date, Measurement.prcp).\
    filter(Measurement.date >= '2016-08-23').\
    order_by(Measurement.date).all()
    precipitation

    return jsonify(precipitation)

@app.route("/api/v1.0/stations")
def stations():
    """Return the station data as json"""
    # Create our session (link) from Python to the DB
    session = Session(engine)
    station1=session.query(Station.id, Station.name,
                          Station.station).\
        order_by(Station.id).all()
    station1
    #resultsstat
    return jsonify(station1)

@app.route("/api/v1.0/tobs")
def tobs():
    """Return the temperature data as json"""
# Create our session (link) from Python to the DB
    session = Session(engine)

    Temperature1=session.query(Measurement.station, Measurement.tobs, Measurement.date).\
    filter(Measurement.date >= '2016-08-23').\
    filter(Measurement.station == "USC00519281").\
    order_by(Measurement.date).all()
    Temperature1

    return jsonify(Temperature1)

@app.route("/api/v1.0/temp2")
def temp2():
    session = Session(engine)

    temperature2=session.query((func.min(Measurement.tobs)), 
                         (func.max(Measurement.tobs)),
                         (func.avg(Measurement.tobs))).\
    filter(Measurement.date >= '2016-09-15').all()
    temperature2


    return jsonify(temperature2)

@app.route("/api/v1.0/temp3")
def temp3():
    session = Session(engine)

    temperature3=session.query((func.min(Measurement.tobs)), 
                         (func.max(Measurement.tobs)),
                         (func.avg(Measurement.tobs))).\
    filter(Measurement.date >= '2016-09-15', Measurement.date <= '2016-09-30').all()
    temperature3


    return jsonify(temperature3)

@app.route("/")
def welcome():
    return (
        f"Welcome to the Climate Weather API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/temp2<br/>"
        f"/api/v1.0/temp3"
    )


if __name__ == "__main__":
    app.run(debug=True)
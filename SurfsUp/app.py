import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

import pandas as pd
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
#engine = create_engine("sqlite:///C:\\Users\\Dan\\Documents\\Python Scripts\\sqlalchemy-challenge\\SurfsUp\\Resources\\hawaii.sqlite")
# 

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)

measurement = Base.classes.measurement

station = Base.classes.station


#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################


@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/&lt;start&gt;<br/>"
        f"/api/v1.0/&lt;end&gt;"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)

    max_date = dt.date(2017, 8, 23)

    min_date = max_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    prec_data = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= min_date).\
        order_by(measurement.date).all()
    
    session.close()

    precs = []
    for date, prcp in prec_data:
        precs_dict = {}
        precs_dict["date"] = date
        precs_dict["prcp"] = prcp
        precs.append(precs_dict)

    return jsonify(precs)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)

    stats = session.query(measurement.station).all()

    session.close()

    stations = []
    for station in stats:
        stat_dict = {}
        stat_dict["station"] = station[0]
        stations.append(stat_dict)

    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    session = Session(engine)

    stat_name = 'USC00519281'

    max_date = dt.date(2017, 8, 23)
    min_date = max_date - dt.timedelta(days=365)

    # Perform a query to retrieve the data and precipitation scores
    twelve_month_temps = session.query(measurement.tobs).\
                            filter(measurement.station==stat_name).\
                            filter(measurement.date >= min_date).all()
    
    session.close()

    temps = []
    for t in twelve_month_temps:
        temp_dict = {}
        temp_dict["tobs"] = t[0]
        temps.append(temp_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>")
def start(start):

    stat_name = 'USC00519281'

    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))

    session = Session(engine)

    sel = [measurement.station, 
        func.avg(measurement.tobs), 
        func.min(measurement.tobs), 
        func.max(measurement.tobs)]
    temps = session.query(*sel).\
            filter(measurement.station==stat_name).\
            filter(measurement.date >= start_date).all()

    #print(f"Station: {stemps[0]}, Avg = {stemps[1]}, Min = {stemps[2]}, Max = {stemps[3]}")

    session.close()

    stemps = temps
    
    temps = []
    for t in stemps:
        temp_dict = {}
        temp_dict["station"] = t[0]
        temp_dict["TAVG"] = t[1]
        temp_dict["TMIN"] = t[2]
        temp_dict["TMAX"] = t[3]
        temps.append(temp_dict)

    return jsonify(temps)


@app.route("/api/v1.0/<start>/<end>")
def end(start, end):
    stat_name = 'USC00519281'

    try:
        start_date = dt.datetime.strptime(start, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))

    try:
        end = dt.datetime.strptime(end, "%Y-%m-%d").date()
    except ValueError:
        raise ValueError('{} is not valid date in the format YYYY-MM-DD'.format(date_string))


    session = Session(engine)

    sel = [measurement.station, 
        func.avg(measurement.tobs), 
        func.min(measurement.tobs), 
        func.max(measurement.tobs)]
    temps = session.query(*sel).\
            filter(measurement.station==stat_name).\
            filter(measurement.date >= start_date).\
            filter(measurement.date <= end).all()

    #print(f"Station: {stemps[0]}, Avg = {stemps[1]}, Min = {stemps[2]}, Max = {stemps[3]}")

    session.close()

    stemps = temps
    
    temps = []
    for t in stemps:
        temp_dict = {}
        temp_dict["station"] = t[0]
        temp_dict["TAVG"] = t[1]
        temp_dict["TMIN"] = t[2]
        temp_dict["TMAX"] = t[3]
        temps.append(temp_dict)

    return jsonify(temps)


if __name__ == "__main__":
    app.run(debug=True)

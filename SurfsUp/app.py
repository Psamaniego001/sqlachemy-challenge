# Import the dependencies.
import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
import datetime as dt

from flask import Flask, jsonify

#################################################
# Database Setup
#################################################

# reflect an existing database into a new model
engine = create_engine("sqlite:///Resources/hawaii.sqlite")
Base = automap_base()
Base.prepare(autoload_with=engine)

# Save references to each table
measurement = Base.classes.measurement
station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(bind=engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)
#################################################
# Flask Routes
#################################################

@app.route("/")
def home():
    return (
        f"Welcome to the Temperature API<br/>"
        f"<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start date/<start_date><br/>"
        f"/api/v1.0/start date/<start_date>/end date/<end_date><br/>"
        f"<br/>"
        f"<br/>"
        f"Please add the date at the end of the path, use the following format for the dates YYYYMMDD"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    
    session = Session(engine)
    
    precipitation = session.query(measurement.date, measurement.prcp).\
        filter(measurement.date >= '2016-08-23').all()                        
    
    session.close()

    precipitation_list = []
    
    for date, prcp in precipitation:
        precipitation_dic = {}
        precipitation_dic['date'] = date
        precipitation_dic['prcp'] = prcp
        precipitation_list.append(precipitation_dic)

    return jsonify(precipitation_list)

@app.route("/api/v1.0/stations")
def stations():

    session = Session(engine)

    stations_list = session.query(station.station, station.name).all()
    
    session.close()

    stations_new_list = []
    for st, names in stations_list:
         st_dic = {}
         st_dic['st'] = st
         st_dic['names'] = names
         stations_new_list.append(st_dic)
    #stations_ist = list(np.ravel(stations_list))

    #return jsonify(stations_ist)
    return jsonify(stations_new_list)

@app.route("/api/v1.0/tobs")
def tobs():

    session = Session(engine)

    most_active_station = session.query(measurement.station, measurement.date, measurement.tobs).\
        filter(measurement.station == 'USC00519281').\
        filter(measurement.date >= '2016-08-23').all()
    
    session.close()

    most_active_station_list = []
    for st, dates, tobs in most_active_station:
         active_dic = {}
         active_dic['st'] = st
         active_dic['date'] = dates
         active_dic['temperature'] = tobs
         most_active_station_list.append(active_dic)
    #stations_ist = list(np.ravel(stations_list))

    #return jsonify(stations_ist)
    return jsonify(most_active_station_list)

@app.route("/api/v1.0/start date/<start_date>")
def stats(start_date):

    adj_start_date = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"

    #print(adj_start_date)

    session = Session(engine)

    max_temp = session.query(func.max(measurement.tobs)).\
    filter(measurement.date >= adj_start_date).scalar()

    min_temp = session.query(func.min(measurement.tobs)).\
    filter(measurement.date >= adj_start_date).scalar()

    avg_temp = session.query(func.avg(measurement.tobs)).\
    filter(measurement.date >= adj_start_date).scalar()

    avg_temp_v1 = round(avg_temp,1)

    session.close()

    #print(adj_start_date)

    # min_temp = session.query(func.min(measurement.tobs)).\
    # filter(measurement.date >= start_date)
    dict = {"Start Date": adj_start_date, "max temp": max_temp, "min temp": min_temp, "avg temp": avg_temp_v1}

    return jsonify(dict)

@app.route("/api/v1.0/start date/<start_date>/end date/<end_date>")
def stats1(start_date, end_date):

    start_date_v1 = f"{start_date[:4]}-{start_date[4:6]}-{start_date[6:8]}"
    end_date_v1 = f"{end_date[:4]}-{end_date[4:6]}-{end_date[6:8]}"

    #print(adj_start_date)

    session = Session(engine)

    max_temp = session.query(func.max(measurement.tobs)).\
        filter(measurement.date >= start_date_v1).\
        filter(measurement.date <= end_date_v1).scalar()

    min_temp = session.query(func.min(measurement.tobs)).\
        filter(measurement.date >= start_date_v1).\
        filter(measurement.date <= end_date_v1).scalar()

    avg_temp = session.query(func.avg(measurement.tobs)).\
        filter(measurement.date >= start_date_v1).\
        filter(measurement.date <= end_date_v1).scalar()

    avg_temp_v1 = round(avg_temp,1)

    session.close()

    # #print(adj_start_date)

    dict = {"Start Date": start_date_v1,"End Date": end_date_v1, "max temp": max_temp, "min temp": min_temp, "avg temp": avg_temp_v1}

    return (dict)


if __name__ == "__main__":
    app.run(debug=True)


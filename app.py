import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)

# List all routes that are available.
@app.route("/")
def home():
    print("request received for list of all routes")
    return (
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start> and /api/v1.0/<start>/<end>"
    )

#Convert the query results to a Dictionary using date as the key and prcp as the value.
# Return the JSON representation of your dictionary.
@app.route("/api/v1.0/precipitation")
def precip():
    session = Session(engine)
    query_date_last = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    date_full_year = dt.datetime.strptime(query_date_last, "%Y-%m-%d") - dt.timedelta(days=365)
    prcp_last12mon = session.query(Measurement.date,Measurement.prcp).\
        filter(Measurement.date>=date_full_year).all()
    session.close()
    prcp_1yr = []
    for date, prcp in prcp_last12mon:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_1yr.append(prcp_dict)

    return jsonify(prcp_1yr)

# Return a JSON list of stations from the dataset.
@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    query_stations=session.query(Station.name).all()
    session.close()
    all_stations = list(np.ravel(query_stations))
    return jsonify(all_stations)








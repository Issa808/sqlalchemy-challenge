#import dependencies
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func, inspect

from flask import Flask, jsonify


# create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(autoload_with=engine)


# Save references to each table
station = Base.classes.station
measurement = Base.classes.measurement

#Flask Setup
app = Flask(__name__)



@app.route("/")
def Welcome():
    return(
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<start><br/>"
        f"/api/v1.0/<start>/<end>"
    )

#Route for Precipitation
@app.route("/api/v1.0/precipitation")
def precipitation():
    #create session
    session = Session(engine)
    # Perform a query to retrieve the data and precipitation scores
    scores = session.query(measurement.date, measurement.prcp).\
            filter(measurement.date >= '2016-08-23').all()

     #close session
    session.close()

    prcp = dict(scores)

    #Return the JSON representation of your dictionary.
    return jsonify(prcp)

#Route for Stations
@app.route("/api/v1.0/stations")
def stations():
    #Create Cession
    session = Session(engine)

    #List the stations and the counts in descending order.
    stations_order = session.query(measurement.station).group_by(measurement.station).\
        order_by(func.count(measurement.station).desc()).all()

    #Close Session
    session.close()

    #Convert to Lists
    stations_list = list(np.ravel(stations_order))

    #Return a JSON list of stations from the dataset.
    return jsonify(stations_list)

#Route for Tobs
@app.route("/api/v1.0/tobs")
def tobs():
    #Create Session
    session = Session(engine)

    #Query the last 12 months of temperature observation data for this station and plot the results as a histogram
    results = session.query(measurement.tobs).filter(measurement.station == 'USC00519281').\
	filter(measurement.date >= '2016-08-23').all()

    #Close Cession
    session.close()

    #Convert to Lists
    temp_list = list(np.ravel(results))

    #Return a JSON list of temperature observations
    return jsonify(temp_list)


#Route for Start Date
@app.route("/api/v1.0/<start>")
def start(start):
    #create session
    session = Session(engine)

    temp = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
	filter(measurement.date >= start).all()


    #close session
    session.close()

    #Convert to Lists
    temp_list = list(np.ravel(temp))

    return jsonify({"Lowest Temperature": temp_list[0]}, {"Highest Temperature": temp_list[1]}, {"Average Temperature": temp_list[2]} )




@app.route("/api/v1.0/<start>/<end>")
def end(start,end):
    #Create Session
    session = Session(engine)

    temp = session.query(func.min(measurement.tobs), func.max(measurement.tobs),func.avg(measurement.tobs)).\
	filter(measurement.date >= start).filter(measurement.date <= end).all()

    #Close Cession
    session.close()

    #Convert to Lists
    temp_list = list(np.ravel(temp))

    return jsonify({"Lowest Temperature": temp_list[0]}, {"Highest Temperature": temp_list[1]}, {"Average Temperature": temp_list[2]})


if __name__ == '__main__':
    app.run(debug=True)

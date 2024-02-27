# Import the dependencies.
from flask import Flask, jsonify
import datetime as dt
from datetime import datetime
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()
# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Station = Base.classes.station
Measurement = Base.classes.measurement

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################
@app.route('/')
def home():
    return '''
    <h1>Climate App</h1>
    <p>Available Routes:</p>
    <ul>
        <li><a href="/api/v1.0/precipitation">/api/v1.0/precipitation</a></li>
        <li><a href="/api/v1.0/stations">/api/v1.0/stations</a></li>
        <li><a href="/api/v1.0/tobs">/api/v1.0/tobs</a></li>
        <li>/api/v1.0/&lt;start&gt;</li>
        <li>/api/v1.0/&lt;start&gt;/&lt;end&gt;</li>
    </ul>
    Note: Replace &lt;start&gt; and &lt;end&gt; with actual dates in the format YYYY-MM-DD for the last two routes.
    '''

@app.route('/api/v1.0/precipitation')
def precipitation():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a list of all precipitation data"""
    # Query all precipitation data
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

    # Create a dictionary from the row data and append to a list of all_passengers
    all_precipitation = []
    for date, prcp in results:
        precipitation_dict = {}
        precipitation_dict[date] = prcp
        all_precipitation.append(precipitation_dict)

    return jsonify(all_precipitation)

@app.route('/api/v1.0/stations')
def stations():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of stations from the dataset."""
    # Query all stations
    results = session.query(Station.station).all()

    session.close()

    # Convert list of tuples into normal list
    all_stations = list(np.ravel(results))

    return jsonify(all_stations)

@app.route('/api/v1.0/tobs')
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    """Return a JSON list of temperature observations (TOBS) for the previous year."""
    # Calculate the date 1 year ago from last date in database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    last_date = last_date[0]
    last_date = datetime.strptime(last_date, '%Y-%m-%d')
    one_year_ago = last_date - dt.timedelta(days=365)

    # Query the primary station for all tobs from the last year
    results = session.query(Measurement.tobs).\
        filter(Measurement.date >= one_year_ago).\
        filter(Measurement.station == 'USC00519281').all()

    session.close()

    # Convert list of tuples into normal list
    all_tobs = list(np.ravel(results))

    return jsonify(all_tobs)

# Define additional routes for /api/v1.0/<start> and /api/v1.0/<start>/<end> as needed

if __name__ == '__main__':
    app.run(debug=True)


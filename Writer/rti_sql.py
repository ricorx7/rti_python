import psycopg2


"""
Update tables
ALTER TABLE ensembles ADD COLUMN project_id integer;
ALTER TABLE ensembles ADD COLUMN created timestamp;
ALTER TABLE ensembles ADD COLUMN modified timestamp;
"""

class rti_sql:


    def __init__(self, conn):
        """
        Make a connection to the database
        :param conn: "host='localhost' dbname='my_database' user='postgres' password='secret'"
        """
        self.conn_string = conn
        self.conn = None
        self.cursor = None

        # Make a connection
        self.sql_conn(conn)

    def sql_conn(self, conn_string):
        # print the connection string we will use to connect
        print("Connecting to database\n	->%s" % (conn_string))

        # get a connection, if a connect cannot be made an exception will be raised here
        self.conn = psycopg2.connect(conn_string)

        # conn.cursor will return a cursor object, you can use this cursor to perform queries
        self.cursor = self.conn.cursor()
        print("Connected!\n")

    def close(self):
        self.cursor.close()
        self.conn.close()

    def query(self, query):
        """
        Send the query and get the results from the query
        :param query: Query to execute on the database.
        :return: Results of query.  It is iterable.
        """
        print(query)
        self.cursor.execute(query)      # Send query
        self.conn.commit()

        # Return the results
        return self.cursor.fetchall()

    def insert(self, query):
        """
        Send the query to insert data.  There is no fetch with an insert.
        :param query: Query to execute on the database.
        :return: Results of query.  It is iterable.
        """
        print(query)
        self.cursor.execute(query)      # Send query to insert data
        self.conn.commit()

    def execute(self, query):
        return self.cursor.execute(query)

    def commit(self):
        return self.conn.commit()

    def create_tables(self):
        # Project
        self.cursor.execute('CREATE TABLE IF NOT EXISTS projects (id SERIAL PRIMARY KEY, '
                            'name text NOT NULL, '
                            'path text,'
                            'created timestamp, '
                            'modified timestamp);')
        print("Projects table created")

        # Ensemble Tables
        # Ensemble
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ensembles (id SERIAL PRIMARY KEY, '
                            'ensNum integer NOT NULL, '
                            'numBins integer, '
                            'numBeams integer, '
                            'desiredPings integer, '
                            'actualPings integer, '
                            'status integer, '
                            'dateTime timestamp, '
                            'serialNumber text, '
                            'firmware text,'
                            'subsystemConfig character, '
                            'project_id integer, '
                            'created timestamp, '
                            'modified timestamp);')
        print("Ensemble Table created")

        # Ancillary
        self.cursor.execute('CREATE TABLE IF NOT EXISTS ancillary (id SERIAL PRIMARY KEY, '
                            'ensIndex integer NOT NULL, '
                            'rangeFirstBin real, '
                            'binSize real, '
                            'firstPingTime real, '
                            'lastPingTime real, '
                            'heading real, '
                            'pitch real, '
                            'roll real, '
                            'waterTemp real, '
                            'sysTemp real, '
                            'salinity real, '
                            'pressure real, '
                            'xdcrDepth real, '
                            'sos real, '
                            'rawMagFieldStrength real,'
                            'pitchGravityVector real, '
                            'rollGravityVector real, '
                            'verticalGravityVector real);')
        print("Ancillary table created")

        # Bottom Track
        self.cursor.execute('CREATE TABLE IF NOT EXISTS projects (id SERIAL PRIMARY KEY,'
                            'firstPingTime real, '
                            'lastPingTime real, '
                            'heading real, '
                            'pitch real, '
                            'roll real, '
                            'waterTemp real, '
                            'salinity real, '
                            'xdcrDepth real, '
                            'pressure real, '
                            'sos real, '
                            'status integer, '
                            'numBeams integer, '
                            'pingCount integer, '
                            'rangeBeam0 real, '
                            'rangeBeam1 real, '
                            'rangeBeam2 real, '
                            'rangeBeam3 real, '
                            'snrBeam0 real, '
                            'snrBeam1 real, '
                            'snrBeam2 real, '
                            'snrBeam3 real, '
                            'ampBeam0 real, '
                            'ampBeam1 real, '
                            'ampBeam2 real, '
                            'ampBeam3 real, '
                            'corrBeam0 real, '
                            'corrBeam1 real, '
                            'corrBeam2 real, '
                            'corrBeam3 real, '
                            'beamVelBeam0 real, '
                            'beamVelBeam1 real, '
                            'beamVelBeam2 real, '
                            'beamVelBeam3 real, '
                            'beamNumPingsBeam0 integer, '
                            'beamNumPingsBeam1 integer, '
                            'beamNumPingsBeam2 integer, '
                            'beamNumPingsBeam3 integer, '
                            'instrVelBeam0 real, '
                            'instrVelBeam1 real, '
                            'instrVelBeam2 real, '
                            'instrVelBeam3 real, '
                            'Beam3BeamSolBeam0 integer, '
                            'Beam3BeamSolBeam1 integer, '
                            'Beam3BeamSolBeam2 integer, '
                            'Beam3BeamSolBeam3 integer, '
                            'earthVelBeam0 real, '
                            'earthVelBeam1 real, '
                            'earthVelBeam2 real, '
                            'earthVelBeam3 real, '
                            'Earth3BeamSolBeam0 integer, '
                            'Earth3BeamSolBeam1 integer, '
                            'Earth3BeamSolBeam2 integer, '
                            'Earth3BeamSolBeam3 integer, '
                            'snrPulseCoherentBeam0 real, '
                            'snrPulseCoherentBeam1 real, '
                            'snrPusleCoherentBeam2 real, '
                            'snrPulseCoherentBeam3 real, '
                            'ampPulseCoherentBeam0 real, '
                            'ampPulseCoherentBeam1 real, '
                            'ampPulseCoherentBeam2 real, '
                            'ampPulseCoherentBeam3 real, '
                            'velPulseCoherentBeam0 real, '
                            'velPulseCoherentBeam1 real, '
                            'velPulseCoherentBeam2 real, '
                            'velPulseCoherentBeam3 real, '
                            'noisePulseCoherentBeam0 real, '
                            'noisePulseCoherentBeam1 real, '
                            'noisePulseCoherentBeam2 real, '
                            'noisePulseCoherentBeam3 real, '
                            'corrPulseCoherentBeam0 real, '
                            'corrPulseCoherentBeam1 real, '
                            'corrPulseCoherentBeam2 real, '
                            'corrPulseCoherentBeam3 real);')
        print("Bottom Track table created")

        # Beam Velocity
        query = 'CREATE TABLE IF NOT EXISTS beamVelocity (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Beam Velocity table created")

        # Instrument Velocity
        query = 'CREATE TABLE IF NOT EXISTS instrumentVelocity (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Instrument Velocity table created")

        # Earth Velocity
        query = 'CREATE TABLE IF NOT EXISTS earthVelocity (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Earth Velocity table created")

        # Amplitude
        query = 'CREATE TABLE IF NOT EXISTS amplitude (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Amplitude table created")

        # Correlation
        query = 'CREATE TABLE IF NOT EXISTS correlation (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' real, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Correlation table created")

        # Good Beam Ping
        query = 'CREATE TABLE IF NOT EXISTS goodBeamPing (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' integer, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Good Beam Ping table created")

        # Good Earth Ping
        query = 'CREATE TABLE IF NOT EXISTS goodEarthPing (id SERIAL PRIMARY KEY, ensIndex integer NOT NULL, '
        for ensBin in range(0, 200):
            for beam in range(0, 4):
                query += 'Beam' + str(beam) + 'Bin' + str(ensBin) + ' integer, '

        query = query[:-2]          # Remove final comma
        query += ');'
        self.cursor.execute(query)
        print("Good Earth Ping table created")

        # NMEA
        query = ' '
        self.cursor.execute('CREATE TABLE IF NOT EXISTS nmea (id SERIAL PRIMARY KEY, '
                            'ensIndex integer NOT NULL, '
                            'nmea text);')
        print("NMEA table created")

        print("Table Creation Complete")
        self.conn.commit()

if __name__ == "__main__":
    conn_string = "host='192.168.0.143' port='32769' dbname='rti' user='rico' password='123456'"
    sql = rti_sql(conn_string)
    sql.create_tables()
    sql.close()

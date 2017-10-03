from rti_python.Writer.rti_sql import rti_sql

from datetime import datetime


class RtiProjects:
    """
    Handle the projects.
    Create projects and add data to the projects.
    """

    def __init__(self,
                 host='localhost',
                 port=5432,
                 dbname='postgres',
                 user='user',
                 pw='pw'):

        # Construct connection string
        self.sql_conn_string = "host=\'{0}\' port=\'{1}\' dbname=\'{2}\' user=\'{3}\' password=\'{4}\'".format(host, port, dbname, user, pw)

        # Sql connection when doing batch inserts
        self.batch_sql = None
        self.batch_prj_id = 0
        self.batch_count = 0


    def add_prj_sql(self, prj_name):
        """
        Add the given project name to the projects table.
        :param prj_name: Project name
        :return: TRUE = Project added.  FALSE = Project already exists and could not add.
        """
        # Check if the project exist
        project_exist = self.check_project_exist(prj_name)

        if project_exist == 0:
            # Add project to database
            dt = datetime.now()
            sql = rti_sql(self.sql_conn_string)
            sql.insert('INSERT INTO projects (name, created, modified) VALUES (\'{0}\', \'{1}\', \'{2}\');'.format(prj_name, dt, dt))
            return True
        elif project_exist > 0:
            # Send a warning and make them give a new name
            return False

    def check_project_exist(self, prj_name):
        """
        Check if the given project name exist in the projects table.
        :param prj_name: Project Name.
        :return: TRUE = Project exists.
        """
        count = 0

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_string)
        except Exception as e:
            print("Unable to connect to the database")
            return -1

        # Check if the project exists
        try:
            result = sql.query('SELECT 1 FROM projects WHERE name = \'{0}\';'.format(prj_name))

            # Count the results
            for row in result:
                count += 1
                print(row)

            # Check if any results were returned
            print("Count: " + str(count))

        except Exception as e:
            print("Unable to run query", e)
            return -2

        # Close connection
        sql.close()

        return count

    def get_all_projects(self):
        """
        Select all the projects from the database.
        :return: All the databases in the projects table.
        """
        result = None

        # Make connection
        try:
            sql = rti_sql(self.sql_conn_string)
        except Exception as e:
            print("Unable to connect to the database")
            return result

        # Get all projects
        try:
            result = sql.query('SELECT * FROM projects;')
        except Exception as e:
            print("Unable to run query", e)
            return result

        # Close connection
        sql.close()

        return result

    def begin_batch(self, prj_name):
        # Make connection
        try:
            self.batch_sql = rti_sql(self.sql_conn_string)
        except Exception as e:
            print("Unable to connect to the database")

        # Get the index for the given project name
        self.batch_prj_id = self.batch_sql.query('SELECT id FROM projects WHERE name=\'{0}\''.format(prj_name))
        print(self.batch_prj_id)

    def end_batch(self):

        # Commit the batch
        self.batch_sql.commit();

        # Close connection
        self.batch_sql.close()

        # Set the connection to none
        self.batch_sql = None

    def add_ensemble(self, ens):
        if self.batch_sql is not None:
            # Get Date and time for created and modified
            dt = datetime.now()

            # Add line for each dataset type
            ens_ds = "INSERT INTO ensembles (" \
                     "ensnum, " \
                     "numbins, " \
                     "numbeams, " \
                     "desiredpings, " \
                     "actualpings, " \
                     "status, " \
                     "datetime, " \
                     "serialnumber, " \
                     "firmware, " \
                     "subsystemconfig, " \
                     "project_id, " \
                     "created, " \
                     "modified)" \
                     "VALUES( " \
                     "{0}, " \
                     "{1}, " \
                     "{2}, " \
                     "{3}, " \
                     "{4}, " \
                     "{5}, " \
                     "\'{6}\', " \
                     "\'{7}\', " \
                     "\'{8}\', " \
                     "\'{9}\', " \
                     "\'{10}\', " \
                     "\'{11}\', " \
                     "\'{12}\');".format(ens.EnsembleData.EnsembleNumber,
                                         ens.EnsembleData.NumBins,
                                         ens.EnsembleData.NumBeams,
                                         ens.EnsembleData.DesiredPingCount,
                                         ens.EnsembleData.ActualPingCount,
                                         ens.EnsembleData.Status,
                                         ens.EnsembleData.datetime(),
                                         ens.EnsembleData.SerialNumber,
                                         ens.EnsembleData.firmware_str(),
                                         ens.EnsembleData.SysFirmwareSubsystemCode,
                                         self.batch_prj_id[0][0],
                                         dt,
                                         dt)

            ens_id = self.batch_sql.execute(ens_ds)
            print(ens_id)

            # Monitor how many inserts have been done so it does not get too big
            self.batch_count += 1
            if self.batch_count > 10:
                self.batch_sql.commit()
                self.batch_count = 0

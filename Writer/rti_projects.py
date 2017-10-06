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
        print("Project ID: " + str(self.batch_prj_id))

    def end_batch(self):

        # Commit the batch
        self.batch_sql.commit();

        # Close connection
        self.batch_sql.close()

        # Set the connection to none
        self.batch_sql = None

    def add_ensemble(self, ens):
        if self.batch_sql is not None:
            ens_idx = self.add_ensemble_ds(ens)         # Ensemble dataset

            # Correlation
            self.add_dataset("correlation",
                             ens.Correlation.Correlation,
                             ens.Correlation.num_elements,
                             ens.Correlation.element_multiplier,
                             ens_idx)
        else:
            print("Batch import not started.  Please call begin_batch() first.")

    def add_ensemble_ds(self, ens):
        """
        Add the Ensemble dataset to the database.
        """

        # Get Date and time for created and modified
        dt = datetime.now()

        # Add line for each dataset type
        ens_query = "INSERT INTO ensembles (" \
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
                    "VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s) RETURNING ID;"

        self.batch_sql.cursor.execute(ens_query, (ens.EnsembleData.EnsembleNumber,
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
                                                  dt))
        ens_idx = self.batch_sql.cursor.fetchone()[0]
        print("Ens Index: " + str(ens_idx))

        # Monitor how many inserts have been done so it does not get too big
        self.batch_count += 1
        if self.batch_count > 10:
            self.batch_sql.commit()
            self.batch_count = 0

        return ens_idx

    def add_dataset(self, table, data, num_elements, element_multiplier, ens_idx):
        """
        Add a dataset to the database.  Give the table name, data, number of beams and bins and the ensemble index.
        :param table: Table name as a string.
        :param data: 2D Array of the data.
        :param num_elements: Number of bins.
        :param element_multiplier: Number of beams.
        :param ens_idx: Ensemble index in Ensembles table.
        """
        # Get Date and time for created and modified
        dt = datetime.now()

        beam0_avail = False
        beam1_avail = False
        beam2_avail = False
        beam3_avail = False
        query_b0_label = ""
        query_b0_val = ""
        query_b1_label = ""
        query_b1_val = ""
        query_b2_label = ""
        query_b2_val = ""
        query_b3_label = ""
        query_b3_val = ""
        for bin_num in range(num_elements):
            for beam in range(element_multiplier):
                if beam == 0:
                    query_b0_label += "Bin{0}, ".format(bin_num)
                    query_b0_val += "{0}, ".format(data[bin_num][beam])
                    beam0_avail = True
                if beam == 1:
                    query_b1_label += "Bin{0}, ".format(bin_num)
                    query_b1_val += "{0}, ".format(data[bin_num][beam])
                    beam1_avail = True
                if beam == 2:
                    query_b2_label += "Bin{0}, ".format(bin_num)
                    query_b2_val += "{0}, ".format(data[bin_num][beam])
                    beam2_avail = True
                if beam == 3:
                    query_b3_label += "Bin{0}, ".format(bin_num)
                    query_b3_val += "{0}, ".format(data[bin_num][beam])
                    beam3_avail = True

        query_b0_label = query_b0_label[:-2]        # Remove final comma
        query_b0_val = query_b0_val[:-2]            # Remove final comma
        query_b1_label = query_b1_label[:-2]        # Remove final comma
        query_b1_val = query_b0_val[:-2]            # Remove final comma
        query_b2_label = query_b2_label[:-2]        # Remove final comma
        query_b2_val = query_b2_val[:-2]            # Remove final comma
        query_b3_label = query_b3_label[:-2]        # Remove final comma
        query_b3_val = query_b3_val[:-2]            # Remove final comma

        # Add line for each beam
        if beam0_avail:
            query = "INSERT INTO {0} (" \
                    "ensIndex, " \
                    "beam, " \
                    "{1}, " \
                    "created, " \
                    "modified) " \
                     "VALUES ( %s, %s, {2}, %s, %s);".format(table, query_b0_label, query_b0_val)
            self.batch_sql.cursor.execute(query, (ens_idx, 0, dt, dt))

        if beam1_avail:
            query = "INSERT INTO {0} (" \
                    "ensIndex, " \
                    "beam, " \
                    "{1}, " \
                    "created, " \
                    "modified) " \
                     "VALUES ( %s, %s, {2}, %s, %s);".format(table, query_b1_label, query_b1_val)
            self.batch_sql.cursor.execute(query, (ens_idx, 1, dt, dt))

        if beam2_avail:
            query = "INSERT INTO {0} (" \
                    "ensIndex, " \
                    "beam, " \
                    "{1}, " \
                    "created, " \
                    "modified) " \
                     "VALUES ( %s, %s, {2}, %s, %s);".format(table, query_b2_label, query_b2_val)
            self.batch_sql.cursor.execute(query, (ens_idx, 2, dt, dt))

        if beam3_avail:
            query = "INSERT INTO {0} (" \
                    "ensIndex, " \
                    "beam, " \
                    "{1}, " \
                    "created, " \
                    "modified) " \
                     "VALUES ( %s, %s, {2}, %s, %s);".format(table, query_b3_label, query_b3_val)
            self.batch_sql.cursor.execute(query, (ens_idx, 3, dt, dt))

        # Monitor how many inserts have been done so it does not get too big
        self.batch_count += 1
        if self.batch_count > 10:
            self.batch_sql.commit()
            self.batch_count = 0
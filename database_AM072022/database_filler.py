import mysql.connector


def cleaner(connectionVar):
    """
    This function can be used to completely empty the database.
    Mainly used in testing
    Args:
        connectionVar: The connection to the database from where cursors can be called.

    Returns:

    """
    cursor = connectionVar.cursor()
    cursor.execute('delete from ge_at')
    cursor.execute('delete from fa_ge')
    cursor.execute('delete from family')
    cursor.execute('delete from gene')
    cursor.execute('delete from attributes')
    print("Emptied database")



def control_database(geneData, annotationData):
    """
    This is the main function that is called from other scripts to start filling the database.
    Here the database filler functions are called in the right order and status updates are printed to the console.
    Args:
        geneData: A list of gene objects
        annotationData: A list of attribute objects

    Returns:

    """
    connectionVar = connection()



    famList = []
    for gene in geneData:

        for family in gene.family:
            if family == '':
                family = 'no family found'
            if family not in famList:
                famList.append(family)

    clean = 0

    if clean == 1:
        cleaner(connectionVar)
    else:
        fill_database_family(connectionVar, famList)
        print('family table filled')

        fill_database_gene(connectionVar, geneData)
        print('Gene table filled')

        fill_database_attributes(connectionVar, annotationData)
        print('Attribute table filled')

        fill_database_gen_fam(connectionVar, geneData)
        print('Gene-family connection made')

        fill_database_gen_att(connectionVar, geneData)
        print('Gene-attribute connection made')

    connectionVar.commit()


def connection():
    """
    Here the connection is established to the database.
    Returns: The connection to the database from where cursors can be called.

    """
    connection = mysql.connector.connect(host='localhost',
                                         database='GECKO',
                                         user='gecko',
                                         password='gecko',
                                         auth_plugin='mysql_native_password')

    return connection


def fill_database_family(connectionVar, famList):
    """
    This functions fills the family table of the database.
    If there is already data in the tables this data is requested and the new data will be added on top of that.
    Args:
        connectionVar: The connection to the database from where cursors can be called.
        famList: A list of all unique families present in the gene objects.

    Returns:

    """

    cursor = connectionVar.cursor()
    cursor.execute("select f_id from family")
    myresult = cursor.fetchall()

    varID = 0
    for x in myresult:
        if int(x[0]) > varID:
            varID = int(x[0])
    if varID != 0:
        varID += 1


    cursor.execute("select symbol from family")

    myresult = [item[0] for item in cursor.fetchall()]

    for fam in famList:
        if fam not in myresult:


            sql = "INSERT INTO family (f_id, symbol) VALUES (%s, %s)"
            val = (varID, fam)
            cursor.execute(sql, val)
            varID += 1



def fill_database_gene(connectionVar, geneData):
    """
    This functions fills the gene table of the database.
    If there is already data in the table this data is requested and the new data will be added on top.
    Args:
        connectionVar: The connection to the database from where cursors can be called.
        geneData: A list of gene objects

    Returns:

    """

    cursor = connectionVar.cursor()

    cursor.execute("select f_id from gene")
    myresult = cursor.fetchall()
    famID = 0
    for x in myresult:
        if int(x[0]) > famID:
            famID = int(x[0])
    if famID != 0:
        famID += 1


    cursor.execute("select case_id from gene")
    myresult = cursor.fetchall()
    caseID = 0

    for x in myresult:
        if int(x[0]) > caseID:
            caseID = int(x[0])
    if caseID != 0:
        caseID += 1


    cursor.execute("select g_id from gene")

    myresult = [item[0] for item in cursor.fetchall()]


    for gene in geneData:
        if gene.name not in myresult:
            sql = "INSERT INTO gene (g_id, f_id, case_id) VALUES (%s, %s, %s)"
            val = (gene.name, famID, caseID)
            cursor.execute(sql, val)

            caseID += 1
            famID += 1



def fill_database_attributes(connectionVar, annotationData):
    """
    This functions fills the attribute table of the database.
    If there is already data in the table this data is requested and the new data will be added on top.
    Args:
        connectionVar: The connection to the database from where cursors can be called.
        annotationData: A list of annotation objects

    Returns:

    """

    cursor = connectionVar.cursor()

    cursor.execute("SELECT case_id FROM attributes")


    results = [item[0] for item in cursor.fetchall()]


    for annotationObject in annotationData:

        if annotationObject.file_id not in results:

            if annotationObject.exposures_years_smoked == '':
                year_smoked = 0
            else:
                year_smoked = annotationObject.exposures_years_smoked
            sql = "INSERT INTO attributes (case_id, gender, race, organ, cancer, disease_type, days_old_at_diagnosis, years_smoked, cigarettes_per_day) VALUES (%s, %s, %s, %s,%s, %s, %s, %s,%s)"
            val = (annotationObject.file_id, annotationObject.gender, annotationObject.race, annotationObject.organ, annotationObject.cancer_status,
                   annotationObject.disease_type, annotationObject.days_old_at_diagnosis,
                   year_smoked, annotationObject.exposures_cigarettes_per_day)
            cursor.execute(sql, val)



def fill_database_gen_fam(connectionVar, geneData):
    """
    This function fills the M to M relations between the genes and families.
    This M to M relation is established in the fa_ge table which connects the two id's
    By retrieving the data in the tables and cross referencing the objects the connections between id's are established.
    Args:
        connectionVar: The connection to the database from where cursors can be called.
        geneData: A list of gene objects.

    Returns:

    """
    cursor = connectionVar.cursor()


    cursor.execute("select f_id, symbol from family")
    myresultFam = [[item[0], item[1]] for item in cursor.fetchall()]

    cursor.execute("select g_id, f_id from gene")
    myresultGene = [[item[0], item[1]] for item in cursor.fetchall()]



    for gene in geneData:
        for genedb in myresultGene:
            try:
                if gene.name == genedb[0]:
                    for geneFam in gene.family:
                        for fams in myresultFam:
                            if geneFam in fams:
                                sql = "INSERT INTO fa_ge (family_f_id, gene_f_id) VALUES (%s, %s)"
                                val = (fams[0],genedb[1])
                                cursor.execute(sql, val)
            except Exception as e:
                pass



def fill_database_gen_att(connectionVar, geneData):
    """
    This function fills the M to M relations between the genes and attributes.
    This M to M relation is established in the ge_at table which connects the two id's
    By retrieving the data in the tables and cross referencing the objects the connections between id's are established.
    Args:
        connectionVar: The connection to the database from where cursors can be called.
        geneData: A list of gene objects.

    Returns:

    """

    cursor = connectionVar.cursor()

    cursor.execute("select g_id, case_id from gene")

    myresult = [[item[0],item[1]] for item in cursor.fetchall()]


    for gene in geneData:


        for case in gene.counts:

            try:
                for item in myresult:
                    if gene.name in item:

                        sql = "INSERT INTO ge_at (gene_case_id, attributes_case_id,read_count) VALUES (%s, %s,%s)"
                        val = (item[1], case, gene.counts[case])
                        cursor.execute(sql, val)

            except Exception as e:
                pass



if __name__ == '__main__':
    connectionVar = connection()

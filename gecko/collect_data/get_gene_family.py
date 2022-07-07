import sys
from zeep import Client
from zeep.cache import SqliteCache
from zeep.transports import Transport

sys.path.append('../')


def main():
    input_ids = 'ENSG00000000003,ENSG00000000005,ENSG00000000419,ENSG00000000457,ENSG00000000460,ENSG00000000938,ENSG00000000971,ENSG00000001036,ENSG00000001084,ENSG00000001167,ENSG00000001460,ENSG00000001461,ENSG00000001497,ENSG00000001561,ENSG00000001617,ENSG00000001626,ENSG00000001629'
    id_type = 'ENSEMBL_GENE_ID'
    client = client_connection()
    client = add_query_list(client, input_ids, id_type)
    client, categories = add_category(client)
    table_report = query_david(client)
    create_fam_dict(categories, table_report)


def client_connection():
    """
    The function client_connection connects to the David API.
    :return: client: The client connected to the David API.
    """
    url = 'https://david.ncifcrf.gov/webservice/services/DAVIDWebService?wsdl'
    transport = Transport(cache=SqliteCache())
    client = Client(url, transport=transport)
    # authenticate user email
    client.service.authenticate('b.vanwessel@student.han.nl')
    return client


def add_query_list(client, input_ids, id_type):
    """
    The function add_query_list ads all parameters to the client.
    :param client: The client connected to the David API.
    :param input_ids: A string containing all input_IDs.
    :param id_type: A string containing the input ID type.
    :return: client: The client connected to the David API.
    """
    list_name = 'make_up'
    list_type = 0
    client.service.addList(input_ids, id_type, list_name, list_type)
    return client


def add_category(client):
    """
    The function add_category ads the output details to the client.
    :param client: The client connected to the David API.
    :return: client: The client connected to the David API.
    categories: A string containing the output categories.
    """
    category_string = str(client.service.setCategories(
        'INTERPRO'))
    categories = category_string.split(',')
    return client, categories


def query_david(client):
    """
    The function query_david queries the David API.
    :param client: The client connected to the David API.
    :return: table_report: The results fom the David API query.
    """
    table_report = client.service.getTableReport()

    return table_report


def create_fam_dict(categories, table_report):
    """
    The function create_fam_dict converts the resulta of the David query to a family dictionary
    :param categories: A string containing the output categories.
    :param table_report: The results fom the David API query.
    :return:
    """
    fam_dict = {}
    for table_record in table_report:
        for arrayString in table_record.values:
            gene_id = ','.join(x for x in arrayString.array)
        for annotation_record in table_record.annotationRecords:
            default_value = ''
            category_dict = dict.fromkeys(categories, default_value)
            terms_concat = '';
            for term in annotation_record.terms:
                term_string = term.split("$")[1]
                term_list = [term_string, terms_concat]
                terms_concat = ','.join(term_list)
            category_dict[str(annotation_record.category)] = terms_concat;
            fam_dict[gene_id] = terms_concat.split(",")
    return fam_dict


def add_gene_familiy(fam_dict, my_genes):
    """
    The function add_gene_family adds the retrieved gene_families to the gene Objects.
    :param fam_dict: A dictionary containing all gene families for the genes.
    :param my_genes: A list containing gene Objects without family.
    :return: my_genes A list containing gene Objects wih the added family
    """
    for i in range(len(my_genes)):
        try:
            gene_name = str(my_genes[i].name).split(".")
            family = fam_dict[gene_name[0]]
            family = family[:len(family) - 1]
            my_genes[i].family = family
            del fam_dict[gene_name[0]]
        except KeyError:
            print("no family")
    return my_genes


if __name__ == '__main__':
    main()

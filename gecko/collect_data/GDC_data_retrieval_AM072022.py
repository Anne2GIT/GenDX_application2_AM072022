from gecko.collect_data import data_retrival, retrieve_counts, create_gene, annotation_data, get_gene_family
from gecko.database.database_filler import control_database
from gecko.database.pickler import database_filler
import gc
import time

gene_family_dictionary = {}


def main():
    """
    The main function calls all needed functions for the Gecko tool to work.
    :return: -
    """
    query_information = [[{"op": "in"}, {"field": "cases.primary_site"}, {"value": ["kidney"]}],
                         [{"op": "in"}, {"field": "files.analysis.workflow_type"}, {"value": ["HTSeq - Counts"]}],
                         [{"op": "in"}, {"field": "cases.project.program.name"}, {"value": ["TCGA"]}],
			             [{"op": "in"}, {"field": "cases.samples.sample_type_id"}, {"value": ["01"]}]]
    file_ids = get_file_ids(query_information)
    map_loc = retrieve_count_data(file_ids[:2])
    gene_list = read_count_data(map_loc)
    file_annotation_objects_list = retrieve_file_annotation(file_ids[:2])
    fam_dict = get_gene_families(gene_list)
    my_genes = get_gene_family.add_gene_familiy(gene_family_dictionary, gene_list)
    database_filler(my_genes,file_annotation_objects_list)
    #control_database(my_genes,file_annotation_objects_list)

def get_file_ids(query_information):
    """
    The function get_file_ids calls all functions needed to retrieve file_ids based on a query.
    :param query_information: The query used to search the GDC Data Portal.
    :return: file_ids: A list containing all found file_ids.
    """
    filters = data_retrival.create_gdc_query(query_information)
    file_ids = data_retrival.retrieve_file_ids(filters)
    return file_ids


def retrieve_count_data(file_ids):
    """
    The function retrieve_count_data calls all function needed to download the files containing the read count data.
    :param file_ids: A list containing all found file_ids.
    :return: map_loc: A string containing the location of the created folder.
    """
    map_loc = retrieve_counts.create_directory()
    retrieve_counts.create_filter(file_ids)
    retrieve_counts.merge_files(map_loc)
    retrieve_counts.normalize_data(map_loc)
    return map_loc


def read_count_data(map_loc):
    """
    The function read_count_data calls all functions needed to extract the read count data for all found fies
    :param map_loc: A string containing the location of the created folder.
    :return: gene_list: A list containing all created Gene objects.
    """
    file_information_list = create_gene.open_file(map_loc)
    gene_list = create_gene.create_dict(file_information_list)
    return gene_list


def retrieve_file_annotation(file_ids):
    """
    The function retrieve_file_annotation calls all the functions needed to retrieve the annotation data for all files.
    :param file_ids: A list containing all found file_ids.
    :return:
    """
    file_annotation_objects_list = []
    file_annotation_objects_list = annotation_data.get_file_objects(file_ids, file_annotation_objects_list)
    return file_annotation_objects_list


def get_gene_families(gene_list):
    """
    The get_gene_families function gets the family for all given genes.
    :param gene_list: A list containing all gene ids used to perform the family search.
    :return: fam_dict: A dictionary containing all gene families for the genes.
    """
    id_type = 'ENSEMBL_GENE_ID'
    input_ids = ""
    if len(gene_list) <= 499:
        for i in range(len(gene_list)):
            gene_id = str(gene_list[i].name)
            gene_id = gene_id.split(".")
            input_ids = input_ids + gene_id[0] + ","
        client = get_gene_family.client_connection()
        client = get_gene_family.add_query_list(client, input_ids, id_type)
        client, categories = get_gene_family.add_category(client)
        table_report = get_gene_family.query_david(client)
        fam_dict = get_gene_family.create_fam_dict(categories, table_report)
        gene_family_dictionary.update(fam_dict)
        gc.collect()
        time.sleep(10)
        return fam_dict
    else:
        for i in range(len(gene_list[:499])):
            gene_id = str(gene_list[i].name)
            gene_id = gene_id.split(".")
            input_ids = input_ids + gene_id[0] + ","
        client = get_gene_family.client_connection()
        client = get_gene_family.add_query_list(client, input_ids, id_type)
        client, categories = get_gene_family.add_category(client)
        table_report = get_gene_family.query_david(client)
        fam_dict = get_gene_family.create_fam_dict(categories, table_report)
        gene_family_dictionary.update(fam_dict)
        gc.collect()
        time.sleep(10)
        return get_gene_families(gene_list[499:])


if __name__ == "__main__":
    main()

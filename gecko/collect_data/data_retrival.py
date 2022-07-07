import requests
import json


def main():
    query_information = [[{"op": "in"}, {"field": "cases.project.primary_site"}, {"value": ["bronchus and lung"]}],
                        [{"op": "in"}, {"field": "cases.demographic.race"}, {"value": ["white"]}],
                        [{"op": "in"}, {"field": "cases.demographic.gender"}, {"value": ["female"]}],
                        [{"op": "in"}, {"field": "files.analysis.workflow_type"}, {"value": ["HTSeq - Counts"]}]]
    filters = create_gdc_query(query_information)
    file_ids = retrieve_file_ids(filters)


def create_gdc_query(query_information):
    """
    The function create_gdc_query builds a query which can be used to retrieve data from the GDC Data Portal.
    :param query_information: A 2D list containing all needed data to create a query.
    :return: filters: A dictionary which contains all filter options needed to query the GDC Data Portal.
    """
    filters = {"op": "and"}
    content = []
    for i in range(len(query_information)):
        sub_content = {"op": query_information[i][0]["op"]}
        content_dic = {"field": query_information[i][1]["field"], "value": query_information[i][2]["value"]}
        sub_content["content"] = content_dic
        content.append(sub_content)
    filters["content"] = content

    return filters


def retrieve_file_ids(filters):
    """
    The function retrieve_file_ids uses the GDC Data Portal API to retrieve file ID`s based on a dictionary that contains filter options.
    :param filters: A dictionary which contains all filter options needed to query the GDC Data Portal.
    :return: file_uuid_list: This is a list containing all found file ids.
    """
    files_endpt = "https://api.gdc.cancer.gov/files"

    params = {
        "filters": json.dumps(filters),
        "fields": "file_id",
        "format": "JSON",
        "size": "10000"
    }

    response = requests.get(files_endpt, params=params)
    file_uuid_list = []

    for file_entry in json.loads(response.content.decode("utf-8"))["data"]["hits"]:
        file_uuid_list.append(file_entry["file_id"])

    return file_uuid_list


if __name__ == "__main__":
    main()

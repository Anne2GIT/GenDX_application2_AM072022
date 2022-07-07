import requests
import json
from gecko.objects import Attributes
import sys
sys.setrecursionlimit(1500)


def main():
    file_ids = ['26311e43-dfa3-4b45-b337-58cbe08e484f', '6bf5b079-6d78-4ef5-b225-3f5493a751f4', 'b701206a-db47-4c5f-9825-8eebc831d1bc', '810bed03-efda-43e9-954b-e78fc995c7c8', '55a58234-84d1-4fd1-b314-f9301ae92f34', '9b52a4c6-787a-43b4-8528-6ba084d693a4', '621e56b2-5669-4dbd-b6df-b0d40c994a7d', '4ff04c8c-70f8-4c08-b4df-1136d70ea9a7', 'ea856e23-c5d3-4018-b98e-e2f4c63ae20c', 'db7a4663-336c-4ebc-976f-193f473b2345', 'a4a631a6-a070-4909-9141-5d07242be579', '6b7f79c9-49a1-427a-9676-5833dd7da5fe', '3ef7a112-d7ff-4a25-bcbd-e4b1e014fe7f', '5367a7b6-a035-4aa8-89b9-2f89e758db62', '418aed95-d68d-446d-96dc-4507f3019476', 'fa339c22-6051-43db-8d29-3531548219f2', 'f954273d-bd3d-47a6-954d-f97d56075456', '8055fabe-15b6-4570-bb04-23c52641620c', '8b06e5a0-0668-41b1-b59f-9a70096c3b26', '329c3d83-f0d4-4861-8297-a405777ad46a', 'c1a5323b-bad7-4648-9f74-eb1f70688b9d', 'a3a1ed5f-a1f3-421d-ae14-7ecee6459005', '43ed092c-c187-410f-a404-12bea37963a0', '99b575f0-1bb4-4d3f-b57a-35c3dc9327d9', '6ac2b7be-d036-463b-ad46-bcb7def853b3', '2c1dbf50-b807-4c46-97a0-42b94bb281cc', '0aaf1076-c99d-408e-9220-dc307355b84e', '5ad39d12-4f87-49ab-92c0-85cfc7da246c', '1b0a6b8f-a8cf-4cbf-bf14-a8be40edeead', 'a4e7b008-2754-4be0-8f0e-896d7ee109bf', 'bc8aaae1-01b7-4d85-9b52-b8f3f60db585', 'e2432639-67f7-47dc-92b1-9b5cde4c9d8e', 'c8b8a3dd-19fb-4d3f-a4e9-440b4063b7b8', '7c177286-9bd7-4be0-a2f4-0d635cb94d25', '46d36497-a4dc-49fa-affc-d29d0cca19fa', '6c035588-d267-4b39-9ef4-9c82d0bd567c', '12dc3992-3bda-41eb-9a83-fbca93d2a942', 'b6a2d572-5c02-4630-bf1d-d03cd8297b1b', '7397d6c5-f5f0-4d85-8f49-9d5924b8be57', '01849baf-6dfb-4dd6-a207-d29e2bcc95d9', 'f7c619ac-9de0-4539-80e7-b96592820646', '1b0388e3-721c-4343-9ab2-01ebacd2aeb3', '7783e608-5038-4abc-9285-9e6c58ca7ac1', 'd4314b32-4b91-4096-b18e-6c81a12c47b0', '73185268-f259-4b40-af7f-1dad2d6be903', 'f3882448-3074-4c36-acef-c6fe8b704b7e', '6909d3fd-d0cc-4139-b60b-d98751b5db00', 'd428b125-149d-44fc-b3ac-513a3e0a2a66', 'a53757ce-a89e-47a3-bd07-0c996f323499', '9a338f89-eb1c-455f-a944-cda79b8e7e8b', '73470df6-d598-4aa1-84af-9c6c39b71ca0', 'd32dd60e-c7b5-43a7-b2f6-95b88c9f87d0', '88bb8d3e-3106-49a8-922c-13d76210e8ac', '6aa2289e-4ce3-4910-8242-08ab893e1071', 'c055a6aa-f0f9-4e6e-8733-ecdd0c533a4e', 'c6e40493-5c3b-4b90-aab2-a3c3b2621a01', 'c711a913-5832-4a37-acb9-34da85f423b6', '23d4aec2-22b0-466f-839b-f16ab75318a7', 'ce638577-b7a3-4a76-b53e-50ebb21df1d7', 'a5544997-2e93-485e-ab05-4f14d66c6cc7', '60085406-f584-4fc1-ae34-c1f7ee8da405', '4bc9feca-bb58-4812-bddb-fd7f008a8d7a', '60729d78-c5c4-464c-8927-ecde0083af08', '6a402ef0-8b06-48ac-8a49-25b769f3e391', '995cb4bc-6d01-4091-ad04-e6f27544db48', '35185968-737b-4f0a-8923-33b3a6ab0dd2', '948a5ea0-8857-448c-89b0-0928424f9316', 'e386e8db-6b78-41c5-b569-fe6540fc0ef8', '718e1732-8a97-4a8a-8628-790c2d811cb8', '235a7a04-95a0-4a14-8c9a-f9eb8a0162d4', '10b6df33-8f32-4ed9-b1b1-8867be485a2f', '185b51b4-0654-457f-ab20-002c853712d7', '74fea061-7241-4552-a71c-61b70dc87a26', 'c10a99e6-de63-4b38-bbe1-7ce948bbbf40', 'dbabbc65-8e90-495a-98c6-7fc1e28e7f25', '1aafde58-9b8e-4fa6-9acb-8b6090cf06db', '40b238c9-c579-4477-ba7d-e5b143d1cfcb', '8037aad2-b632-430b-a12f-77248b3cabd0', 'acd984e5-23a5-4d14-a5e7-6febf735a386', '61964dcc-f351-4ba2-a51d-e779e88537c1', '84053350-b3a9-4d6c-9f20-46f7f7afd124', 'b2cc40b1-f3d9-4cfc-9c36-59a9510bf12f', '9ec4ae85-38f6-423e-bff9-1ccffaa59a17', 'd67ac0ab-fdb0-4c4f-b7cd-798805a95775', '2ea13f7c-8b0d-43d5-90d7-211f39911e4d', '2c141f07-b3fd-401c-a3e5-05e2326c662d', 'ade5b83e-0d5e-4129-8ad0-d473f02bb7b3', '6e502953-e211-4408-8d1f-ace3347a8915', 'f5d59da9-502d-4694-8a9a-460250a9765f', 'b922c9fe-8213-4ff5-b2fc-b0e0f7e40273', '774c053a-4816-4518-ab9c-312319b03e07', '121332a0-1a55-4d4f-b782-08e9d929f5c0', '70d623eb-dabf-40e1-8ca4-47dd171796c7', 'be0ae0e8-038a-4287-8700-268f286ee2e8', '4e58016e-6a67-49a7-bd58-353a4dd71f9c', 'b4f0819f-c29c-4ac8-a46d-917b0530fcd6', 'eff6361c-64b0-4aa8-ad10-184cea7edddd', '221e1149-f245-4f0a-92f4-d6031a290511', '7d9f1ff0-b118-4a7b-9c92-8622f1edfe70', '3016ea90-7bcb-40e7-b0a8-33ee114565dc', '7993a704-3e7e-49e8-9172-ca302704ecd9', '3424905f-56d9-4134-b03d-1134697c3358', 'a47ca7db-8f7a-470d-b14e-9ba2589860bb', '5b0b6d34-d692-4fcd-89b7-45e1ee37c35d', 'cbbd3beb-1cb3-40cc-8d98-733904f5c8d1', '51de2f4f-a833-4db7-983f-5ee56d670c98', 'a6250de7-ab33-446f-bc17-6e70c5b8e4b5', '15ca6bac-19f2-4a56-a803-0b1d05b8ae47', 'f2913baa-ed39-4fcf-be2e-2efc77afbcb5', '80ba4b54-b984-4006-94dc-47990e1ea853', '03418695-e200-4957-9453-e34acffe3c67', '3c4e84b9-1043-40ef-8988-73fd8d64f747', '5d581b48-477b-488c-800c-3e7c2a2c7998', 'a55f34f6-cd4c-4d45-9573-66165f4c2625', 'd92deacb-ae99-4b7f-9f21-2c9a95b64bbe', '062b40e1-2f4e-466d-a85c-d5c721bec650', '04c48702-a9ec-4c1e-99ba-805adc04c93b', '3c3716a7-d1f4-4f5a-8d18-a72cb31e333e', '08424086-937f-4204-8499-b50561544354', '80023575-bdfd-49d5-bafc-662fb0beb899', '382cbf8f-9811-49f4-acc1-a7b79d302be3', '5d7d0a64-7411-4bf3-bb9f-716a8fdd3843', '096e538f-8902-4343-b78f-16b4d737e89c', '2c229251-a725-47e3-9d11-31a99d46ac58', '8e2d8847-5f3c-4a48-ac5e-0b16ae848e9c', '34a53742-0155-4fca-81ea-eb7be7113533', 'c96f01b7-ac5b-4128-8fd0-73a52e362d3d', 'c62d4332-833d-4125-a47a-554398017985', 'bca93e0a-49d4-482b-a9be-c98a128746ec', 'c72f59d2-355a-41bb-8c72-ad024af1090e', 'afc92e92-ce10-4381-be0c-ab22822ca960', 'e799ab87-6ec2-410c-9921-a97d8a87ab4a', '7e6e15ca-7a3d-4729-ac48-2de7a34a9e29', 'c69e8fb8-7263-4aa8-a1bb-ebb2118832ee', 'f51aceb7-dddf-4529-bb65-41cc81fda873', 'b14ba6be-58e6-4e1d-bd1c-f1916e346491', '6af47543-4d7a-4e1b-9803-eae5195f74d1', '24988998-9ffa-43d5-8cc1-b27e52307367', 'a0212121-5a04-4015-b02a-2e9f9c2d70b4', 'a8cd5a5b-f6b6-40aa-8f7b-8e9bd5e80e79', '3ed081fc-3069-4996-b48d-b50c1f60fc90', '47043dc2-b3a6-46cd-a4a8-9360951d60c9', '0d8e0de7-ddfa-42eb-9ddf-a369540c39ed', 'a347bee8-651f-4c8a-9e57-f21fcf955a1d', 'cb3c15e8-45b6-48a5-b106-baad530e8ca3', '752bf6b9-a679-4946-b390-b8760e121cb0', 'f51dba5b-7fb2-493a-a7ee-ae4f2944ebf0', 'c270acf4-c437-4759-8e29-b5b8e1b2560d', 'cc1c854d-6ef6-443c-b6c4-70f32f6cb5c0', '548d59c0-8f7d-417f-a463-e9acb03dc03e', 'f66788fa-58c5-461e-aad7-2fb4023f6660', '2c703ece-198f-4aae-9a7b-398c9d50bfaa', '98a3035b-0bf6-4c50-b184-5becfef43fff', 'ca81360b-e708-4e20-b5de-660002b57f17', 'ee500acc-7143-4783-a6dd-f1f7c70e6503', '47e6f6f4-cc9a-48ef-aa00-a2662311c227', '6e3ddfdd-f48a-4c2e-be94-d03466d254e1', '5cc494b1-85fa-4415-943c-1cf31a27242a', '142bf27f-0ac8-48d3-a49d-a9ee1098bd70', 'cd7bac40-d763-4f9d-a3c7-e54f70a7ad6f', 'fd5e3e35-4836-4a86-8ff1-94fb18f3872f', 'f532dd00-5231-49c9-853e-e2454cad551b', '081db6db-7768-4fc6-bbe8-0e9a783345ce', 'fde5a0b0-8d5d-4468-bf31-89429c9d7837', '4fa12a4a-9762-4a3d-88bb-aaa5a458918f', '79b293b2-1e88-4e63-bbd9-70c9ec743c82', 'c2c32082-dfd7-44a8-a2bb-5fc60f19a987', '46c48d64-a69e-4f91-a472-f836b815595a', 'f453a024-4495-468f-8a9c-75b1d8dc3252', '8cf46a69-cf97-4522-ae7e-62acf5ece268', '359c109d-dff3-4041-9fc8-aeaac7211e4e', '6aa29eba-181e-4d87-869b-86eab58cfcb7', '1b119ce9-e81f-4363-be43-8167f0c2b0d2', 'fa6a3fc2-264b-412c-9b13-799da5f26959', '59122622-f44f-4b02-ba1a-6848eff4b49c', 'ad720e79-5111-418b-b440-991fe6354f72', 'a29eb812-2356-42bf-8b63-149cd53d9fbe', '45166aa2-8d3d-4741-9278-adc5121ad007', '87baca8b-3846-4eca-ad32-e199de691948', 'a1ccb7e6-c058-481c-afe1-f3bb1dfc0451', '6326b40e-b4c6-4a3d-bfc7-3f916041377f', '6a414a58-e327-4c35-b308-8ec872da466c', '139c706f-d38b-4eba-bed9-703f0d0dfb8f', '8c1bbdba-cac0-4e70-939e-1bf6c5bca84b', '2612d0ee-ec8d-4f8c-badd-4f60e461a21a', 'c9d894a6-ac12-4826-8efa-628bf586329b', '8e27a9f9-435f-40ba-ba6c-0ae9088cabdc', '06fee850-0942-4ec7-ba22-4ed4717ea64f', '765c6cf7-e20e-4d95-af68-420074498688', '7a77d162-3919-4843-bcc0-5c0331ad3ba0', '27c5c74d-b121-49af-abab-76bbdbc9e68b', '9c802e41-322b-4218-ab68-220a80770e72', '35e0675a-ebf7-4bfb-b93a-b604a9e1e46a', '9667a488-9256-4e5d-adab-e987ebe59dab', 'c79ecd42-1bf6-48d6-9aaf-b7cf24945976', '4ba51854-5c0b-45d1-a4e8-e0c6474b852f', 'a3109a89-0537-493d-a1ca-5f07b4845f6c', '64585107-b3ab-4820-a834-c183f422a023', '3230248f-210e-44ba-b550-a7998a8bcdd2', '596718cf-a59b-4497-ad1e-69bca6a37ab2', 'e581161e-59e6-4fd2-8c3a-6109dec2316c', 'a938ba89-101e-4aac-aa9c-73b03ca36471', '57225a4f-6c03-453e-893d-1998267f0bf1', '398d54c5-0031-4aae-8d1f-4e0e6243bc78', '82749d9e-a37a-4def-8138-1cf1211e2670', '7c4228d5-3df5-4b34-a2e8-9dbe72d228eb', '73313c2d-e900-4e2b-acd3-c055abd0ef87', 'c5b283b8-a6ab-4652-b824-18fe1cebe0e3', 'da368838-dad0-434d-a2a8-084b362e358e', 'be46ee72-8958-483f-bd54-38d21ebf7ff6', '228836d1-518a-464c-8475-e3df86194d15', 'bfe0df9c-3c61-41c9-84ae-e70bb56bf5b0', '9f2a81a3-b9ad-4eb2-bf7a-563931efef87', 'eba13e76-96e4-41fb-9342-794110f1037e', 'aedc0968-a84e-4636-ba71-37d48e5667e7', 'd54bd3b4-1e83-4869-8b9c-76f367696f21', 'b8043952-b9fa-4e4e-9bb6-0af5a6110f48', 'f5e52f6b-4524-48a5-bb9b-607a89c45c2b', '43203c2b-8166-40e2-a7c4-f40d8376305b', '63a5a4fc-74d4-4374-af65-7d76f0c161ac', '0e26b724-db35-42ad-80fc-fed30ebedd31', '45255727-d2ee-4431-81f3-115ba9284bd6', '0296c64a-a8af-4945-8463-800642a0ec55', '9c78ad88-2f98-4b97-a17e-054b1b7f86e0', '04cf9ab8-5822-4241-aefc-d7f0e69329fc', 'ab99271a-8aa7-4416-8254-b841ad350140', 'e0c4055d-a5bc-4462-9f16-72454e02c4eb', 'd33ac91c-0cd1-4721-9b27-02cd7561c128', 'fffe4058-dcbe-4c55-8b69-0eee31ad427a', '75bad590-ce4c-49eb-bd6d-b3bda056a4e5', '9f2b3dd4-4f60-4c52-af87-0780dabbb849', '2094a275-62cb-4972-bed0-1b333e96b250', 'bce3c61b-50ef-4d45-b606-c7ffe4eaef05']
    file_objects_list = []
    file_objects_list = get_file_objects(file_ids,file_objects_list)


def get_file_objects(file_ids, file_objects_list):
    """
    The function get_file_objects uses recursion tot find file information and create objects for all file_ids.
    Some file_ids do not have any information so these will be deleted.
    :param file_ids: A list containing all GDC file _ids belonging to a specific search.
    :param file_objects_list: A list containing all Attributes objects you want to ust as starting point.
    :return: file_objects_list: A list containing all Attributes created based on the file information.
    """
    if len(file_ids) == 1:
        params = set_annotation_query(file_ids[:1])
        response = get_annotation_information(params)
        file_information = read_annotation_data(response)
        file_objects_list = create_objects(file_information, file_objects_list,file_ids[:1])
        return file_objects_list
    else:
        params = set_annotation_query(file_ids[:1])
        response = get_annotation_information(params)
        file_information = read_annotation_data(response)
        file_objects_list = create_objects(file_information, file_objects_list,file_ids[:1])
        return get_file_objects(file_ids[1:], file_objects_list)


def set_annotation_query(file_ids):
    """
    The function set_annotation_query gets file information from the GDC Data Portal API using the file_ids.
    :param file_ids: A list containing all GDC file _ids belonging to a specific search.
    :return: params: A dictionary containing all the needed parameters information to perform a search to the GDC Data Portal.
    """
    fields = [
        "exposures.cigarettes_per_day",
        "primary_site",
        "disease_type",
        "diagnoses.age_at_diagnosis",
        "demographic.gender",
        "exposures.years_smoked",
        "demographic.race",
        "sample_type"
    ]

    fields = ",".join(fields)

    filters = {
        "op": "and",
        "content": [
            {
                "op": "in",
                "content": {
                    "field": "files.file_id",
                    "value": file_ids
                }
            }
        ]
    }

    params = {
        "filters": json.dumps(filters),
        "fields": fields,
        "format": "TSV",
        "size": "10000"
    }
    return params


def get_annotation_information(params):
    """
    The function get_annotation_information performs a request to the GDC Data Portal API using the given parameters.
    :param params: A dictionary containing all the needed parameters information to perform a search to the GDC Data Portal.
    :return: response: A response from the GDC DATA Portal API.
    """
    cases_endpt = "https://api.gdc.cancer.gov/cases"
    response = requests.get(cases_endpt, params=params)
    return response


def read_annotation_data(response):
    """
    The function read_annotation_data converts the GDC DATA Portal API response to a list.
    :param response: A response from the GDC DATA Portal API.
    :return: file_information: A list containing the information for file_ids.
    """
    file_information = []
    response = response.content.decode()
    sub_response = response.split("\n")
    for line in sub_response:
        line = line.rstrip()
        sub_line = line.split("\t")
        if len(sub_line) > 1:
            file_information.append(sub_line)
    return file_information


def create_objects(file_information, file_objects_list,file_ids):
    """
    The function create_objects creates an attribute object for found file information.
    :param file_information: A list containing the information for all file_ids.
    :param file_objects_list: A list containing Attributes objects that are already created.
    :param file_ids: A list containing the file_ids used for the search
    :return: file_objects_list A list containing all Attributes created based on the file information.
    """

    for i in range(len(file_information)):
        if i > 0:
            days_old_at_diagnosis = file_information[i][2]
            exposures_years_smoke = file_information[i][5]
            exposures_cigarettes_per_day = file_information[i][4]
            if days_old_at_diagnosis == "":
                days_old_at_diagnosis = 0
            if exposures_years_smoke == "":
                exposures_years_smoke = 0
            if exposures_cigarettes_per_day == "":
                exposures_cigarettes_per_day = 0
            file_objects_list.append(
                Attributes.Attributes(file_information[i][0], file_information[i][1], file_information[i][7],
                                      file_information[i][3], days_old_at_diagnosis, exposures_years_smoke,
                                      exposures_cigarettes_per_day, file_ids[i-1]))
    return file_objects_list



if __name__ == "__main__":
    main()

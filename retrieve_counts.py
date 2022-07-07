import time
import os, shutil, fnmatch, gzip
import json
import requests
import hashlib
import urllib
import pandas as pd
from pathlib import Path

TCGA_Barcode_Dict = {}
File_ID_Dict = {}


BLA = [
    "0396e511-86ab-4d95-8415-ff107764f8ce",
    "219fa29f-3da2-4ee1-991f-18dcca25184a",
    "31afdd90-b09f-429d-9371-16c92c3fa4dd",
    "d7cc4e9e-cd60-4995-ac43-fff15bbc671d",
    "e829dfb2-2113-4471-b4cc-72a0e77bcd89",
    "f83c858c-c5c5-4ba6-94c8-a4a29a749261"]



# Hardcoded a random list with file ids
TESTSET = ['033a3728-a55c-4d7b-bffb-dd4990684f38',
           '0e903a34-9c87-4444-abfa-fa22882f2cd5',
           '2c21b8cc-43f3-4926-919b-9202b0c8e745',
           '65509594-c7a3-441c-ae35-026b9f296ef4',
           '6b2e3689-7b3f-46e3-aa43-7e5eec010727',
           '6f85f46a-0b68-4f9d-8839-891ce4e98669',
           '895bc144-af38-4ae9-b6d7-3dca677082fb',
           'a15b496c-8c52-43fc-8080-9747eed5ee60',
           'ec1c40a3-24a1-41f1-ba22-3e90b82e378f',
           'f1020d56-a422-4627-99fa-57ad2900f3fa']

# Hardcoded a random list with file ids
DIFFERENTIDS = ['65509594-c7a3-441c-ae35-026b9f296ef4',
                '6b2e3689-7b3f-46e3-aa43-7e5eec010727',
                'a15b496c-8c52-43fc-8080-9747eed5ee60',
                'c19ed7ed-e850-4597-b8aa-836b15ad4a1d',
                'd7cc4e9e-cd60-4995-ac43-fff15bbc671d',
                'e829dfb2-2113-4471-b4cc-72a0e77bcd89',
                'ec1c40a3-24a1-41f1-ba22-3e90b82e378f']


class Filter(object):

    def __init__(self):
        self.filter = {"op": "and", "content": []}

    def add_filter(self, Field, Value, Operator):
        self.filter['content'].append({"op": Operator, "content": {"field": Field, "value": Value}})

    def create_filter(self):
        self.final_filter = json.dumps(self.filter, separators=(',', ':'))
        return self.final_filter


def main():
    mapLoc = create_directory()
    create_filter(BLA)
    merge_files(mapLoc)
    normalize_data(mapLoc)


def create_directory():
    """
    Creates a directory where the files can be downloaded

    Returns:
        map_Loc: Path to the created directory
    """
    global OFILE
    global PARAM
    timestr = time.strftime("%Y%m%d-%H%M%S")

    dir_path = os.path.dirname(os.path.realpath(__file__))
    File = dir_path
    mapLoc = str(Path(File).parents[0]) + '/Map_' + timestr + '/'

    os.makedirs(mapLoc)

    OFILE = {'data': mapLoc + "{ES}/{WF}/{DT}/{uuid}/{name}"}

    PARAM = {
        'url-data': "https://api.gdc.cancer.gov/data/{uuid}",
        'max retry': 10,
    }

    return mapLoc


def create_filter(ids):
    """
    Creates a filter class needed for retrieving file info

    Args:
        ids: A list with file id's
    """
    File_Filter = Filter()
    File_Filter.add_filter("files.file_id", ids, "in")
    File_Filter.add_filter("files.analysis.workflow_type",
                           ["HTSeq - Counts", "HTSeq - FPKM", "HTSeq - FPKM-UQ", "BCGSC miRNA Profiling"], "in")
    File_Filter.create_filter()

    retrieve_file_info(File_Filter)


def retrieve_file_info(File_Filter):
    """
    Requests the GDC data portal to retrieve file information. Creates

    Args:
        File_Filter: Filter class used to be
    """
    EndPoint = 'files'
    Fields = 'cases.samples.portions.analytes.aliquots.submitter_id,file_name,cases.samples.sample_type,file_id,md5sum,experimental_strategy,analysis.workflow_type,data_type'
    Size = '10000'

    Payload = {'filters': File_Filter.create_filter(),
               'format': 'json',
               'fields': Fields,
               'size': Size}
    r = requests.post('https://api.gdc.cancer.gov/files', json=Payload)
    data = json.loads(r.text)
    file_list = data['data']['hits']

    file_to_dictionary(file_list)


def file_to_dictionary(file_list):
    """
    Stores the file information in a dictionary. The dictionary is used later to download the RNA-seq counts

    Args:
        file_list: A list with information about the file
    """
    Dictionary = {}

    for file in file_list:
        UUID = file['file_id']
        Barcode = file['cases'][0]['samples'][0]['portions'][0]['analytes'][0]['aliquots'][0]['submitter_id']
        File_Name = file['file_name']

        Dictionary[UUID] = {'File Name': File_Name,
                            'TCGA Barcode': Barcode,
                            'MD5': file['md5sum'],
                            'Sample Type': file['cases'][0]['samples'][0]['sample_type'],
                            'Experimental Strategy': file['experimental_strategy'],
                            'Workflow Type': file['analysis']['workflow_type'],
                            'Data Type': file['data_type']}

        TCGA_Barcode_Dict[File_Name] = {Barcode}
        File_ID_Dict[File_Name] = {UUID}

    download_counts(Dictionary)


def download_counts(Dictionary):
    for key, value in Dictionary.items():
        download(key,
                 value['File Name'],
                 value['MD5'],
                 value['Experimental Strategy'],
                 value['Workflow Type'],
                 value['Data Type'])


def download(uuid, name, md5, ES, WF, DT, retry=0):
    """
    Download the RNA-seq count data from the GDC data portal

    Args:
        Dictionary with information about the files
    """
    try:
        fout = OFILE['data'].format(ES=ES, WF=WF, DT=DT, uuid=uuid, name=name)

        def md5_ok():
            with open(fout, 'rb') as f:
                return (md5 == hashlib.md5(f.read()).hexdigest())

        print("Downloading (attempt {}): {}".format(retry, uuid))
        url = PARAM['url-data'].format(uuid=uuid)

        with urllib.request.urlopen(url) as response:
            data = response.read()

        os.makedirs(os.path.dirname(fout), exist_ok=True)

        with open(fout, 'wb') as f:
            f.write(data)

        if md5_ok():
            return (uuid, retry, md5_ok())
        else:
            os.remove(fout)
            raise ValueError('MD5 Sum Error on ' + uuid)
    except Exception as e:
        print("Error (attempt {}): {}".format(retry, e))
        if (retry >= PARAM['max retry']):
            raise e
        return download(uuid, name, md5, ES, WF, DT, retry + 1)


def merge_files(mapLoc):
    """
    Merged the downloaded RNA-seq counts data to one .tsv file

    Args:
        mapLoc: The path where to find the downloaded count data
    """
    RNASeq_WFs = ['HTSeq - Counts', 'HTSeq - FPKM-UQ', 'HTSeq - FPKM']

    GZipLocs = [mapLoc + 'RNA-Seq/' + WF for WF in RNASeq_WFs]

    for i in range(len(RNASeq_WFs)):

        print('--------------')
        pattern = '*.gz'  # pattern to find .gz files and ungzip into the folder
        Files = []

        if os.path.exists(GZipLocs[i] + '/UnzippedFiles/'):
            shutil.rmtree(GZipLocs[i] + '/UnzippedFiles/')
            os.makedirs(GZipLocs[i] + '/UnzippedFiles/')
        else:
            os.makedirs(GZipLocs[i] + '/UnzippedFiles/')

        for root, dirs, files in os.walk(GZipLocs[i]):
            for filename in fnmatch.filter(files, pattern):
                OldFilePath = os.path.join(root, filename)
                NewFilePath = os.path.join(GZipLocs[i] + '/UnzippedFiles/', filename.replace(".gz", ".tsv"))

                gunzip(OldFilePath, NewFilePath)  # unzip to New file path

                Files.append(NewFilePath)  # append file to list of files

        Matrix = {}

        for file in Files:
            p = Path(file)
            Name = str(p.name).replace('.tsv', '')
            Name = Name + '.gz'
            Name = File_ID_Dict[Name]
            Name = str(list(Name)[0])
            Counts_DataFrame = pd.read_csv(file, sep='\t', header=None, names=['GeneId', Name])
            Matrix[Name] = tuple(Counts_DataFrame[Name])

        if len(Matrix) > 0:
            Merged_File_Name = 'Merged_' + RNASeq_WFs[i].replace('HTSeq - ', '') + '.tsv'
            print('Creating merged ' + RNASeq_WFs[i] + ' File... ' + '( ' + Merged_File_Name + ' )')
            Counts_Final_Df = pd.DataFrame(Matrix, index=tuple((Counts_DataFrame['GeneId'])))
            Counts_Final_Df.drop(Counts_Final_Df.tail(5).index, inplace=True)
            Counts_Final_Df.to_csv(str(mapLoc) + '/' + Merged_File_Name, sep='\t', index=True)


def gunzip(file_path, output_path):
    """
    Unzips downloaded RNA-SEQ count files
    """
    with gzip.open(file_path, "rb") as f_in, open(output_path, "wb") as f_out:
        shutil.copyfileobj(f_in, f_out)


def get_gene_symbols():
    """
    Creates a dataframe from GitHub.

    Returns:
        A dataframe with Gene id's as index and gene symbols as data
    """
    url = 'https://github.com/cpreid2/gdc-rnaseq-tool/raw/master/Gene_Annotation/gencode.v22.genes.txt'
    gene_map = pd.read_csv(url, sep='\t')
    gene_map = gene_map[['gene_id', 'gene_name']]
    gene_map = gene_map.set_index('gene_id')

    return gene_map


def normalize_data(mapLoc):
    """
    Normalize the retrieved HT-SEQ count data.
    This function calls normalize_data.R

    Args:
        mapLoc: Path to working directory
    """
    file = mapLoc + "Merged_Counts.tsv"
    print("Normalizing " + file)
    print("--------------")

    os.system("Rscript normalize_data.R " + file)
    Counts_DataFrame = pd.read_csv(mapLoc + "Normalized_Counts.tsv", sep='\t')

    gene_map = get_gene_symbols()
    Counts_Final_Df = gene_map.merge(Counts_DataFrame, how='right', left_index=True, right_index=True)
    Counts_Final_Df.to_csv(mapLoc + "Normalized_Counts.tsv", sep="\t")


if __name__ == "__main__":
    main()
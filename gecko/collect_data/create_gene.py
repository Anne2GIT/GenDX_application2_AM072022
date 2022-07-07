from gecko.objects import Gene
import csv


def main():
    file_information_list = open_file()
    gene_list = create_dict(file_information_list)
    for i in gene_list:
        print(i.name)
        print(i.number)
        print(i.counts)


def open_file(map_loc):
    """
    Opens a file and saves the information in a list
    :param map_loc: Location for the target file
    :return: file_information_list: a list containing the gene names, filenames, and counts

    """
    filename = map_loc + 'Normalized_Counts.tsv'
    with open(filename) as tsvfile:
        file_information_list = []
        reader = csv.reader(tsvfile, dialect='excel-tab')
        for row in reader:
            file_information_sublist = []
            file_information_sublist.append(row[0])
            for i in range(len(row[2:])):
                file_information_sublist.append(row[i+2])
            file_information_list.append(file_information_sublist)
    return file_information_list


def create_dict(file_information_list):
    """
    Creates a list of files containing Gene objects
    :param file_information_list: a list containing the gene names, filenames, and counts
    :return: gene_list: a list containing gene objects
    """
    filenames_temp = file_information_list[0]
    file_names = filenames_temp[1:]
    gene_list = []
    gen_number = get_gennummer()

    for i in file_information_list[1:]:
        gene_name = i[0]
        counts_list = i[1:]
        counts_dict = {}

        for index, counts in enumerate(counts_list):
            filename =file_names[index]
            counts_dict.update( {filename : counts})
        gene = Gene.Gene(gen_number, gene_name, counts_dict)
        gen_number = gen_number + 1
        gene_list.append(gene)
    return gene_list


def get_gennummer():
    """
    get the number of genes in the database to determine the new gen_number
    :return: unique_number: the new gen number that will be used to create a new Gene object
    """
    number = 0
    unique_number = number+1
    return unique_number


if __name__ == "__main__":
    main()
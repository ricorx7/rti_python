


def generate_csv(file_path, df):
    """
    Convert the dataframe to an CSV file
    In clude the id and class.
    :param file_path: File path to write the file.
    :param df: Dataframe to convert.
    :return:
    """
    df.to_csv(file_path, encoding='utf-8', index=False)
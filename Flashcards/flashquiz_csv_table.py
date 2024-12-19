from pandas import read_csv
from streamlit import cache_data


@cache_data
def flashquiz_csv_table(file_obj):
    """
    Reads a CSV file with two columns: FrontText and BackText, and returns a DataFrame.
    """
    # Read the CSV file into a pandas DataFrame
    df = read_csv(file_obj)

    # Ensure the DataFrame contains the required columns
    if not {"FrontText", "BackText"}.issubset(df.columns):
        raise ValueError("The CSV file must have 'FrontText' and 'BackText' columns.", icon="🚫")

    return df
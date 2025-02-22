from pandas import read_excel
from streamlit import cache_data

@cache_data
def xlsx_table(file_obj):
    """
    Reads an Excel file with two columns: English and Deutsch, and returns a DataFrame.
    """
    # Read the Excel file into a pandas DataFrame
    df = read_excel(file_obj)

    # Ensure the DataFrame contains the required columns
    if not {"English", "Deutsch"}.issubset(df.columns):
        raise ValueError("The Excel file must have 'English' and 'Deutsch' columns.", icon="🚫")

    return df
# Function to parse .flashquiz file and extract FrontText and BackText
from xml.etree.ElementTree import fromstring
from pandas import DataFrame, ExcelWriter
from io import BytesIO
from streamlit import cache_data, write

@cache_data
def flashquiz_to_xlsx(file_content):
    # Parse the content as XML
    root = fromstring(file_content)

    # Define namespaces (based on your debug output)
    namespaces = {
        "peach": "http://schemas.datacontract.org/2004/07/Peach.Sharing",
        "ms_array": "http://schemas.microsoft.com/2003/10/Serialization/Arrays",
        "peach_card": "http://schemas.datacontract.org/2004/07/Peach",
    }

    # Initialize lists to hold FrontText and BackText pairs
    front_texts = []
    back_texts = []

    # Find all Cards
    for card in root.findall(".//peach_card:Card", namespaces=namespaces):
        # Extract FrontText and BackText
        front_text = card.find("peach_card:FrontText", namespaces=namespaces)
        back_text = card.find("peach_card:BackText", namespaces=namespaces)

        # Add them to the lists if both are present
        if front_text is not None and back_text is not None:
            front_texts.append(front_text.text)
            back_texts.append(back_text.text)

    # Create a DataFrame with the collected data
    df = DataFrame({"English": front_texts, "Deutsch": back_texts})

    # Convert DataFrame to Excel content as a bytes object
    output = BytesIO()
    with ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, index=False, sheet_name='Flashcards')
    xlsx_data = output.getvalue()
    
    return xlsx_data
import PyPDF2
import pandas as pd


indexes_to_remove_A = [0,6,7,8,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37,38,39,40]
indexes_to_remove_B = [0,1,2,26,27,28,29,30,31,32,33,36,37,38,39,40,41,42,43,44,45,46,47,48,49] 

def extract_data_from_pdf(pdf_path, key_title):
    extracted_data = []

    with open(pdf_path, 'rb') as pdf_file:
        pdf_reader = PyPDF2.PdfReader(pdf_file)

        for page_num in range(len(pdf_reader.pages)):
            page = pdf_reader.pages[page_num]
            text = page.extract_text()

            # Check if the key title is present on the page
            if key_title in text:
                # Find the start and end indices of the table data
                start_index = text.index(key_title)
                end_index = text.find("Source:", start_index)  # Assuming "Source:" is the end of your data

                # Extract the table data
                table_data = text[start_index:end_index].strip()

                # Add the extracted data to the list
                extracted_data.append(table_data)

    return extracted_data

def clean_data(raw_data,colum_num):
    # Split the string into lines
    lines = raw_data[0].split('\n')

    # Initialize an empty list to store data
    data_list = []

    for line in lines:
        # Split line by whitespace
        values = line.split()

        # Check if the line has enough values
        if len(values) >= 4:
            # Extract values and append to data_list
            category = ' '.join(values[:-colum_num])
            data = values[-colum_num:]

            data_list.append({"Category": category, "Dec. 2022": data[0], "Oct. 2023": data[1],
                              "Nov. 2023": data[2], "Dec. 2023": data[3],
                              "Change from: Nov. 2023-Dec. 2023": data[len(data) - 1]})

    # Create a DataFrame from the list of dictionaries
    df = pd.concat([pd.DataFrame([data_dict]) for data_dict in data_list], ignore_index=True)

    df["Category"] = df["Category"].str.replace('\.+', '', regex=True)

    return df

def filter_data(data_frame,indexes_to_remove):
    # List of categories to keep
      # Replace with the indexes you want to remove
    filtered_df = data_frame.drop(indexes_to_remove)


    return filtered_df

def save_to_csv(data_frame, filename):
    # Save the DataFrame to a CSV file
    data_frame.to_csv(filename, index=False)

# Example usage
pdf_path = 'F:/python_dev/pdf_automation/empsit.pdf'
key_title_A = 'Summary table A. Household data, seasonally adjusted'
key_title_B = 'Summary table B. Establishment data, seasonally adjusted'

raw_data = extract_data_from_pdf(pdf_path, key_title_A)
cleaned_data = clean_data(raw_data,5)
filtered_data = filter_data(cleaned_data,indexes_to_remove_A)

# Save the filtered DataFrame to a CSV file
save_to_csv(filtered_data, "filtered A.csv")

# Save the cleaned DataFrame to a CSV file
save_to_csv(cleaned_data, "output A.csv")

raw_data = extract_data_from_pdf(pdf_path, key_title_B)
cleaned_data = clean_data(raw_data,4)
filtered_data = filter_data(cleaned_data,indexes_to_remove_B)

# Save the filtered DataFrame to a CSV file
save_to_csv(filtered_data, "filtered B.csv")

# Save the cleaned DataFrame to a CSV file
save_to_csv(cleaned_data, "output B.csv")


print(cleaned_data)

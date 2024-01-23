import PyPDF2
import pandas as pd


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

# Example usage
pdf_path = 'F:/python_dev/pdf_automation/empsit.pdf'
key_title = 'Summary table B. Establishment data, seasonally adjusted'

result = extract_data_from_pdf(pdf_path, key_title)



# Split the string into lines
lines = result[0].split('\n')

# Initialize an empty list to store data
data_list = []

# Iterate through lines and extract data
for line in lines:
    # Split line by whitespace
    values = line.split()



    # Check if the line has enough values
    if len(values) >= 4:
        # Extract values and append to data_list
        category = ' '.join(values[:-4])
        data = values[-4:]
     
        data_list.append({"Category": category, "Dec. 2022": data[0], "Oct. 2023": data[1],
                          "Nov. 2023": data[2], "Dec. 2023": data[3],
                          "Change from: Nov. 2023-Dec. 2023": data[3]})

# Create a DataFrame from the list of dictionaries
df = pd.concat([pd.DataFrame([data_dict]) for data_dict in data_list], ignore_index=True)
df["Category"] = df["Category"].str.replace('\.+', '', regex=True)


# Save the DataFrame to a CSV file
df.to_csv("output B.csv", index=False)



# Drop specific indexes from the DataFrame
indexes_to_remove = [1, 2,26,27,28,29,30,31,32,33,36,37,38,39,40,41,42,43,44,45,46,47,48,49]  # Replace with the indexes you want to remove
df = df.drop(indexes_to_remove)



# Save the DataFrame to a CSV file
df.to_csv("filtered B.csv", index=False)







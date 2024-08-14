import json
import csv
from simplegmail import Gmail
from bs4 import BeautifulSoup

gmail = Gmail()

# Define the sender email you want to filter by
sender_email = "*@web3forms.com"

# Get the emails that match the query
emails = gmail.get_messages(query=f"from:{sender_email}")

# Define the CSV file to save the data to
csv_file = "form_data.csv"

# Define the CSV writer
with open(csv_file, "w", newline="") as csvfile:
    writer = csv.DictWriter(csvfile, fieldnames=["Form Name", "Name", "Email", "Message"])

    # Write the header row
    writer.writeheader()

    # Print the form data from the email body
    for message in emails:
        html = message.html
        soup = BeautifulSoup(html, 'html.parser')
        text = soup.get_text()
        if "Form_name" in text and "Data" in text:
            lines = text.split("\n")
            form_name = None
            data = None
            for line in lines:
                if "Form_name" in line:
                    form_name = line.split(" ")[1].strip()
                elif "Data" in line:
                    data_line = line
                    for next_line in lines[lines.index(line) + 1:]:
                        if next_line.strip():
                            data_line += " " + next_line
                        else:
                            break
                    # Try to parse the JSON data
                    try:
                        data = json.loads(data_line.split("Data")[-1].strip())
                        print("JSON Data:", data)

                        # Write the data to the CSV file
                        writer.writerow({
                            "Form Name": form_name,
                            "Name": data.get("name"),
                            "Email": data.get("email"),
                            "Message": data.get("message")
                        })
                    except json.JSONDecodeError:
                        pass
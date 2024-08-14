from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import date
gmail = Gmail()


# year month day
''' label
    sent: Sent messages
    inbox: Inbox messages
    drafts: Draft messages
    spam: Spam messages
    trash: Trash messages
'''
query_params = {

    #"after": date.today().strftime("%Y/%m/%d"),
"newer_than": (2, "day"),
    "older_than": (0, "day"),
    "label": "inbox"


}
messages = gmail.get_messages(query=construct_query(query_params))

for message in messages:
   # print("To: " + message.recipient)
  #  print("From: " + message.sender)
   # print("Subject: " + message.subject)
  #  print("Date: " + message.date)
  #  print("Preview: " + message.snippet)
    
    with open("email_samples.txt", "a", encoding="utf-8") as f:
        if message.plain:
            if len(message.plain) < 1000:
               # f.write(message.plain)
                print("Message Body: " + message.plain)
        # or message.html
'''from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import date

gmail = Gmail()

# year month day
'''# label
  #  sent: Sent messages
   # inbox: Inbox messages
  #  drafts: Draft messages
  #  spam: Spam messages
   # trash: Trash messages
'''
query_params = {

    # "after": date.today().strftime("%Y/%m/%d"),
    "newer_than": (1, "day"),
    "older_than": (0, "day"),
    "label": "inbox"

}
messages = gmail.get_messages(query=construct_query(query_params))

for message in messages:
    # print("To: " + message.recipient)
    print("From: " + message.sender)
    # print("Subject: " + message.subject)
    # print("Date: " + message.date)
    # print("Preview: " + message.snippet)
    if message.plain:
        if len(message.plain) < 1000:
            with open("email_samples.txt", "a", encoding="utf-8") as f:
                print("sgd")
                # f.write(message.plain)
                # print("Message Body: " + message.plain)'''
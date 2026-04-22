import win32com.client
import win32com
import os
import sys

outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
accounts= win32com.client.Dispatch("Outlook.Application").Session.Accounts

# print send of emails in specified folder.
def emailleri_al(folder):
    messages = folder.Items
    a=len(messages)
    if a>0:
        for message2 in messages:
             try:
                # sender = message2.SenderEmailAddress
                sender = message2.Subject
                if sender != "":
                    print(sender)
             except:
                print("Error")
                print(account.DeliveryStore.DisplayName)
                pass

            #  try:
            #     message2.Save
            #     message2.Close(0)
            #  except:
            #      pass

# print folder names
for account in accounts:
    global inbox
    inbox = outlook.Folders(account.DeliveryStore.DisplayName)
    if account.DisplayName == "Tamilyn.Peck2@extendhealth.com":
        continue
    print("****Account Name**********************************")
    print(account.DisplayName)
    print("***************************************************")
    folders = inbox.Folders
    # Personal Email inbox 6
    # DataSupport Email Inbox 1
    print(folders[1]) 
    subFolders = folders[1].Folders
    # podFour = folders[1].Folders['.Pod4']
    SQLNotification = folders[1].Folders['SQL Notification']
    # podFourFolders = folders[1].Folders['.Pod4'].Folders
    SQLNotificationfolder = folders[1].Folders['SQL Notification'].Folders
    podFourCompletedFolders = folders[1].Folders['.Pod4'].Folders['Completed'].Folders
    for f in podFourCompletedFolders:
        print(f) 

    # emailleri_al(folders[1])
    # emailleri_al(podFour)
print("***************************************************")
print("Finished Succesfully")


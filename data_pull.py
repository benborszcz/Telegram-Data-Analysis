import codecs
import json
import os

TARGET_NAME = 'Ben Borszcz' #put the name of the users data you want to get


CONTEXT_MESSAGES = 6
MESSAGE_MINIMUM_DELTA = 300
MAX_TIMED_MESSAGES = 10

TELEGRAM_FILE_NAME = 'Lions Den Data' #do not put .json


if not os.path.exists('Data'):
    os.makedirs('Data')

if not os.path.exists('Data\\'+TARGET_NAME.replace(' ','_')):
    os.makedirs('Data\\'+TARGET_NAME.replace(' ','_'))

with codecs.open('Data\\'+TELEGRAM_FILE_NAME+'.json', 'r', encoding='utf-8') as f:
    data = json.load(f)


messages = []
messages_with_context = []
timed_conversation_messages = []
names = {}
names_with_times = {}
min_time = int(data['messages'][0]['date_unixtime'])



"""-----------------------Parsing Through All Messages-----------------------"""

print("----------------------------------------------------------")
print("-               Starting All Message Parse               -")
print("----------------------------------------------------------")

for i, msg in enumerate(data['messages']):
    
    print("Parsing Message "+str(i+1)+"...")
    
    # Only parse messages
    if msg['type'] != 'message': 
        continue

    # Get rid of empty messages, mainly meant to remove images
    if msg['text'] == "": 
        continue

    # Set person to the senders name, if the sender has deleted their account set to user ID
    person = msg['from']
    if person == None:
        person = msg['from_id']

    # If person is the target name collect their messages and context for their messages and timed conversation messages
    if person == TARGET_NAME:
        
        # simple message list
        messages.append(msg)

        # messages with context
        context = []
        for j in range(CONTEXT_MESSAGES,0,-1):
            context.append(data['messages'][i-j])
        context.append(msg)
        messages_with_context.append(context)

        # timed conversation messages
        context = [msg]
        for j in range(1,MAX_TIMED_MESSAGES-1):
            if abs(int(data['messages'][i-j]['date_unixtime'])-int(context[0]['date_unixtime'])) <= MESSAGE_MINIMUM_DELTA:
                context.insert(0, data['messages'][i-j])
        
        timed_conversation_messages.append(context)

    # Get all users and add there total message count or timestamps
    if person in names:
        names[person] = names[person]+1
        names_with_times[person].append(int(msg['date_unixtime'])-min_time)
    else:
        names[person] = 1
        names_with_times[person] = [int(msg['date_unixtime'])-min_time]
   

# Sorts all of the users by total messages sent
sorted_names = dict(sorted(names.items(), key=lambda x: x[1], reverse=True))





print("----------------------------------------------------------")
print("-              Saving Total User Information             -")
print("----------------------------------------------------------")

"""-------------------------Total User Pool File Dumps-------------------------"""

# Dump the users and their totals into users.json
with codecs.open('Data\\users.json', 'w', encoding='utf-8') as f:
    json.dump(sorted_names, f, indent=4)

# Dump the users and an array of when their messages were sent into users_with_times.json
with codecs.open('Data\\users_with_times.json', 'w', encoding='utf-8') as f:
    json.dump(names_with_times, f, indent=4)


print("----------------------------------------------------------")
print("-              Saving Target User Information            -")
print("----------------------------------------------------------")

"""---------------------------Target User File Dumps---------------------------"""

# Dumps the messages for the target user into target_user_messages.json
with codecs.open('Data\\'+TARGET_NAME.replace(' ','_')+"\\"+TARGET_NAME.replace(' ','_')+'_messages.json', 'w', encoding='utf-8') as f:
    json.dump(messages, f, indent=4)

# Dumps the messages and the untimed context for each message for the target user into target_user_messages_with_context.json
with codecs.open('Data\\'+TARGET_NAME.replace(' ','_')+"\\"+TARGET_NAME.replace(' ','_')+'_messages_with_context.json', 'w', encoding='utf-8') as f:
    json.dump(messages_with_context, f, indent=4)

# Dumps the messages and the timed context for each message for the target user into target_user_messages_timed_conversation_messages.json
with codecs.open('Data\\'+TARGET_NAME.replace(' ','_')+"\\"+TARGET_NAME.replace(' ','_')+'_timed_conversation_messages.json', 'w', encoding='utf-8') as f:
    json.dump(timed_conversation_messages, f, indent=4)









def parse_text_object(msg):
    unicode_dict = {
        '\u2019': '\'',
        '\u2018': '\'',
        '\u201c': '"',
        '\u201d': '"',
        '\u00bf': '?', 
        '\u2026': '...',
    }
    
    text_list = msg['text']
    result = ""
    for item in text_list:
        if isinstance(item, str):
            result += item
        elif isinstance(item, dict) and item.get('type') == 'mention_name':
            result += f"@{item['text']}"
        elif isinstance(item, dict) and item.get('type') == 'mention':
            result += f"{item['text']}"
        elif isinstance(item, dict) and item.get('type') == 'link':
            result += f"{item['text']}"


    for key, value in unicode_dict.items():
        result = result.replace(key, value)


    return result.strip()



def slim_message_data(message_data, file_name):
    
    slimmed_list = []
    for c, group in enumerate(message_data):
        
        print("Slimming Message "+str(c+1)+"...")

        slimmed_list_item = {}
        for i, msg in enumerate(group):
            if i == len(group)-1: break

            result = parse_text_object(msg)
            if result == '' or result == None: continue

            person = msg['from']
            if person == None:
                person = msg['from_id']

            slimmed_list_item['prefix'+str(len(group)-i-1)] = person
            slimmed_list_item['context'+str(len(group)-i-1)] = result
    
        result = parse_text_object(group[-1])
        if result == '' or result == None: continue

        response = result

        slimmed_list_item['prefix'] = TARGET_NAME
        slimmed_list_item['response'] = response
        slimmed_list.append(slimmed_list_item)

    

    with codecs.open('Data\\'+TARGET_NAME.replace(' ','_')+"\\"+TARGET_NAME.replace(' ','_')+'_'+file_name+'_slimmed_data.json', 'w', encoding='utf-8') as f:
        json.dump(slimmed_list, f, indent=4)


    return slimmed_list

print("----------------------------------------------------------")
print("-              Starting User Message Slimming            -")
print("----------------------------------------------------------")

#slim_message_data(messages, 'messages')
slim_message_data(messages_with_context, 'messages_with_context')
slim_message_data(timed_conversation_messages, 'timed_conversation_messages')

print("----------------------------------------------------------")
print("-                        Complete!                       -")
print("----------------------------------------------------------\n")
print("Your files were save to the \"Data\" folder. Make sure to display hidden files")

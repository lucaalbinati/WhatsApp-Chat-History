# WhatsApp-Chat-History

## Description
Given a WhatsApp group conversation history as input, it outputs some interesting statistics about the people within the group and their contribution to the conversation.
This includes how many messages they sent, whether they were simple messages or media attachments, as well as how they vary through time.

## Setup

### Download the repository
```
git clone git@github.com:lucaalbinati/WhatsApp-Chat-History.git
cd WhatsApp-Chat-History
```

### Create ```data``` folder
```
mkdir data
cp 'your_whatsapp_group_conversion_name.txt' data
```
Currently the program only supports the ```.txt``` extension.

### Run
```
python main.py 'your_whatsapp_group_conversion_name'
```

Once the program finishes, you can find the results in the new folder, ```output/'your_whatsapp_group_conversion_name'```.

## 🛠 Improvements

Feel free to create an issue or a pull request in case you find bugs or want to add a feature!

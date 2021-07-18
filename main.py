from dateutil import parser
from datetime import datetime
import re
import matplotlib.pyplot as plt
import matplotlib
import collections

DATE_MESSAGE_SEPARATOR = " - "
DATE_REGEX = r"^([0]{0,1}[1-9]|1[012])\/([1-9]|([012][0-9])|(3[01]))\/\d\d,\s([0-1]?[0-9]|2?[0-3]):([0-5]\d)$"
SENDER_MESSAGE_SEPARATOR = ": "
MEDIA_OMITTED_MESSAGE = "<Media omitted>\n"
SENDER_UNKNOWN = "Unknown"

def convert_file_to_list(path):
	# return list of tuple: (date, sender, message)

	f = open(path, 'r')
	lines = f.readlines()

	dated_messages = []

	curr_date = ""
	curr_sender = ""
	curr_message = ""

	for line in lines:
		try:
			date_message_separator_index = line.index(DATE_MESSAGE_SEPARATOR)
			potential_date = line[:line.index(DATE_MESSAGE_SEPARATOR)]
	
			if re.match(DATE_REGEX, potential_date):
				if curr_date != "":
					# on the first line, 'curr_date' will be equal to "", so we don't append anything
					dated_messages.append((curr_date, curr_sender, curr_message))

				sender_message_begin_index = date_message_separator_index + len(DATE_MESSAGE_SEPARATOR)
				sender_message = line[sender_message_begin_index:]
				sender_end_index = sender_message.index(SENDER_MESSAGE_SEPARATOR)
				message_begin_index = sender_end_index + len(SENDER_MESSAGE_SEPARATOR)

				curr_date = potential_date
				curr_sender = sender_message[:sender_end_index]
				curr_message = sender_message[message_begin_index:]
			else:
				curr_message += line
		except ValueError as e:
			continue

	f.close()
	return dated_messages

def convert_dates(dated_messages):
	for i, (date_str, sender, message) in enumerate(dated_messages):
		date = parser.parse(date_str)
		dated_messages[i] = (date, sender, message)
	return dated_messages

def amount_per_month(dated_messages):
	# return dict with key=(month,year) and value=(nb_all, nb_messages, nb_media)

	nb_per_month = {}
	for (date, _, message) in dated_messages:
		month_year = datetime(year=date.year, month=date.month, day=1)
		if month_year in nb_per_month:
			prev_nb_all = nb_per_month[month_year][0]
			prev_nb_messages = nb_per_month[month_year][1]
			prev_nb_media = nb_per_month[month_year][2]

			if is_media(message):
				nb_per_month[month_year] = (prev_nb_all + 1, prev_nb_messages, prev_nb_media + 1)
			else:
				nb_per_month[month_year] = (prev_nb_all + 1, prev_nb_messages + 1, prev_nb_media)
		else:
			if is_media(message):
				nb_per_month[month_year] = (1, 0, 1)
			else:
				nb_per_month[month_year] = (1, 1, 0)

	# order it
	nb_per_month = collections.OrderedDict(sorted(nb_per_month.items()))
	return nb_per_month

def plot_month_frequency(nb_per_month):
	keys = list(nb_per_month.keys())
	values = list(nb_per_month.values())

	ax = plt.gca()
	xaxis = matplotlib.dates.date2num(keys)
	hfmt = matplotlib.dates.DateFormatter("%m/%y")
	ax.xaxis.set_major_formatter(hfmt)
	key_ticks = [k for i, k in enumerate(keys) if i % 2 == 0]
	ax.xaxis.set_ticks(key_ticks)

	plt.xlabel("Date (month/year)")
	plt.ylabel("Number of messages/media sent")
	plt.xticks(rotation=65)
	plt.plot(xaxis, values)
	plt.title("Sending activity across time")
	plt.legend(["all", "messages", "media"])
	plt.show()

def plot_sender_stats(dated_messages):
	# dict with key=sender, value=(nb_messages, nb_chars, nb_media)
	sender_stats = {}

	for (_, sender, message) in dated_messages:
		if sender == SENDER_UNKNOWN:
			continue

		if sender in sender_stats:
			prev_nb_messages = sender_stats[sender][0]
			prev_nb_chars = sender_stats[sender][1]
			prev_nb_media = sender_stats[sender][2]
			if is_media(message):
				sender_stats[sender] = (prev_nb_messages, prev_nb_chars, prev_nb_media + 1)
			else:
				sender_stats[sender] = (prev_nb_messages + 1, prev_nb_chars + len(message), prev_nb_media)
		else:
			if is_media(message):
				sender_stats[sender] = (0, 0, 1)
			else:
				sender_stats[sender] = (1, len(message), 0)

	for sender, (nb_messages, nb_chars, nb_media) in sender_stats.items():
		print("{}: {} messages sent ({} characters in total), {} media sent".format(sender, nb_messages, nb_chars, nb_media))

	senders = list(sender_stats.keys())
	values = list(sender_stats.values())
	nb_messages = [v[0] for v in values]
	nb_chars = [v[1] for v in values]
	nb_media = [v[2] for v in values]

	plt.bar(senders, nb_messages)
	plt.bar(senders, nb_media)
	plt.title("Overall sending activity")
	plt.legend(["messages sent", "media sent"])
	plt.show()

	plt.bar(senders, nb_chars)
	plt.title("Overall characters sent")
	plt.show()

	avg_chars_per_message = [nb_char/nb_message for nb_message, nb_char in zip(nb_messages, nb_chars)]
	plt.bar(senders, avg_chars_per_message)
	plt.title("Average messages' length")
	plt.show()

def is_media(message):
	return message == MEDIA_OMITTED_MESSAGE

def print_dated_messages(dated_messages):
	for (date, sender, msg) in dated_messages:
		print(date)
		print(sender)
		print(msg)

def main():
	dated_messages = convert_file_to_list("data/Neuer.txt")
	dated_messages = convert_dates(dated_messages)
	nb_per_month = amount_per_month(dated_messages)
	plot_month_frequency(nb_per_month)
	plot_sender_stats(dated_messages)

main()


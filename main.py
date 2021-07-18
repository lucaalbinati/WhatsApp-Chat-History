from dateutil import parser
from datetime import datetime
import re
import matplotlib.pyplot as plt
import matplotlib
import collections

DATE_MESSAGE_SEPARATOR = " - "
DATE_REGEX = r"^([0]{0,1}[1-9]|1[012])\/([1-9]|([012][0-9])|(3[01]))\/\d\d,\s([0-1]?[0-9]|2?[0-3]):([0-5]\d)$"
SENDER_MESSAGE_SEPARATOR = ": "

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
			if "substring not found" in str(e):
				curr_message += line
			else:
				raise e

	f.close()
	return dated_messages

def convert_dates(dated_messages):
	for i, (date_str, message) in enumerate(dated_messages):
		date = parser.parse(date_str)
		dated_messages[i] = (date, message)
	return dated_messages

def amount_per_month(dated_messages):
	# return dict with key=(month,year) and value=amount

	nb_per_month = {}
	for (date, _) in dated_messages:
		month_year = datetime(year=date.year, month=date.month, day=1)
		if month_year in nb_per_month:
			nb_per_month[month_year] += 1
		else:
			nb_per_month[month_year] = 1

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
	plt.ylabel("Number of messages sent")
	plt.xticks(rotation=65)
	plt.plot(xaxis, values)
	plt.show()

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

main()


from nltk.corpus import stopwords

x = 3

stop_rom = set(stopwords.words('romanian'))
stop_eng = set(stopwords.words('english'))

# Common stopwords
stop_rom_eng = stop_rom.intersection(stop_eng)
stop_eng_in_rom = set(['in', 'o', 'a'])
stop_rom_in_eng = set([])

# Prepare stopwords
stop_rom -= stop_rom_eng
stop_eng -= stop_rom_eng
stop_eng -= stop_eng_in_rom
stop_rom -= stop_rom_in_eng

make: # Run the program
	python3 load-json.py

data: # Create the directory where the MongoDB databse will be stored.
	mkdir mongodb_data_folder 
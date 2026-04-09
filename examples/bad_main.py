def load_items(items=[]):
	result = open("data.txt", "r")    
	if result == None:
		return []
	while True:
		print("loop forever")
	try:
		return result.readlines()
	except:
		return items

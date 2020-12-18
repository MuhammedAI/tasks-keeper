from os.path import exists  
import ast # ast.literal_eval() is used


def check_data():

	if not exists("users.txt"):
		return
	users_file = open("users.txt", "r")
	users_dict = {}
	for user in users_file:
		lst = user.strip().split(";")
		user_email = lst[0]
		user_pass = lst[1]
		users_dict[user_email] = user_pass
	return users_dict


def sign_in():
	email = input("Email: ")
	password = input("Password: ")	
	
	if users_dict == None:
		print("Wrong user email or password")

	elif users_dict.get(email) == password:
		print(f"\\Welcome {email}/".center(100),"\n")
		user_page(email)
	else:
		print("Wrong user email or password")


def sign_up():
	email = input("email: ")
	the_valid_email = validate_email(email) 

	password = input("password: ")

	the_valid_password = validate_pass(password)
	password_confirm = input("re-enter password: ")

	while not the_valid_password == password_confirm:
		print("Passwords didn't match! Try again.")
		password = input("password: ")
		the_valid_password = validate_pass(password)
		password_confirm = input("re-enter password: ")

	users_file = open("users.txt", "a")
	users_file.write(the_valid_email+";"+the_valid_password+"\n")
	users_file.close()
	print("User added")


def validate_email(email):
	email = email.strip()
	while True:
		if users_dict:
			if email in users_dict:
				print("This email is already has account!")
				email = input("Email again: ").strip()
				continue
		
		if not ("@" in email and len(email) > 8 ):
			print("This email is Not a valid form! try another one.")
			email = input("Email again: ").strip()

		else:
			return email


def validate_pass(password):
	while not (password[0].isupper() and  len(password) > 11 and not password.isalpha()):
		print("*Password you've entered ["+password +"] is not valid!\nyou have to enter at least 12 characters with letters OR numbers,\nand must start with uppercase letter.")
		password = input("Password again: ")		
	return password

def get_user_tasks(email):
	if exists("tasks.txt"):
		file = open("tasks.txt","r")
		# my idea in example:
		#	dict = {"a":1}
		#	dict_as_str = str({"a":1})
		#	dict_back = ast.literal_eval(dict_as_str)
		file_as_dict = ast.literal_eval(file.read())

		file.close()
		user_tasks = file_as_dict.get(email, [])
		return user_tasks
	else:
		return []

def update_screen(email):
	# update the GUI (i.e. user_page() )
	lol = get_user_tasks(email)
	if len(lol) != 0:
		
		print("\n"+"-"*100)
		print("tasks".center(27)+"|"+"pritority".center(25)+"|"+"percentage of completion".center(25)+"|")
		print("-"*100,"\n")
		for i in range(len(lol)):
			print(f"{i+1}.",end="")
			for j in lol[i]:
					print(j.center(25),end="|")
			print("\n")
	else: 
		print("You have no tasks, yet")
	

def user_page(email):
	lol = get_user_tasks(email)
	if len(lol) != 0:
		
		print("\n"+"-"*100)
		print("tasks".center(27)+"|"+"pritority".center(25)+"|"+"percentage of completion".center(25)+"|")
		print("-"*100,"\n")
		for i in range(len(lol)):
			print(f"{i+1}.",end="")
			for j in lol[i]:
					print(j.center(25),end="|")
			print("\n")
	else: 
		print("You have no tasks, yet")
		
	while True:
		print("\n|"*5)
		option = input("\nAdd new[+]  Update status[#]  Cancel[-]\t--> SignOut[o]\n> ")
		if exists("tasks.txt"):
			file = open("tasks.txt","r")
			file_as_dict = ast.literal_eval(file.read())
			file.close()
		else:
			file_as_dict ={}

		if option == "+":
			
			lst = []
			for tag in ["task_name", "task_priority", "done_%"]:
				i = input(f"{tag} ")
				lst.append(i)
			if not email in file_as_dict:
				file_as_dict[email] = []
				file_as_dict[email].append(lst)
			else:
				
				file_as_dict[email].append(lst)
			
			file = open("tasks.txt", "w")
			file.write(str(file_as_dict))
			file.close()
			
			update_screen(email)
		elif option == "#":
			file = open("tasks.txt", "r")
			file_as_dict = ast.literal_eval(file.read())
			file.close()
			taskno = input("Update task No. ")
			while not (taskno.isnumeric() and (1 <= int(taskno) < len(get_user_tasks(email)))  ):
				print("Not valid input")
				taskno = input("Update task No. ")
			taskno = int(taskno) - 1
			new_done = input("progress so far(done_%) = ")
			file_as_dict[email][taskno][2] = new_done
			print("hey",file_as_dict[email]) 
			file = open("tasks.txt", "w")
			file.write(str(file_as_dict))
			file.close()
			update_screen(email)

		elif option == "-":
			file = open("tasks.txt", "r")
			file_as_dict = ast.literal_eval(file.read())
			file.close()
			taskno= input("Delete task No. ")
			while not (taskno.isnumeric() and (1 <= int(taskno) < len(get_user_tasks(email)))  ):
				print("Not valid input")
				taskno = input("Delete task No. ")
			taskno = int(taskno) - 1
			del file_as_dict[email][int(taskno)] # I used del instead of .pop() to overcome the need of index
			
			file = open("tasks.txt","w")
			file.write(str(file_as_dict))
			file.close()

			update_screen(email)
		elif option == "o":
			print(f"\nBye, {email} logged out successfully!")
			break

# Now lets use functional programming and fun

while True:
	choice = input("\nSign In[s] or Create new account[n]?\t --> exit[q]\n> ")
	if choice == "n":
		users_dict = check_data()
		sign_up()
	elif choice == "s":
		users_dict = check_data()
		sign_in()
	elif choice == "q":
		quit()
	else:
		print("Not valid input")

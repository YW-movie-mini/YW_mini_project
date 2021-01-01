import User
import Administrator

class WebSite:
	opt_list = ['나가기', '회원가입', '로그인']
	
	def __init__(self):
		admin = Administrator.Administrator('YW', '1234', '영우')
		self.users = {admin.id: admin}
		self.user = None
		self.movie_data = None
		self.load_data()

	def execute(self):
		self.show_start_page()

	def show_start_page(self):
		while True:
			if self.user is None:
				print("{:^80}".format("START PAGE"))
				self.print_menu(self.opt_list)
				opt = self.select_option()
				if opt == -1:
					continue
				elif opt == 1:
					self.sign_up()
				elif opt == 2:
					self.sign_in()
				elif opt == 3:
					self.sign_out()
				elif opt == 0:
					self.save_data()
					break
				else:
					self.out_of_range_error()
					continue
			elif isinstance(self.user, Administrator.Administrator):
				self.show_administrator_page()
			else:
				self.show_user_page()

	def show_administrator_page(self):
		while True:
			print("{:^80}".format("ADMINISTRATOR PAGE"))
			self.print_menu(Administrator.Administrator.opt_list)
			opt = self.select_option()
			if opt == -1:
				continue
			elif opt == 1:
				pass
			elif opt == 2:
				self.user.show_all_users(self.users)
			elif opt == 3:
				pass
			elif opt == 0:
				self.sign_out()
				break
			else:
				self.out_of_range_error()
				continue

	def show_user_page(self):
		while True:
			print("{:^80}".format("USER PAGE"))
			self.print_menu(User.User.opt_list)
			opt = self.select_option()
			if opt == -1:
				continue
			elif opt == 1:
				self.user.change_pwd()
			elif opt == 0:
				self.sign_out()
				break
			else:
				self.out_of_range_error()
				continue

	def show_movie_recommendation_by_관객수(self):
		pass

	def show_movie_recommendation_by_genre(self):
		pass

	def show_movie_recommendation_by_directors(self):
		pass

	def sign_up(self):
		while True:
			id = input("아이디를 입력해주세요(특수문자 X): ")
			if not id.isalnum():
				print("error: 특수문자가 들어있습니다.")
				continue
			if id.upper() in self.users:
				print("error: 동일한 아이디가 있습니다.")
				continue
			pwd = input("비밀번호를 입력해주세요(\\사용불가): ")
			if '\\' in pwd:
				print("error: \\ 문자가 들어있습니다.")
				continue
			name = input("이름을 입력해주세요: ")
			if not name.isalpha():
				print("error: 문자가 아닙니다.")
			
			menu = ["나가기", "완료", "다시하기"]
			self.print_menu(menu)
			while True:
				opt = self.select_option()
				if opt == -1:
					continue
				elif opt < 0 and opt >= len(menu):
					self.out_of_range_error()
					continue
				else:
					break
			if opt == 0:
				break
			elif opt == 2:
				continue

			new_user = User.User(id, pwd, name)
			self.users[id.upper()] = new_user
			print("")
			print("축하합니다 ", id, "님")
			print("회원가입 완료되었습니다.")
			break

	def sign_in(self):
		while True:
			id = input("아이디를 입력해주세요: ")
			pwd = input("비밀번호를 입력해주세요: ")
			if id.upper() not in self.users:
				print("없는 아이디 입니다.")
			else:
				if self.users[id.upper()].pwd != pwd:
					print("비밀번호가 틀립니다")
				else:
					print("로그인에 성공하였습니다.")
					self.user = self.users[id.upper()]
					break
			menu = ["나가기", "다시하기"]
			self.print_menu(menu)
			while True:
				opt = self.select_option()
				if opt == -1:
					continue
				elif opt < 0 and opt >= len(menu):
					self.out_of_range_error()
					continue
				else:
					break
			if opt == 0:
				break
		
	def sign_out(self):
		self.user = None
		print("로그아웃 되었습니다.")

	def print_menu(self, opt):
		print("")
		print("="*80)
		for i in range(1, len(opt)):
			if i % 5 == 1:
				print("")
			menu_str = str(i) + ". " + opt[i]
			print("{:^15}".format(menu_str), end='')
		menu_str = "0. " + opt[0]
		print("{:^15}".format(menu_str))
		print("")
		print("="*80)
		print("")
		pass

	def load_data(self):
		with open("data/user_data.txt", 'r') as f:
			line = f.readline()
			while line:
				line = line.split('\\')
				id = line[0]
				new_user = User.User(line[0], line[1], line[2])
				self.load_dictionary_data(line[3], new_user.movie)
				self.load_dictionary_data(line[4], new_user.genre)
				self.load_dictionary_data(line[5], new_user.director)
				self.users[id.upper()] = new_user
				line = f.readline()

	def load_dictionary_data(self, line, dict):
		if not line.startswith("N/A"):
			line = line.split(',')
			for i in range(len(line) - 1):
				key_value = line[i].split(':')
				key = key_value[0]
				value = float(key_value[1])
				dict[key] = value

	def save_data(self):
		with open("data/user_data.txt", 'w') as f:
			for id in self.users:
				if isinstance(self.users[id], User.User):
					f.write("{}\\{}\\{}\\".format(self.users[id].id, self.users[id].pwd, self.users[id].name))
					self.save_dictionary_data(f, self.users[id].movie)
					self.save_dictionary_data(f, self.users[id].genre)
					self.save_dictionary_data(f, self.users[id].director)
					f.write("\n")

	def save_dictionary_data(self, file, dict):
		if len(dict) == 0:
			file.write("N/A\\")
		else:
			for key, value in dict.items():
				file.write("{}:{}".format(key, value),end=',')
			file.write("\\")
	
	def select_option(self):
		try:
			opt = int(input("메뉴를 선택해주세요: "))
			return opt
		except:
			print("error: 숫자가 아닙니다.")
			print("다시 선택해주세요.")
			return -1

	def out_of_range_error(self):
		print("error: 범위를 벗어났습니다.")
		print("다시 선택해주세요.")
		print("")




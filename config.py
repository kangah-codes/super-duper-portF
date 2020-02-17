import random
import string

def gen_session():
	chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
	return ''.join(random.choice(chars) for _ in range(10))+'-'+''.join(random.choice(chars) for _ in range(10))

def gen_upload_id():
	chars = string.ascii_uppercase+string.ascii_lowercase+string.digits
	return ''.join(random.choice(chars) for _ in range(6))
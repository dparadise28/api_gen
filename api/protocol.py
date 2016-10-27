from utils import email_utils
import random, string

method_map = {
	"generate_code": lambda args: ''.join([random.choice(string.printable[:63]) for i in range(random.choice(range(6, 17)))]),
	"email_activation_code": email_utils.send_auth_code,
}
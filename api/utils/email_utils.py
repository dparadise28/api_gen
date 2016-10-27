from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from utils.image_utils import txt2img
import smtplib, validators

def validate(req):
	'''port for py lib validators used email format checking'''
	if validators.email(req['email']):
		return {"status": "Success", "error": ""}
	return {"status": "Failed", "error": "Could not communicate with the email provided. Please try again"}

def send_auth_code(req, strFrom = "ecomTesterMail6@gmail.com"):
	'''
		Static but works for now. Using a gmail test account 
		
		could be made more generic but there isnt much need for sending mass emails
		(easy enough to work with for now)
	'''
	# Create the root message and fill in the from, to, and subject headers
	msgRoot = MIMEMultipart('related')
	msgRoot['Subject'] = 'Thank you for joining!'
	msgRoot['From'] = strFrom
	msgRoot['To'] = req['email']

	# Encapsulate the plain and HTML versions of the message body in an
	# 'alternative' part, so message agents can decide which they want to display.
	msgAlternative = MIMEMultipart('alternative')
	msgRoot.attach(msgAlternative)

	msgText = MIMEText('This is the alternative plain text message.')
	msgAlternative.attach(msgText)

	# We reference the image in the IMG SRC attribute by the ID we give it below
	msgText = MIMEText('<b> <i>Here is your activation code:</i> </b> <br><img src="cid:image1"><br>Hope you find what your looking for!', 'html')
	msgAlternative.attach(msgText)

	# get image generated by text to image util and load it using MIMEImage
	msgImage = MIMEImage(txt2img(req['new_activation_code']))

	# Define the image's ID as referenced above
	msgImage.add_header('Content-ID', '<image1>')
	msgRoot.attach(msgImage)

	# Send the email (this example assumes SMTP authentication is required)
	server = smtplib.SMTP('smtp.gmail.com', 587)
	server.starttls()
	try:
		server.login("ecomTesterMail6@gmail.com", "6VFHGyjeE")
		server.sendmail(strFrom, req['email'], msgRoot.as_string())
		server.quit()
		return {'status': 'Success'}
	except:
		server.quit()
		return {"status": "Failed", "error": "Could not communicate with the email provided. Please try again"}

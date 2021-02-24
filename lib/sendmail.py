import utils
import sys

print "Sending Email Notification"
csvfile = sys.argv[1]
utils.send_mail(csvfile)
print "Email Notification sent"

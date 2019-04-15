import os
import sys
import argparse
import subprocess
import platform
import time
import datetime
import psutil

parser = argparse.ArgumentParser(description="Manage some services!")
parser.add_argument('--service-names', nargs='+', required=True, help="A list of services to be managed!")
parser.add_argument('--action', nargs=1, required=True, choices=('start', 'stop', 'restart'), help="Action to be taken against")
parser.add_argument('--location', nargs=1, required=False, default='/etc/init.d/', help="The location of the services!")
args = parser.parse_args()
system=""

def linux_sample_data():
    metaData = parser.parse_args() + "\n"

    if os.getenv('USER') != 'root':
        print("You must run the script as root!")
        raise SystemExit

    # /etc/init.d/apache
    for service in args.service_names:
        print("Working on: {}".format(service))

    if os.path.isfile(os.path.join(args.location, service)):
        print("Checking the status of the service!")
        Command = """ $(ps -ef | grep -v grep | grep {} | wc -1) """.format(service)

        ServiceStatus = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        metaData = ServiceStatus + " \n"

        OK, ERR = ServiceStatus.communicate()

        servicestate = 'start'
        if '0:not found' in OK.replace('\r\n', ''):
            servicestate = 'stop'

        if args.action == servicestate:
            print("Incompatibe state, skipping!")

        Command = os.path.join(args.location, service)
        print('Trying to perform action: {}'.format(Command))

        ActionResult = subprocess.Popen(Command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        metaData = ActionResult + " \n"

        OK, ERR = ActionResult.communicate()

        if ERR is None:
            print("OK: The service was successfully {}ed!".format(args.action[0]))
        else:
            print("ERROR: changing service state to: {}".format(ERR))
    else:
        print("The service's file could not be found on: {}, skipping!".format(os.path.join(args.location, service)))
    return metaData


def windows_sample_data():


    def getService(name):

        service = None
        try:
            service = psutil.win_service_get(name)
            service = service.as_dict()
        except Exception as ex:
            print
            str(ex)

        return service

    service = getService('myservice')

    print
    service

    if service:

        print
        "service found"
    else:

        print
        "service not found"

    if service and service['status'] == 'running':

        print
        "service is running"
    else:

        print
        "service is not running"


time_p = input("Please choose time period between Logfile sample: ")

service_list_file = open("serviceList", "w")
status_log_file = open("Status_Log.txt", "w")
old_sample = ""
new_sample = ""
sample_data = ""
modified_since = datetime.datetime.now()

if   (system == "Linux"):
            sample_data = linux_sample_data()
elif (system == 'Windows'):
            sample_data = windows_sample_data
else:
            raise Exception("unsupported platform {}".format(system))

old_sample = sample_data()
while 1:
            new_sample = sample_data()
            if (old_sample != new_sample):
                print('Log file has been modified since ', modified_since)
                status_log_file.write(new_sample)
                modified_since = datetime.datetime.now()
                old_sample = new_sample

            service_list_file.write(new_sample)  # writing to service list file
            time.sleep(time_p)



def manual(system):
        if system == "Linux": pass
        elif system == "Windows": pass
        else: raise Exception("unsupported platform {}".format(system))


if __name__ == "__main__":
	state = input("Please choose mode : Monitor / Manual / Quit").lower()
	system = platform.system()
	
	if state == "monitor":
		monitor(system)

	elif state == "manual":
	    manual(system)

	elif state == "quit":
	    print("Quitting from the program")
	    exit()

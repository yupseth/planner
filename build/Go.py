import os
import json
import paramiko
import webbrowser
from getpass import getpass
from urllib.parse import urlparse, parse_qs
from http.server import HTTPServer, BaseHTTPRequestHandler, SimpleHTTPRequestHandler


PORT = 8000
INDEXFILE = 'index.html'

class FakeModReWriteHandle(SimpleHTTPRequestHandler):

    def do_GET(self):

        # Parse query data to find out what was requested
        parsedParams = urlparse(self.path)

        # See if the file requested exists
        if os.access('.' + os.sep + parsedParams.path, os.R_OK):
            # File exists, serve it up
            SimpleHTTPRequestHandler.do_GET(self)

        # send index.html, but don't redirect
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        with open(INDEXFILE, 'rb') as fin:
            self.copyfile(fin, self.wfile)


def HOMEserver():
    httpd = HTTPServer(("0.0.0.0", 3000), FakeModReWriteHandle)
    print("Home Server run at port", 3000)
    httpd.serve_forever()



def startHomeServer():
    try:
        HOMEserver()
    except OSError:
        print("\nError check if the PORT:[%s] address is already in use!\n", 3000)
    except KeyboardInterrupt:
        print("\nBye Server Down!\n")




initialized = False
try:
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print('Hello, working directory set to: ' + str(script_dir))
    remote_json_path = os.path.join(script_dir, 'Connection.json')
    with open(remote_json_path, 'r') as f:
        config = json.load(f)
    host = config['host']
    port = config['port']
    username = config['username']
    print('Connecting to: ' + host + ':' + str(port) + ' - as: ' + username)
    password = getpass("Password: ")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        ssh.close()
        initialized = True
        print('Connection test successful.')
    except:
        print('Connection test failure.')
except:
    print('Unable to retrieve Connection.json file data, please type in the connection details.')
    host = input(" Host: ")
    try:
        port = int(input("Port: "))
    except:
        print('Wrong port entry, setting to default port 22.')
        port = 22
    username = input(" Username: ")
    print('Connecting to: ' + host + ':' + str(port) + ' - as: ' + username)
    password = getpass("Password: ")
    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(host, port, username, password)
        ssh.close()
        initialized = True
        print('Connection test successful.')
    except:
        print('Connection test failure.')


def get_month_data(month, year):
    remote_script_path = '/opt/planner/getcalendar.py'
    try:
        # Command with command-line arguments
        command = f'python {remote_script_path} {month} {year}'
        # Connect to the remote server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, password)
            # Execute the command remotely
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            ssh.close()
            if error:
                # Close the SSH connection
                return(f"Error occurred: {error}")
            else:
                # Close the SSH connection
                return(output)
        except:
            try:
                ssh.close()
            except:
                pass
            return('Unable to connect to remote server.')
    except:
        return('Unable to connect to remote server.')


def get_users_data(month, year):
    remote_script_path = '/opt/planner/getusersdata.py'
    try:
        # Command with command-line arguments
        command = f'python {remote_script_path} {month} {year}'
        print (command)
        # Connect to the remote server
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            ssh.connect(host, port, username, password)
            # Execute the command remotely
            stdin, stdout, stderr = ssh.exec_command(command)
            output = stdout.read().decode()
            error = stderr.read().decode()
            ssh.close()
            if error:
                # Close the SSH connection
                return(f"Error occurred: {error}")
            else:
                # Close the SSH connection
                return(output)
        except:
            try:
                ssh.close()
            except:
                pass
            return('Unable to connect to remote server.')
    except:
        return('Unable to connect to remote server.')


class customRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/api/calendar'):
            try:
                query_components = parse_qs(urlparse(self.path).query)
                month = query_components.get('month', [])[0]
                year = query_components.get('year', [])[0]
                if month and year:
                    data = get_month_data(month, year) # Pass both month and year to the get_month_data function
                    print(data)
                else:
                    # Handle case when either month or year is missing
                    data = {"error": "Month and year parameters are required."}

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Bad Calendar Request :( - sample usage: /api/calendar?month=5&year=2023'.encode())
                print(f'Error: {e}')


        elif self.path.startswith('/api/getusers'):
            try:
                query_components = parse_qs(urlparse(self.path).query)
                month = query_components.get('month', [])[0]
                year = query_components.get('year', [])[0]
                if month and year:
                    data = get_users_data(month, year) # Pass both month and year to the get_month_data function
                else:
                    # Handle case when either month or year is missing
                    data = {"error": "User, Month and Year parameters are required."}
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps(data).encode())
            except Exception as e:
                self.send_response(400)
                self.send_header('Content-type', 'text/plain')
                self.end_headers()
                self.wfile.write('Bad Users Request :( - sample usage: /api/getusers?month=5&year=2023'.encode())
                print(f'Error: {e}')
        else:
            self.send_error(404)


def APIserver():
    httpd = HTTPServer(("0.0.0.0", 8080), customRequestHandler)
    print("API Server run at port", 8080)
    httpd.serve_forever()


def startAPIServer():
    try:
        APIserver()
    except OSError:
        print("\nError check if the PORT:[%s] address is already in use!\n", 8080)
    except KeyboardInterrupt:
        print("\nBye Server Down!\n")



import threading

t1 = threading.Thread(target=startHomeServer)
t2 = threading.Thread(target=startAPIServer)

t1.start()
t2.start()

t1.join()
t2.join()

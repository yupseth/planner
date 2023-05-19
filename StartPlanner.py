import os
import json
import paramiko
import webbrowser
from getpass import getpass
from urllib.parse import urlparse, parse_qs
from http.server import BaseHTTPRequestHandler, HTTPServer


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

    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()

    def do_GET(self):
        if self.path.startswith('/planner'):
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            # Open the front-end HTML file and send its contents
            try:
                FRONT_HOME = os.path.dirname(os.path.abspath(__file__))
                print(FRONT_HOME)
                FRONT_END_DIR = os.path.join(FRONT_HOME, 'public\index.html')
                print('Loaded app: ' + FRONT_END_DIR)
                with open(FRONT_END_DIR, 'r') as f:
                    self.wfile.write(f.read().encode())
            except:
                print('Failed to fetch frontend.')

        elif self.path.startswith('/api/calendar'):
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


if initialized:
    server = HTTPServer(('localhost', 3000), customRequestHandler)
    print('Started local API host.')
    #webbrowser.open('http://localhost/home')
    #print('Started localhost browser.')
    server.serve_forever()
else:
    print('Failed to initialize connection to remote server.')

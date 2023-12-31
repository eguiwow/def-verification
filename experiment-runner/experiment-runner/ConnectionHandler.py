# This module is an adaptation of another one created by @galexad and can be found in https://github.com/galexad/experiment-runner/

from ProgressManager.Output.OutputProcedure import OutputProcedure as output

import os
import paramiko

class ConnectionHandler:
    def __init__(self, host_name):
        self.host_name = host_name

    def execute_remote_command(self, command, command_name):
        con = self.connect_to_host()
        output.console_log(command_name)
        req, out, err = con.exec_command(command)
        err = err.read()

        if err != b'':
            output.console_log(err)
            return 0

        output.console_log(f"'{command_name}' command successfully executed")
        return 1

    def connect_to_host(self):
        host, username, password = self.get_credentials()
        # connect to server
        con = paramiko.SSHClient()
        con.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        con.connect(host, username = username, password = password)
        output.console_log(f"Connection successful to {self.host_name}")

        return con

    def get_credentials(self):
        # declare credentials
        host_name = self.host_name
        host = os.getenv(f"{host_name}_H")
        username = os.getenv(f"{host_name}_U")
        password = os.getenv(f"{host_name}_P")

        if not password or not username or not host:
            raise Exception('No environment variables set for credentials')

        return host, username, password

    def get_containers_count(self):
        conn = self.connect_to_host()
        _, _, password = self.get_credentials()
        _, number_of_containers_buf, err = conn.exec_command(f" echo {password} | sudo -S docker ps | wc -l")
        number_of_containers = int(number_of_containers_buf.read().strip())
        output.console_log(f"Found {number_of_containers} running after sleeping")

        return number_of_containers




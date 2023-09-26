import subprocess

def execute_command(command, text):
    try:
        output = subprocess.check_output(command, shell=True, universal_newlines=True)
        return text in output
    except (subprocess.CalledProcessError, FileNotFoundError):
        return False
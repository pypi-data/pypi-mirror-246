import subprocess
import sys
from colorama import Fore, Style

def check_installation(program_name, check_command):
    result = subprocess.run(check_command, capture_output=True, shell=True, text=True)
    output = result.stdout.strip() if result.stdout.strip() else result.stderr.strip()
    if "not found" in output:
        print(f"{Fore.RED}✗{Style.RESET_ALL} Could not detect {program_name} version")
        return False
    else:
        print(f"{Fore.GREEN}✓{Style.RESET_ALL} {program_name} version detected: {output}")
        return True

def check_installations():
    programs = [
        {"name": "Python", "command": "python --version"},
        {"name": "pip", "command": "pip --version"},
        {"name": "Robot Framework", "command": "robot --version"},
        {"name": "Node.js", "command": "node --version"},  # Adicionado verificação do Node.js
    ]
    exit_code = 0
    for program in programs:
        if not check_installation(program["name"], program["command"]):
            exit_code = 1
    if exit_code == 1:
        sys.exit(1)
from automation_fw_setup.check_installations import check_installations
from automation_fw_setup.create_project_folder import create_project_folder
from automation_fw_setup.create_virtual_env import create_virtual_env
from automation_fw_setup.ask_test_framework import ask_test_framework
from automation_fw_setup.ask_target_platform import ask_target_platform
from automation_fw_setup.clone_repository import clone_repository
from colorama import Fore, Style

def main():
    framework_choice = ask_test_framework()

    if framework_choice == 'Robot Framework':
        platform_choice = ask_target_platform()
        if platform_choice == 'Web':
            check_installations()
            project_name = create_project_folder()
            clone_repository(project_name)
            create_virtual_env(project_name)
        else:
            print(f"{Fore.RED}✗{Style.RESET_ALL} The selected platform is not yet supported.")
    else:
        print(f"{Fore.RED}✗{Style.RESET_ALL} The selected framework is not yet supported.")

if __name__ == "__main__":
    main()
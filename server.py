import importlib.util
import subprocess
import shutil
import os


# function to check and install Gunicorn
def check_and_install_gunicorn():
    package_name = "gunicorn"
    package_installed = importlib.util.find_spec(package_name) is not None

    if package_installed:
        print(f"{package_name} is installed")
    else:
        print(f"{package_name} is not installed")
        print(f"Installing {package_name}...")
        subprocess.call(["pip", "install", package_name])


# Function to start Gunicorn server
def start_gunicorn_server():
    app_name = "app:app"

    print(f"Starting Gunicorn server...")
    subprocess.Popen(["gunicorn", "-b","127.0.0.1:8000", app_name])



# Function to check if Nginx is installed
def check_and_install_nginx():
    nginx_path = shutil.which("nginx")

    if nginx_path:
        print("Nginx is installed at {nginx_path}")
    else:
        print("Nginx is not installed. Installing Now ...")
        try:
            subprocess.call(["sudo", "apt-get", "update"])
            subprocess.call(["sudo", "apt-get", "install", "-y", "nginx"])
            print("Nginx installed successfully")
        except Exception as e:
            print(f"Error installing Nginx: {e}")

# function to check if a nginx site configuration file exists
def check_and_create_nginx_site_config(site_name,content):
    site_config_path = f"/etc/nginx/sites-available/{site_name}"

    if os.path.exists(site_config_path):
        print(f"Site configuration file exists at {site_config_path}")
    else:
        print(f"Site configuration file does not exist at {site_config_path}")

        # Create a new site configuration file
        try:
            with open(site_config_path, "w") as file:
                file.write(content)
            print(f"Site configuration file created at {site_config_path}")

            # Create a symbolic link to the sites-enabled directory
            symlink_path = f"/etc/nginx/sites-enabled/{site_name}"
            os.symlink(site_config_path, symlink_path)
            print(f"Symbolic link created at {symlink_path}")

            # Restart Nginx
            subprocess.call(["sudo", "systemctl", "reload", "nginx"])
            print("Nginx restarted successfully")
        
        except Exception as e:
            print(f"Error creating site configuration file: {e}")

site_config_content = """
server {
    listen 80;
    server_name 0.0.0.0;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }

    # Optionally serve static files
    # location /static/ {
    #     root /path/to/static/files;
    # }
}
"""




site_config_name = "flask_app"

check_and_install_gunicorn()
start_gunicorn_server()
check_and_install_nginx()
check_and_create_nginx_site_config(site_config_name,site_config_content)
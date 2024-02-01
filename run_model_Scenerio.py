import paramiko,boto3
import time,os
        
def run_ssh_commands(hostname, username, private_key_path, command,output_file1,output_file2,desired_folder):
    try:
        # Create an SSH client instance
        ssh_client = paramiko.SSHClient()

        # Automatically add the server's host key (this is insecure and should not be used in production)
        ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Load the private key (you may need to adjust the key permissions)
        private_key = paramiko.RSAKey.from_private_key_file(private_key_path)

        # Connect to the EC2 instance
        ssh_client.connect(hostname=hostname, username=username, pkey=private_key)

        # Execute the command and capture the output
        stdin, stdout, stderr = ssh_client.exec_command(command)

        # Print the command output
        print("Command output:")
        # print(stdout.read().decode())
        
        # # Print the command error (if any)
        # print(stderr.read().decode())
        print("Command END")
        ssh_client.close()
        timeout = time.time() + 3600  # Set a timeout for 30 minutes
        while time.time() < timeout:
            if output_file1 in os.listdir(desired_folder) and output_file2 in os.listdir(desired_folder):
                print("Output files are available!")
                break
            time.sleep(60)  # Check every 5 minutes

        else:
            print("Timeout reached. Output files were not found.")
      
    except paramiko.AuthenticationException:
        print("Authentication failed. Please check your credentials.")
    except paramiko.SSHException as e:
        print("Error occurred while connecting to the server:", e)
            


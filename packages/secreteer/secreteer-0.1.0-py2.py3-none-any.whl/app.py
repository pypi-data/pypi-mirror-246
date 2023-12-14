'''
A neat little secrets manager.
'''



from cryptography.fernet import Fernet
import yaml
from getpass import getpass
import os
import click

if not os.getenv("SECRETS_KEY"):
   key = Fernet.generate_key()
   print(f"Keep this key safe, you will need it to access your secrets. export SECRETS_KEY={key}")
else:
   key = os.getenv("SECRETS_KEY")
cipher_suite = Fernet(key)

@click.group()
def cli():
    pass

@cli.command()
@click.argument('secret_name')
@click.argument('secret_body', required=False)
def encrypt(secret_name, secret_body):
    if not secret_body:
        secret_body = getpass("Secret Body: ")
    try:
        # Encrypt the secret
        cipher_text = cipher_suite.encrypt(secret_body.encode())

        # Store the encrypted secret in a YAML file
        secrets = {}
        with open("secrets.yaml", "r") as file:
            secrets = yaml.safe_load(file)
        secrets[secret_name] = cipher_text.decode()
        with open("secrets.yaml", "w") as file:
            yaml.dump(secrets, file)
        print("Secret encrypted and stored successfully!")
    except Exception as e:
        print(f"Error encrypting and storing secret: {str(e)}")

@cli.command()
@click.argument('secret_name')
def decrypt(secret_name):
    try:
        # Retrieve the secret from the YAML file
        with open("secrets.yaml", "r") as file:
            secrets = yaml.safe_load(file)

        # Decrypt the secret
        decrypted_secret = cipher_suite.decrypt(secrets[secret_name].encode()).decode()

        print(f"{secret_name}: {decrypted_secret}")
    except KeyError:
        print(f"Secret '{secret_name}' not found in the YAML file.")
    except Exception as e:
        print(f"Error decrypting secret: {str(e)}")

if __name__ == '__main__':
    cli()

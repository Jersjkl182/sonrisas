# hashed_password_generator.py

from werkzeug.security import generate_password_hash

def generate_hash(password):
    """
    Generates a hash for the given password using Werkzeug's security module.
    """
    return generate_password_hash(password)

if __name__ == '__main__':
    # Define the password you want to hash
    plain_password = "jerson" # ¡Cambia esto por la contraseña que quieras usar!

    # Generate the hashed password
    hashed_pass = generate_hash(plain_password)

    # Print the hashed password
    print(f"La contraseña plana es: '{plain_password}'")
    print(f"La contraseña hasheada es: '{hashed_pass}'")
    print("\nCopia la cadena que empieza con 'pbkdf2:sha256:' y pégala en tu base de datos.")
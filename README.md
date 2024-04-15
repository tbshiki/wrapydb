# Wrapydb

## Configuration

To use the `WrapydbConnector`, you need to provide connection settings that include both SSH and database connection details. Here's what you need to configure:

### `connection_settings` dictionary format:

The `connection_settings` dictionary should include the following keys:

- `ssh_host`: The hostname or IP address of the SSH server.
- `ssh_port`: The port number on which the SSH server is running (usually 22).
- `ssh_username`: Your SSH username.
- `ssh_private_key`: The path to your private SSH key (e.g., `~/.ssh/id_rsa`).
- `ssh_private_key_password`: The password for your SSH key (if applicable).

For the database connection:

- `db_host`: The hostname or IP address of the database server accessible via the SSH tunnel.
- `db_port`: The port number on which the database server is running.
- `db_user`: Your database username.
- `db_password`: Your database password.
- `db_name`: The name of the database to connect to.

### Example Usage

Here is an example of how you can set up the `connection_settings` and initialize the `WrapydbConnector`:

```
python
connection_settings = {
    "ssh_host": "example.sshhost.com",
    "ssh_port": 22,
    "ssh_username": "sshuser",
    "ssh_private_key": "/path/to/private/key",
    "ssh_private_key_password": "yourkeypassword",
    "db_host": "127.0.0.1",
    "db_port": 3306,
    "db_user": "dbuser",
    "db_password": "dbpassword",
    "db_name": "yourdbname"
}

connector = WrapydbConnector(connection_settings)
```

[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

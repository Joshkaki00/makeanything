# SSH Basics

## What is SSH

SSH (Secure Shell) is a network protocol that allows you to connect to a remote computer securely. It provides a secure channel over an unsecured network by using encryption. SSH is commonly used to:

- Log in to remote servers and execute commands
- Transfer files between machines securely (using SCP or SFTP)
- Port forward connections to access services on remote machines
- Access version control systems like Git

SSH uses public key cryptography for authentication, which is more secure than passwords.

## SSH Key Pair Setup

SSH uses a pair of cryptographic keys:
- **Private key** — Keep this secret on your local machine; it's your identity
- **Public key** — Share this with servers you want to access

To generate an SSH key pair on your local machine:

```bash
ssh-keygen -t ed25519 -C "your_email@example.com"
```

This creates two files:
- `~/.ssh/id_ed25519` — Your private key (keep it secret!)
- `~/.ssh/id_ed25519.pub` — Your public key (safe to share)

You'll be prompted to enter a passphrase to protect your private key. Choose a strong passphrase.

## Connecting to a Remote Server

To connect to a remote server via SSH:

```bash
ssh username@remote-host
```

Replace `username` with your username on the remote server and `remote-host` with the IP address or domain name of the server.

For example:
```bash
ssh ubuntu@192.168.1.100
```

The first time you connect, SSH will ask if you trust the remote host's key fingerprint. Type `yes` to proceed.

## SSH Configuration

You can create a configuration file to make connecting easier. Create or edit `~/.ssh/config`:

```
Host myserver
  HostName 192.168.1.100
  User ubuntu
  IdentityFile ~/.ssh/id_ed25519
  Port 22
```

Now you can connect with just:
```bash
ssh myserver
```

## Adding Your Public Key to a Server

To allow password-less login, add your public key to the remote server:

```bash
ssh-copy-id -i ~/.ssh/id_ed25519.pub username@remote-host
```

This adds your public key to the `~/.ssh/authorized_keys` file on the remote server. Now you can log in without entering a password (assuming you're using ssh-agent to manage your passphrase).

## SSH Security Best Practices

- **Keep your private key secure** — Never share your private key or commit it to version control
- **Use a strong passphrase** — Protect your private key with a passphrase
- **Disable password authentication** — Once you have key-based auth working, disable password login on servers
- **Use SSH agents** — Use `ssh-agent` to manage your passphrases so you don't type them repeatedly
- **Limit key access** — Regularly review `authorized_keys` and remove old or unnecessary keys
- **Use non-standard ports** — Consider changing SSH from port 22 to a different port to reduce automated attacks

## Executing Remote Commands

You can run commands on a remote server without opening an interactive shell:

```bash
ssh ubuntu@myserver.com "sudo systemctl restart nginx"
```

This is useful in scripts and automation.

## File Transfer with SCP

To copy files securely between local and remote machines:

```bash
# Copy file from local to remote
scp /path/to/local/file username@remote-host:/path/on/remote

# Copy file from remote to local
scp username@remote-host:/path/on/remote/file /path/to/local/
```

For example:
```bash
scp app.py ubuntu@myserver.com:~/
```

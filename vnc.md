To share the same GNOME session across multiple Ubuntu VNC viewers, you can use the `x11-display` option in the VNC server configuration. Here's how to set it up:

1. **Install the VNC server:**

First, install the VNC server on your Ubuntu system:

```bash
sudo apt install tightvncserver
```

2. **Create a GNOME session script:**

Create a new script in your home directory, e.g., `~/.vnc/xstartup`, with the following content:

```bash
#!/bin/sh

gnome-session --session=mysession &
DISPLAY=:1
exec /usr/bin/X11 /usr/bin/XtightVNC -nopw -display :1 -depth 24 -rfbport 5901 -auth none
```

Replace `mysession` with the desired name for your GNOME session. Make sure to give the script the correct permissions:

```bash
chmod +x ~/.vnc/xstartup
```

3. **Configure the VNC server:**

Update the VNC server configuration file, usually located at `/etc/init.d/tightvncserver`, and add the following lines at the end of the file:

```bash
VNCARGS="-nopw -display :1 -depth 24 -rfbport 5901 -auth none -xstartup /home/yourusername/.vnc/xstartup"
```

Replace `yourusername` with your actual username.

4. **Start the VNC server:**

Start the VNC server with the following command:

```bash
sudo systemctl start tightvncserver
```

5. **Access the shared GNOME session:**

Now, you can access the shared GNOME session using a VNC viewer like TigerVNC or Remmina. Connect to the VNC server using the following details:

- Host: `<VNC_SERVER_IP_ADDRESS>`
- Port: `5901`
- Password: (Leave blank if you haven't set one)

After connecting, you should see the same GNOME session across multiple VNC viewers.

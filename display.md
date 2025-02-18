To configure a dummy display in Xorg, you can use the `xserver-xorg-video-dummy` driver. This is particularly useful for headless setups, remote access via VNC, or when no physical monitor is connected. Below is an example of how to set up an `xorg.conf` file for a dummy display.

### **Steps to Configure a Dummy Display**

1. **Install the Dummy Driver**:
   Ensure you have the `xserver-xorg-video-dummy` package installed. On Debian-based systems, you can install it using:
   ```bash
   sudo apt-get install xserver-xorg-video-dummy
   ```

2. **Create or Modify the Xorg Configuration File**:
   Create a new configuration file for the dummy display at `/etc/X11/xorg.conf` or `/usr/share/X11/xorg.conf.d/99-dummy.conf`. If an existing `xorg.conf` file exists, back it up first.

3. **Example Configuration**:
   Use the following configuration as a template:
   ```plaintext
   Section "Device"
       Identifier  "DummyDevice"
       Driver      "dummy"
       Option      "IgnoreEDID" "true"
       Option      "NoDDC" "true"
       VideoRam    256000
   EndSection

   Section "Monitor"
       Identifier  "DummyMonitor"
       HorizSync   28.0-80.0
       VertRefresh 48.0-75.0
       Modeline    "1920x1080" 148.50 1920 2008 2052 2200 1080 1084 1089 1125 +HSync +VSync
   EndSection

   Section "Screen"
       Identifier  "DummyScreen"
       Device      "DummyDevice"
       Monitor     "DummyMonitor"
       DefaultDepth 24
       SubSection "Display"
           Depth     24
           Modes     "1920x1080"
           Virtual   1920 1080
       EndSubSection
   EndSection

   Section "ServerLayout"
       Identifier  "DummyLayout"
       Screen      "DummyScreen"
   EndSection
   ```

4. **Restart X Server**:
   After saving the configuration file, restart the X server to apply changes:
   ```bash
   sudo systemctl restart gdm3    # For GNOME (or replace with your display manager)
   ```

5. **Verify the Dummy Display**:
   You can check if the dummy display is active by running:
   ```bash
   xrandr --listmonitors
   ```

### **Additional Notes**
- The `Modeline` specifies the resolution and refresh rate of the dummy display. You can generate custom modelines using tools like `cvt` or online modeline calculators.
- If you're using this setup for remote access (e.g., VNC), ensure your VNC server is configured to use the dummy display.
- For dynamic setups where you want the dummy display to activate only when no physical monitor is connected, scripting solutions may be required to monitor connection states and modify configurations dynamically[1][2][3].

This setup works on most Linux distributions with X11 and provides flexibility for headless or mixed-display environments.

Citations:
[1] https://superuser.com/questions/1774401/how-to-create-a-hotpluggable-dummy-monitor-in-x11
[2] https://askubuntu.com/questions/1231608/how-do-i-add-a-xserver-xorg-video-dummy-display-to-mirror-the-physical-display
[3] https://forums.developer.nvidia.com/t/low-resolution-dummy-monitor-for-vnc-when-displayport-unplugged/263892
[4] https://www.reddit.com/r/linuxquestions/comments/zgtrj3/is_it_possible_to_configure_xorg_to_set_a/
[5] http://cosmolinux.no-ip.org/raconetlinux2/dummy_radeon_nvidia.html
[6] https://askubuntu.com/questions/1396903/dummy-monitor-in-21-10
[7] https://unix.stackexchange.com/questions/756456/redhat-8-and-xorg-conf-and-x11-xorg-drv-dummy-and-console-monitor-and-vnc
[8] https://gist.github.com/terwey/1e49383e7cb2114e98a034558a5de682
[9] https://unix.stackexchange.com/questions/585069/unable-to-add-a-virtual-display-to-xorg
[10] https://bbs.archlinux.org/viewtopic.php?id=297503
[11] https://forums.developer.nvidia.com/t/cant-overclock-memory-using-intel-integrated-as-display-dummy-xorg-entry-needed/51857
[12] https://www.linuxquestions.org/questions/linux-software-2/can't-figure-out-how-to-convince-xorg-to-create-a-fake-virtual-screen-to-the-left-of-my-real-screen-4175681290/
[13] https://unix.stackexchange.com/questions/631624/switch-between-dummy-xserver-and-a-real-monitor
[14] https://superuser.com/questions/438699/adding-dual-monitor-settings-to-xorg-conf-d
[15] https://bbs.archlinux.org/viewtopic.php?id=246284
[16] https://gist.github.com/divinity76/ce210b5dbcd9ea7d0585ac403caef577
[17] https://discuss.kde.org/t/multihead-with-xorg-dummy-screen/15823
[18] https://superuser.com/questions/1779799/xrandr-cant-open-display-trying-to-add-fake-display
[19] https://wiki.archlinux.org/title/Xorg
[20] https://gist.github.com/vadimstasiev/b9ce8e78a35dac819d54c383db383423

---
Answer from Perplexity: pplx.ai/share

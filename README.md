# dimscreen

Python script to set brightness of ODROID M1 (original) display. 

/etc/systemd/system/dim-screen.service
```
[Unit]
Description=Dim screen when idle
After=multi-user.target

[Service]
Type=simple
ExecStart=su tomcat -c "/home/tomcat/Development/dimscreen/dimscreen.py backlight 30 0 255" &

[Install]
WantedBy=multi-user.target
```

/etc/systemd/system/dim-screen.timer
```
[Unit]
Description=Timer for dim screen after boot

[Timer]
OnBootSec=1min
Unit=dim-screen.service

[Install]
WantedBy=multi-user.target
```

# MultiContainer Desktop Environment

Initially this program was part of larger project, which is now closed, so I decided to publish some useful tools to open source.

MCDE is not production-ready itself. If you decide to use it without modification, beware of some security issues, so VPN/Firewall is highly recommended!

### Description
MCDE allows using multiple separated desktop environments on same host
* Full-featured LXDE with desktop, taskbar, some default apps including browser, can use any GUI-based linux software
* Different external IP's for each container through SOCKS5 proxy. Routing is transparent for underlying apps, but works only for TCP
* Browser-based control panel with VNC throughput and basic power control. Also works on mobile devices
* Command-line-based container creation helper — deploying new one takes a few seconds
* Low resource consumption (compared to virtual machines)

Control panel is [here](https://github.com/Egor3f/mcde-frontend)

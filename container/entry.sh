#!/bin/bash

if [[ -n $MCDE_PROXY_HOST ]]; then
  echo "
  base {
   log_debug = off;
   log_info = off;
   log = \"file:/var/log/redsocks.log\";
   daemon = on;
   user = redsocks;
   group = redsocks;
   redirector = iptables;
  }
  redsocks {
   local_ip = 127.0.0.1;
   local_port = 12345;
   ip = $MCDE_PROXY_HOST;
   port = $MCDE_PROXY_PORT;
   type = socks5;
  }
  " > /etc/redsocks.conf

  service redsocks restart

  iptables -t nat -N REDSOCKS
  iptables -t nat -A OUTPUT -p tcp -j REDSOCKS
  iptables -t nat -A REDSOCKS -d 0.0.0.0/8 -j RETURN
  iptables -t nat -A REDSOCKS -d 10.0.0.0/8 -j RETURN
  iptables -t nat -A REDSOCKS -d 100.64.0.0/10 -j RETURN
  iptables -t nat -A REDSOCKS -d 127.0.0.0/8 -j RETURN
  iptables -t nat -A REDSOCKS -d 169.254.0.0/16 -j RETURN
  iptables -t nat -A REDSOCKS -d 172.16.0.0/12 -j RETURN
  iptables -t nat -A REDSOCKS -d 192.168.0.0/16 -j RETURN
  iptables -t nat -A REDSOCKS -d 198.18.0.0/15 -j RETURN
  iptables -t nat -A REDSOCKS -d 224.0.0.0/4 -j RETURN
  iptables -t nat -A REDSOCKS -d 240.0.0.0/4 -j RETURN
  iptables -t nat -A REDSOCKS -d $MCDE_PROXY_HOST -j RETURN
  iptables -t nat -A REDSOCKS -p tcp -j REDIRECT --to-port 12345
fi

/startup.sh

# smp_affinity
A script to set and display affinity of IRQs and Processes


## Features

smp_affinity is a perl script that displays processor affinity in a human readable way.

### Requirements

The script has only 2 requirements:
- Linux Kernel
- perl (should be standard among all distributions)

No other module is needed.

To display and set IRQs affinity, the script must be run as root.

## Examples

### TL;DR

- Show affinity of all process with details: `smp_affinity -s`
- Show process that have non-default affinity: `smp_affinity -s -d`
- Show process that have consumed more than 30% CPU in average of their lifespan: `smp_affinity --pctcpu=30%`
- Set affinity of process 1234 to CPUs 0,1,2 and 5: `smp_affinity -P 1234 -C 0-2,5`


### Display

In its simplest form, `smp_affinity` will show all processes (and thread) affinity.

The threads are padded with 4 spaces under their main process (thread-leader) and shown
with their custom name (if one is set).

<pre>
$ ./smp_affinity
ID     Owner    Description                                                                                      0  1  2  3  4  5  6  7 
1      root     init [3]                                                                                         X  X  X  X  X  X  X  X 
673    adrien   /usr/local/Aventail/AvConnect --app-dir=/home/adrien/.sonicwall -p40255                          X  X  X  X  X  X  X  X 
5564   root     /sbin/udevd                                                                                      X  X  X  X  X  X  X  X 
6636   messageb /usr/bin/dbus-daemon --system                                                                    X  X  X  X  X  X  X  X 
6917   root     supervising syslog-ng                                                                            X  X  X  X  X  X  X  X 
6952   dnsmasq  /usr/sbin/dnsmasq -x /var/run/dnsmasq.pid --user=dnsmasq --group=dnsmasq                         X  X  X  X  X  X  X  X 
6985   root     /usr/sbin/chronyd -f /etc/chrony/chrony.conf                                                     X  X  X  X  X  X  X  X 
7415   root     /usr/sbin/sshd -o PidFile=/run/sshd.pid -f /etc/ssh/sshd_config                                  X  X  X  X  X  X  X  X 
7610   root     /usr/sbin/console-kit-daemon --no-daemon                                                         X  X  X  X  X  X  X  X 
7611   root         gmain                                                                                        X  X  X  X  X  X  X  X 
7613   root         gdbus                                                                                        X  X  X  X  X  X  X  X 
7614   root         console-kit-dae                                                                              X  X  X  X  X  X  X  X 
7617   root         vt_thread_start                                                                              X  X  X  X  X  X  X  X 
</pre>

If you add the `-s|--statistics` option, many 6 more columns will be shown:
  - Scheduling class: TS (Time Sharing, default) RR (Round Robin, RealTime) FF (FIFO, RealTime), IDL (IDLE).
  - RealTime Priority
  - Last CPU where application has run
  - %CPU Consumed during the application lifespan
  - %MEM Consumed currently (Resident size, the real one)
  - State: R (running) S (interruptible wait) D (uninterruptible wait) Z (zombie) 

<pre>
$ ./smp_affinity -s | head
ID     Owner    Description                                                                                      0  1  2  3  4  5  6  7 
1      root     TS  -  0  0.0  0.0  S init [3]                                                                   X  X  X  X  X  X  X  X 
673    adrien   TS  -  7  0.0  0.0  S /usr/local/Aventail/AvConnect --app-dir=/home/adrien/.sonicwall -p40255    X  X  X  X  X  X  X  X 
5564   root     TS  -  3  0.0  0.0  S /sbin/udevd                                                                X  X  X  X  X  X  X  X 
6636   messageb TS  -  1  0.0  0.0  S /usr/bin/dbus-daemon --system                                              X  X  X  X  X  X  X  X 
6917   root     TS  -  1  0.0  0.0  S supervising syslog-ng                                                      X  X  X  X  X  X  X  X 
6952   dnsmasq  TS  -  1  0.0  0.0  S /usr/sbin/dnsmasq -x /var/run/dnsmasq.pid --user=dnsmasq --group=dnsmasq   X  X  X  X  X  X  X  X 
6985   root     TS  -  7  0.0  0.0  S /usr/sbin/chronyd -f /etc/chrony/chrony.conf                               X  X  X  X  X  X  X  X 
7415   root     TS  -  7  0.0  0.0  S /usr/sbin/sshd -o PidFile=/run/sshd.pid -f /etc/ssh/sshd_config            X  X  X  X  X  X  X  X 
7610   root     TS  -  0  0.0  0.0  S /usr/sbin/console-kit-daemon --no-daemon                                   X  X  X  X  X  X  X  X 
7611   root     TS  -  4  0.0  0.0  S     gmain                                                                  X  X  X  X  X  X  X  X 
7613   root     TS  -  2  0.0  0.0  S     gdbus                                                                  X  X  X  X  X  X  X  X 
7614   root     TS  -  4  0.0  0.0  S     console-kit-dae                                                        X  X  X  X  X  X  X  X 
7617   root     TS  -  6  0.0  0.0  S     vt_thread_start                                                        X  X  X  X  X  X  X  X 
</pre>



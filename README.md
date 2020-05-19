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


If you have a large CPU count, use the `--compact` option:
<pre>
[mvconcept@clxap2 smp_affinity]$ ./smp_affinity  --compact --statistics --defined-only
ID     Owner    Description                                                  0          10         20         30         40         50         60         70         80         90         100        110        120        130        140        150        160        170        180        190 
595683 adrien   TS  -  1  78.0 0.1  S /ansys_inc/v201/ansys/ansysbin          X         |          |          |          |          |          |          |          |          |      X   |          |          |          |          |          |          |          |          |          | 
595629 adrien   TS  -  2  78.1 0.1  S /ansys_inc/v201/ansys/ansysbin           X        |          |          |          |          |          |          |          |          |       X  |          |          |          |          |          |          |          |          |          | 
595702 adrien   TS  -  3  78.1 0.1  S /ansys_inc/v201/ansys/ansysbin            X       |          |          |          |          |          |          |          |          |        X |          |          |          |          |          |          |          |          |          | 
595736 adrien   TS  -  7  78.3 0.1  S /ansys_inc/v201/ansys/ansysbin                X   |          |          |          |          |          |          |          |          |          |  X       |          |          |          |          |          |          |          |          | 
595744 adrien   TS  -  8  78.7 0.1  S /ansys_inc/v201/ansys/ansysbin                 X  |          |          |          |          |          |          |          |          |          |   X      |          |          |          |          |          |          |          |          | 
595681 adrien   TS  -  9  78.9 0.1  S /ansys_inc/v201/ansys/ansysbin                  X |          |          |          |          |          |          |          |          |          |    X     |          |          |          |          |          |          |          |          | 
595897 adrien   TS  -  13 79.1 0.1  S /ansys_inc/v201/ansys/ansysbin                    |  X       |          |          |          |          |          |          |          |          |        X |          |          |          |          |          |          |          |          | 
595860 adrien   TS  -  14 79.4 0.1  S /ansys_inc/v201/ansys/ansysbin                    |   X      |          |          |          |          |          |          |          |          |         X|          |          |          |          |          |          |          |          | 
595741 adrien   TS  -  15 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |    X     |          |          |          |          |          |          |          |          |          |X         |          |          |          |          |          |          |          | 
595885 adrien   TS  -  19 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |        X |          |          |          |          |          |          |          |          |          |    X     |          |          |          |          |          |          |          | 
595805 adrien   TS  -  20 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |         X|          |          |          |          |          |          |          |          |          |     X    |          |          |          |          |          |          |          | 
595847 adrien   TS  -  4  79.3 0.1  R /ansys_inc/v201/ansys/ansysbin             X      |          |          |          |          |          |          |          |          |         X|          |          |          |          |          |          |          |          |          | 
595812 adrien   TS  -  5  79.4 0.1  R /ansys_inc/v201/ansys/ansysbin              X     |          |          |          |          |          |          |          |          |          |X         |          |          |          |          |          |          |          |          | 
595833 adrien   TS  -  6  79.5 0.1  R /ansys_inc/v201/ansys/ansysbin               X    |          |          |          |          |          |          |          |          |          | X        |          |          |          |          |          |          |          |          | 
595811 adrien   TS  -  10 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                   X|          |          |          |          |          |          |          |          |          |     X    |          |          |          |          |          |          |          |          | 
595896 adrien   TS  -  11 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |X         |          |          |          |          |          |          |          |          |      X   |          |          |          |          |          |          |          |          | 
595947 adrien   TS  -  12 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    | X        |          |          |          |          |          |          |          |          |       X  |          |          |          |          |          |          |          |          | 
595904 adrien   TS  -  16 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |     X    |          |          |          |          |          |          |          |          |          | X        |          |          |          |          |          |          |          | 
595902 adrien   TS  -  17 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |      X   |          |          |          |          |          |          |          |          |          |  X       |          |          |          |          |          |          |          | 
595938 adrien   TS  -  18 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |       X  |          |          |          |          |          |          |          |          |          |   X      |          |          |          |          |          |          |          | 
595917 adrien   TS  -  21 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |X         |          |          |          |          |          |          |          |          |      X   |          |          |          |          |          |          |          | 
595993 adrien   TS  -  22 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          | X        |          |          |          |          |          |          |          |          |       X  |          |          |          |          |          |          |          | 
595928 adrien   TS  -  23 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |  X       |          |          |          |          |          |          |          |          |        X |          |          |          |          |          |          |          | 
595971 adrien   TS  -  24 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |   X      |          |          |          |          |          |          |          |          |         X|          |          |          |          |          |          |          | 
595893 adrien   TS  -  25 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |    X     |          |          |          |          |          |          |          |          |          |X         |          |          |          |          |          |          | 
595909 adrien   TS  -  26 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |     X    |          |          |          |          |          |          |          |          |          | X        |          |          |          |          |          |          | 
595941 adrien   TS  -  27 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |      X   |          |          |          |          |          |          |          |          |          |  X       |          |          |          |          |          |          | 
595891 adrien   TS  -  31 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |X         |          |          |          |          |          |          |          |          |      X   |          |          |          |          |          |          | 
595989 adrien   TS  -  32 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          | X        |          |          |          |          |          |          |          |          |       X  |          |          |          |          |          |          | 
595948 adrien   TS  -  36 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |     X    |          |          |          |          |          |          |          |          |          | X        |          |          |          |          |          | 
596015 adrien   TS  -  37 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |      X   |          |          |          |          |          |          |          |          |          |  X       |          |          |          |          |          | 
595987 adrien   TS  -  38 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |       X  |          |          |          |          |          |          |          |          |          |   X      |          |          |          |          |          | 
596019 adrien   TS  -  42 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          | X        |          |          |          |          |          |          |          |          |       X  |          |          |          |          |          | 
595991 adrien   TS  -  43 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |  X       |          |          |          |          |          |          |          |          |        X |          |          |          |          |          | 
595981 adrien   TS  -  44 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |   X      |          |          |          |          |          |          |          |          |         X|          |          |          |          |          | 
596011 adrien   TS  -  28 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |       X  |          |          |          |          |          |          |          |          |          |   X      |          |          |          |          |          |          | 
596020 adrien   TS  -  29 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |        X |          |          |          |          |          |          |          |          |          |    X     |          |          |          |          |          |          | 
596022 adrien   TS  -  30 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |         X|          |          |          |          |          |          |          |          |          |     X    |          |          |          |          |          |          | 
595992 adrien   TS  -  33 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |  X       |          |          |          |          |          |          |          |          |        X |          |          |          |          |          |          | 
596023 adrien   TS  -  34 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |   X      |          |          |          |          |          |          |          |          |         X|          |          |          |          |          |          | 
596035 adrien   TS  -  35 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |    X     |          |          |          |          |          |          |          |          |          |X         |          |          |          |          |          | 
596077 adrien   TS  -  39 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |        X |          |          |          |          |          |          |          |          |          |    X     |          |          |          |          |          | 
596038 adrien   TS  -  40 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |         X|          |          |          |          |          |          |          |          |          |     X    |          |          |          |          |          | 
596064 adrien   TS  -  41 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |X         |          |          |          |          |          |          |          |          |      X   |          |          |          |          |          | 
596068 adrien   TS  -  45 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |    X     |          |          |          |          |          |          |          |          |          |X         |          |          |          |          | 
596025 adrien   TS  -  46 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |     X    |          |          |          |          |          |          |          |          |          | X        |          |          |          |          | 
596072 adrien   TS  -  47 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |      X   |          |          |          |          |          |          |          |          |          |  X       |          |          |          |          | 
596099 adrien   TS  -  48 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |       X  |          |          |          |          |          |          |          |          |          |   X      |          |          |          |          | 
596101 adrien   TS  -  49 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |        X |          |          |          |          |          |          |          |          |          |    X     |          |          |          |          | 
596100 adrien   TS  -  50 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |         X|          |          |          |          |          |          |          |          |          |     X    |          |          |          |          | 
596106 adrien   TS  -  51 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |X         |          |          |          |          |          |          |          |          |      X   |          |          |          |          | 
596096 adrien   TS  -  55 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |    X     |          |          |          |          |          |          |          |          |          |X         |          |          |          | 
596102 adrien   TS  -  56 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |     X    |          |          |          |          |          |          |          |          |          | X        |          |          |          | 
596107 adrien   TS  -  60 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |         X|          |          |          |          |          |          |          |          |          |     X    |          |          |          | 
596103 adrien   TS  -  61 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |X         |          |          |          |          |          |          |          |          |      X   |          |          |          | 
596115 adrien   TS  -  62 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          | X        |          |          |          |          |          |          |          |          |       X  |          |          |          | 
596110 adrien   TS  -  66 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |     X    |          |          |          |          |          |          |          |          |          | X        |          |          | 
596111 adrien   TS  -  67 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |      X   |          |          |          |          |          |          |          |          |          |  X       |          |          | 
596114 adrien   TS  -  68 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |       X  |          |          |          |          |          |          |          |          |          |   X      |          |          | 
596108 adrien   TS  -  52 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          | X        |          |          |          |          |          |          |          |          |       X  |          |          |          |          | 
596109 adrien   TS  -  53 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |  X       |          |          |          |          |          |          |          |          |        X |          |          |          |          | 
596118 adrien   TS  -  54 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |   X      |          |          |          |          |          |          |          |          |         X|          |          |          |          | 
596105 adrien   TS  -  57 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |      X   |          |          |          |          |          |          |          |          |          |  X       |          |          |          | 
596117 adrien   TS  -  58 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |       X  |          |          |          |          |          |          |          |          |          |   X      |          |          |          | 
596120 adrien   TS  -  59 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |        X |          |          |          |          |          |          |          |          |          |    X     |          |          |          | 
596112 adrien   TS  -  63 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |  X       |          |          |          |          |          |          |          |          |        X |          |          |          | 
596104 adrien   TS  -  64 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |   X      |          |          |          |          |          |          |          |          |         X|          |          |          | 
596121 adrien   TS  -  65 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |    X     |          |          |          |          |          |          |          |          |          |X         |          |          | 
596119 adrien   TS  -  69 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |        X |          |          |          |          |          |          |          |          |          |    X     |          |          | 
596116 adrien   TS  -  70 79.5 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |         X|          |          |          |          |          |          |          |          |          |     X    |          |          | 
596113 adrien   TS  -  71 79.4 0.1  R /ansys_inc/v201/ansys/ansysbin                    |          |          |          |          |          |          |X         |          |          |          |          |          |          |          |          |      X   |          |          | 
</pre>





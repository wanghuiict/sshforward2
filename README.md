# sshforward2

Use SSH tunneling to set up services in the background, and keep services up by detecting services' status.

```
$ ./sshforward2 
provide services in SSH forwarding tunnel
Usage:
	./sshforward2 [-i][-c][-p] <setting file> [vault file]
Options:
	-i        show config info and exit.
	-c        clean all processes and exit.
	-p        type password.
```

## Example

### git clone 

```
$ git clone https://github.com/wanghuiict/sshforward2
$ cd sshforward2
```

### Create json file named test.json

```
{
    "ssh-0": {
        "hook": "tests/hook-rdp",
        "host": "112.18.100.75",
        "port": "22",
        "user": "root",
        "pass": "password",
        "forward": {
            "rdp": {
                "host": "10.10.10.11",
                "port": "13389",
                "rhost": "172.16.100.245",
                "rport": "3389"
            }
        }
    }
}
```
* ssh-0: ssh remote connection,named "ssh-XXX"
* host: ssh remote host
* port: ssh remote port
* user: ssh remote user
* pass: ssh remote pass
* hook: check functon
* forward: ssh forwarding
* rdp: a friendly name
* host: local host
* port: local port
* rhost: remote host（rdp server in this example）
* rport: remote port


### run command

```
sshforward2$ ./sshforward2 test.json
------------------------------------------------------------------------------
SSH Host: 112.18.100.75 -p 22 -l root
rdp       	         10.10.10.11:13389	       172.16.100.245:3389 
------------------------------------------------------------------------------
searchprocess connector test.json default|connector -p test.json default
LISTEN     0      128    10.10.10.11:13389                    *:*                   users:(("ssh",pid=7196,fd=5))
spawn ssh -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -f -N -L 10.10.10.11:13389:172.16.100.245:3389 112.18.100.75 -p 22 -l root
root@112.18.100.75's password: 

sshforward2$ 

```

## hook

detect connection status periodically.
e.g. tests/hook-rdp for RDP

```
read a rdp c <<< $(python helper.py $conf info |grep "^rdp")
# $rdp is local ip:port
count=6
while true; do
    rdesktop $rdp 2>&1 |grep "ERROR: CredSSP" &>/dev/null
    if [ $? -ne 0 ]; then
        if [ $count -eq 0 ]; then
            break
        fi
        ((count--))
        sleep 5
        continue
    fi
    count=6
    sleep 30
done

```

## vault file

```
$ ./sshforward2 <setting file> [vault file]
```

secret file will be saved in ~/.vault/

e.g. tests/beijing.json

```
{
    "hook": "tests/hook-beijing",
    "ssh-0": {
        "host": "{{ loginhost }}",
        "port": "{{ loginport }}",
        "user": "{{ loginuser }}",
        "pass": "{{ loginpass }}",
        "forward": {
            "redmine": {
                "host": "{{ local_ip }}",
                "port": "{{ redmine_forward }}",
                "rhost": "{{ redmine_server }}",
                "rport": "80"
            },
            "zentao": {
                "host": "{{ local_ip }}",
                "port": "8080",
                "rhost": "10.10.14.14",
                "rport": "8080"
            }
        }
    }
}
```

file named "mysecret1"
```
# remote login node
loginhost: 1.2.3.4
loginport: 22
loginuser: myname
loginpass: mypass
# http server
redmine_server: 10.10.16.60

# local
local_ip: 10.10.16.22
redmine_forward: 18080
```

run command

```
$ ./sshforward2 tests/beijing.json mysecret1
```

mysecret1 in current directory can be deleted.




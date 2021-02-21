#!/bin/bash

# test:
# export host1=10.1.2.3
# export pass1=******
# ./test-expect.sh

function fun1() {
echo "
spawn ssh -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -l root $host1 hostname
expect {
-re \"assword:\" {
send \"$pass1\r\"
exp_continue
}
}
"
}

fun1

cat << eof1 |expect -f -
spawn ssh -oStrictHostKeyChecking=no -oExitOnForwardFailure=yes -l root $host1 hostname
expect {
-re "assword:" {
send "$pass1\r"
exp_continue
}
}
eof1

echo

cat << eof1 |expect -f -
$(fun1)
eof1

cat << eof1 |expect -f - &
$(python ../helper.py ../redmine.json)
eof1

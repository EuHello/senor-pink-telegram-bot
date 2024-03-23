#!/bin/bash
# login.sh

source utils/config.sh

cmd1="aws sso login --profile $MYPROFILE"
echo $cmd1
$cmd1

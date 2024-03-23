#!/bin/bash
# deploy.sh

source utils/config.sh

cmd1="sam deploy --profile $MYPROFILE"
echo $cmd1
time $cmd1

# args --guided

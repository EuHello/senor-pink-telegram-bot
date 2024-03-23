#!/bin/bash
# invoke.sh

source utils/config.sh

cmd1="sam local invoke --profile $MYPROFILE"
echo $cmd1
$cmd1

# sam local invoke --env-vars env.json --event events/event.json --profile $MYPROFILE
# https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-using-invoke.html#serverless-sam-cli-using-invoke-environment-file

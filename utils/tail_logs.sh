#!/bin/bash
# tail_logs.sh

source utils/config.sh

echo "Options: -err          Filter for error logs"

if [[ $1 == "-err" ]]; then
  cmd1="sam logs -n TelegramBot --stack-name senor-pink-telegram-bot --profile $MYPROFILE --tail -s '5min ago' --filter \"err\""
  echo "$cmd1"
  $cmd1
else
  cmd2="sam logs -n TelegramBot --stack-name senor-pink-telegram-bot --profile $MYPROFILE --tail -s '5min ago'"
  echo "$cmd2"
  $cmd2
fi

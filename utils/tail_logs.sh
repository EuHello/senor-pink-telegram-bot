#!/bin/bash
# tail_logs.sh

source utils/config.sh

echo "Options: -b          See only bot app logs"

if [[ $1 == "-b" ]]; then
  cmd1="sam logs -n TelegramBot --stack-name senor-pink-telegram-bot --profile $MYPROFILE --tail -s '5min ago' --filter \"BOT_APP\""
  echo "$cmd1"
  $cmd1
else
  cmd2="sam logs -n TelegramBot --stack-name senor-pink-telegram-bot --profile $MYPROFILE --tail -s '5min ago'"
  echo "$cmd2"
  $cmd2
fi

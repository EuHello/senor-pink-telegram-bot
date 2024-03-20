# senor-pink-telegram-bot


AWS Serverless Application Model (AWS SAM) - with cloudformation  

Architecture  
Telegram Bot/Server -> AWS API gateway -> AWS Lambda -> AWS DynamoDB  


AWS CLI  
AWS SAM CLI  
AWS IAM - permissions  
AWS Parameter Store  

AWS Commands  
`sam init`  

`sam validate`  
`sam local invoke -e events/event.json`  (with docker)
`sam local start-api`

`sam build`  
`sam deploy --guided`  (with S3)  

`sam list`  
`sam logs -n TelegramBot --stack-name mystack`  


Telegram Bot  
`curl --request POST \
--url https://api.telegram.org/bot<TELEGRAM_TOKEN>/setWebhook\
--header 'content-type: application/json'\
--data '{"url": "<LINK_TO_YOUR_LAMBDA_API>"}'`  


structure  
unit tests -pytest  

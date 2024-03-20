# About
Telegram bot that reads message, writes to DB, and responds. 

## Infrastructure 
AWS Serverless Application Model (AWS SAM)  
- Built on top and extends AWS CloudFormation  
- Event driven architecture
- Infrastructure as code
- Serverless Technology  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html  

## Architecture  
Telegram Bot/Server -> AWS API gateway -> AWS Lambda -> AWS DynamoDB  

## Key Tooling
- AWS CLI  
- AWS SAM CLI  
- AWS IAM - permissions  
- AWS Parameter Store  

## Key AWS SAM commands for building and deploying  
`sam init`  

`sam validate`    
`sam build`  
`sam local invoke -e events/event.json` (with docker)
`sam local start-api`  

`sam sync --code --watch`  
`sam sync --no-watch`  

`sam deploy --guided --profile <profile>`  (Deploys to S3)

`sam list`  
`sam logs -n <resource name> --stack-name <mystack>`      


## Telegram Bot 
Uses Web-hook Api.  
Why? This is most suitable for AWS Lambda compared to long-polling (other option).  
`curl -F "url=https://<YOURDOMAIN.EXAMPLE>/<WEBHOOKLOCATION>" -F "certificate=@<YOURCERTIFICATE>.pem" https://api.telegram.org/bot<YOURTOKEN>/setWebhook`    
https://core.telegram.org/bots/webhooks#how-do-i-set-a-webhook-for-either-type  

Setup SSL    
https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-client-side-ssl-authentication.html


## Test
Unit tests with pytest  

# Python Telegram milk bot
A Telegram bot that records babies' milk feedings for allowed users.  
User speaks to the bot, example "12pm 120ml milk". Bot records it and informs user how much milk drank for the day.  
Named after the legendary Señor Pink from One Piece.  

## Infrastructure 
AWS Serverless Application Model (AWS SAM) with AWS Lambda  
- Built on top and extends AWS CloudFormation  
- Event driven architecture
- Infrastructure as code
- Serverless Technology  

https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html  
https://aws.amazon.com/lambda/

## Architecture
Telegram Bot/Server -> AWS API gateway -> AWS Lambda -> AWS DynamoDB  


## Description of key components
| Resources                                   | Description                                                                                                            |
|---------------------------------------------|------------------------------------------------------------------------------------------------------------------------|
| AWS Lambda function                         | Serverless function written in Python. This will contain all functions for the Telegram Bot                            |
| AWS API Gateway                             | API gateway to Lambda                                                                                                  |
| AWS DynamoDB                                | NoSQL Database. We will be using composite primary keys - a partition key and sort key                                 |
| AWS Lambda Authenticator                    | WIP                                                                                                                    |
| AWS Parameter Store                         | Stores secret key-values, via Parameter Store Console. i.e. Telegram Bot Token                                         |
| AWS Parameters and Secrets Lambda Extension | Extension allows Lambda to retrieve secret keys from AWS Parameter Store. Uses cache, which reduces API calls and cost |
| AWS IAM                                     | Permissions                                                                                                            |
| AWS SAM (Serverless Application Model)      | All the above are written in SAM, template.yaml, environment variables too. Configurations are in samconfig.toml       |

Other Tools
- Command Line Interfaces used: AWS CLI and SAM CLI
- Docker - for local testing

## DynamoDB Schema
Two main actions (1) write records e.g. drank milk 100ml. (2) get records by date, sorted by time. e.g. Drank total of 500ml today.   
Hence, I chose to use composite primary keys of date(partition key), and a timestamp(sort key).  
https://aws.amazon.com/blogs/database/choosing-the-right-dynamodb-partition-key/

## AWS SAM Concepts
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html  


## Telegram Bot

### Setting up Bot
Speak to Botfather https://core.telegram.org/bots/features#botfather  

### API - Web-hook
There are two options to communicate with Telegram bot api.  
1. Long Polling  
2. Web-hook - this is my preferred option due for serverless solution like Lambda.  

Why Web-hook?
1. Lower api calls compared to long polling, leading to more costs savings.    
2. In my use case - smaller number of users via allowed user list.  
3. Long polling requires open connection. AWS Lambda works better for event triggers, which are quick, short connections. 
Long polling fits a server model like AWS EC2 better.    

### Web-hook with SSL  
Telegram docs recommends using SSL authentication for web-hooks.
https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-client-side-ssl-authentication.html  


### Creating Web-hook
Create a web-hook with a POST request to Telegram API. 
```
curl -F "url=https://<YOURDOMAIN.EXAMPLE>/<WEBHOOKLOCATION>" -F "certificate=@<YOURCERTIFICATE>.pem" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
```
https://core.telegram.org/bots/webhooks#how-do-i-set-a-webhook-for-either-type  


## Test
Unit tests with pytest  
```bash
pytest
```

## SAM CLI commands
Initiate SAM directory and templates  
```
sam init           # Initiate SAM directory and templates
```

Key AWS SAM commands for build, testing and deployment  
```
sam validate       # Validates SAM template.yaml
sam build          # Builds .aws-sam, uses docker

sam deploy         # Builds zip, deploy to S3. 
                   # useful options: --guided --profile <profile>
```

Local Testing - use after `sam build`. Invokes Lambda function with event json, uses Docker.  
```
sam local invoke     # useful options: --env-vars env.json --event events/event.json --profile <profile>
```

Generate test json for sam local invoke  
```
sam local generate-event apigateway aws-proxy --stage DEV > event.json
```

Simulate API Gateway  
```
sam local start-api
```

Sync local dev changes to AWS
```
sam sync --code --watch     # Local changes are sync to cloud
sam sync --no-watch         # Stop sync
```

Pull logs from AWS
```
sam logs -n <resource name> --stack-name <mystack>      # useful options: --tail -s '5min ago'
```

View Endpoints and Resources
```
sam list endpoints      # useful opions: --region <region> --profile <profile>
sam list resources
```

## Odds and Ends

### AWS CloudWatch console
https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-cwconsole  

### Log Retention with AWS CloudWatch console
https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#SettingLogRetention  

### Change Log timezone in AWS CloudWatch console
https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#ViewingLogData  
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/modify_graph_date_time.html#set-time-zone-Cloudwatch-graph  


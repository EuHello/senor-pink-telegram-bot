# About
A Telegram bot that records babies' milk feedings for allowed users.  
Essentially, a bot that reads chat messages, writes to DB, and responds.  
Named after the legendary Senor Pink from One Piece.  

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


## Prerequisites and Key Tooling
- Lambda function <- Python 3    
- AWS SAM Template
- CLI - AWS CLI, AWS SAM CLI
- Docker - for local testing
- AWS IAM - permissions
- AWS Parameter Store - for parameter and secrets


## AWS SAM
Concepts  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/sam-specification.html  


Initiate SAM directory and templates  
```bash
sam init        # Initiate SAM directory and templates
```

Key AWS SAM commands for build, testing and deployment  
```bash
sam validate    # Validates SAM template.yaml
sam build       # Builds .aws-sam
sam deploy --guided --profile <profile>    # Builds zip, deploy to S3 
```

Local Testing - use after sam build
```bash
sam local invoke -e events/event.json    # Invokes Lambda function with event json. Creates local Docker
sam local start-api                      # Simulate local Api Gateway

sam sync --code --watch                  # Local changes are sync to cloud
sam sync --no-watch                      # Stop sync
```

Pulling logs from AWS
```bash
sam logs -n <resource name> --stack-name <mystack>  
```

View Endpoints and Resources
```bash
sam list endpoints --region <region> --profile <profile>
sam list resources --region <region> --profile <profile>
```

## Telegram Bot
There are two options to communicate with Telegram bot api.  
1. Long Polling  
2. Web-hook - this is the preferred option due to Lambda.  

### Setting up Bot
https://core.telegram.org/bots/features#botfather  

### Web-hook Api
Preferred option with AWS Lambda.  
1. Lower api calls compared to long polling, leading to more costs savings.    
2. Smaller number of allowed users.  
3. Requires open connection. AWS Lambda works better for event triggers (quick connections), rather than long polling (open connect fits AWS EC2 server better).    

### Web-hook with SSL  
Recommended Option.  
https://docs.aws.amazon.com/apigateway/latest/developerguide/getting-started-client-side-ssl-authentication.html  


### Creating Web-hook
```bash
curl -F "url=https://<YOURDOMAIN.EXAMPLE>/<WEBHOOKLOCATION>" -F "certificate=@<YOURCERTIFICATE>.pem" https://api.telegram.org/bot<YOURTOKEN>/setWebhook
```
https://core.telegram.org/bots/webhooks#how-do-i-set-a-webhook-for-either-type  


## Test
Unit tests with pytest  


## Odds and Ends
### AWS Parameter Store
Stores telegram bot token as a secret key.  

### Policy to allow AWS Lambda function to read from Parameter Store 
On SAM Template, add policy template for SSMParameterReadPolicy.  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-templates.html  
https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-policy-template-list.html#ssm-parameter-read-policy  
https://stackoverflow.com/questions/53361664/aws-sam-managed-policy-for-ssm-get-parameter  


### AWS Parameters and Secrets Lambda Extension
Extension allows AWS Lambda to pull secret keys from Parameter Store.  
Extension uses cache, which reduces API calls, reduces cost.  
Create Extension layer in SAM Template.  
https://docs.aws.amazon.com/systems-manager/latest/userguide/ps-integration-lambda-extensions.html  
https://community.aws/posts/parameters-and-secrets-lambda-extension-with-python  
https://docs.aws.amazon.com/secretsmanager/latest/userguide/retrieving-secrets_lambda.html#retrieving-secrets_lambda_ARNs  

### Logging with AWS CloudWatch
https://docs.aws.amazon.com/lambda/latest/dg/python-logging.html#python-logging-cwconsole  

### Set Log Retention with AWS CloudWatch
https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#SettingLogRetention  

### Change Log timezone in AWS CloudWatch
https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/Working-with-log-groups-and-streams.html#ViewingLogData  
https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/modify_graph_date_time.html#set-time-zone-Cloudwatch-graph  
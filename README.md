# Microservice serverless, lambda, python, AWS

- npm i -g serverless
- configure aws profile using deploy production

1. git clone project
2. virtualenv venv --python=python3
3. source venv/bin/activate
2. npm install
3. pip install -r requirements.txt

# Running project lambda, dynamoDB localhost

1. sls wsgi serve
2. sls dynamodb install  
3. sls dynamodb start

# Deploy production 

1. sls deploy 
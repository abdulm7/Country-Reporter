# Country Reporter a React and AWS Cloud Native Application

## Avaliable at: https://web-app.d2t1p3afrg3owy.amplifyapp.com/

## A Full-stack web application written in JavaScript and Python, deployed on AWS Amplify

* This web application allows users to generate and view reports based on a specific country or a specific year.
* Reports are created in the Lambda backend, which then stores these reports in their respective s3 buckets.
* Users may then view all generated reports via the 'view' button in the reports table
* The reports table and raw database tables will be retrieved on load

#  Architecture Diagram
![CountryReporterArchitectureDiagram](https://github.com/abdulm7/Country-Reporter/assets/46537861/0367b775-ea35-403e-9d50-2d9b9928b443)

# How to Run

* install dependencies via "npm run-script build"
* each python script with the prefix "lambda_" is backend code for each lambda function required
* all lambda functions must be on the same API url to utilize the same env variable
  * Feel free to use mutliple, just note you will need to update your env file + api request
* NOTE the endpoint is the name of the lambda function
  * e.g. "lambda_GetReports" has API call (process.env.REACT_APP_API + "/GetReports")
  * Note that most lambda functions require query string parameters e.g. "/CreateCountryReport?country=Canada"
* Ensure you give lambda functions appropriate roles via IAM Roles e.g. 
  * "GetReports" has read only access to S3
  * "DbRetrieve" has read only access to DynamoDB
* React front-end is hosted on AWS Amplify, however can be hosted where ever since it has no direct access to AWS
* Check 'console-app' branch on DynamoDB structure 

# Coming Soon/To Do
* Add/Delete from Database tables
* Delete reports from S3
* Edit existing records
* Create VPC with subnets for data protection
* User Authentication
* CI/CD pipelines

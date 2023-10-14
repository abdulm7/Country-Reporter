resource "aws_iam_role" "cr_lambda_role" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "lambda.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )

  name = "cr-backend-role-garoobh3"
  path = "/service-role/"

}

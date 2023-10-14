resource "aws_dynamodb_table" "cr_table_non_econ" {
  name = "non-econ"
}

resource "aws_dynamodb_table" "cr_table_econ" {
  name = "econ"
}

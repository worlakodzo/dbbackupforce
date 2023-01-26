## Worlako DevOps Portforlio (Develop Bootcamp Ghana 1)









## AWS IAM  user and role Permission
- User access policy
    - Create inline policy
    ```
            {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "eksadministrator",
                    "Effect": "Allow",
                    "Action": "eks:*",
                    "Resource": "*"
                }
            ]
        }
     ```
- Role access policy
    - AmazonEC2FullAccess
    - IAMFullAccess
    - AmazonEC2ContainerRegistryFullAccess
    - AmazonS3FullAccess
    - AmazonDynamoDBFullAccess
    - AmazonElasticContainerRegistryPublicFullAccess
    - Create inline policy
    ```
        {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "eksadministrator",
                    "Effect": "Allow",
                    "Action": "eks:*",
                    "Resource": "*"
                }
            ]
        }
    ```
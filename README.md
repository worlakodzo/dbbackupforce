## Worlako DevOps Portforlio (Develop Bootcamp Ghana 1)


### Amazon EKS add-ons
- kube-proxy                (Enable service networking within your cluster.)
- CoreDNS                   (Enable service discovery within your cluster.)
- Amazon VPC CNI            (Enable pod networking within your cluster.)
- Amazon EBS CSI Driver     (Enable Amazon Elastic Block Storage (EBS) within your cluster)







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




### Reference 
- https://yashmehrotra.com/posts/building-minimal-docker-images-using-multi-stage-builds/
- https://gabnotes.org/lighten-your-python-image-docker-multi-stage-builds/
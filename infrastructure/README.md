# EKS-Cluster

### Create Amazon S3 bucket
The s3 bucket is use for terraform state file versioning
and service as a single source of truth
```
 aws s3api create-bucket –bucket <bucket-name-here> –region us-east-2 –create-bucket-configuration LocationConstraint=us-east-2

 aws s3api put-bucket-encryption –bucket <bucket-name-here> –server-side-encryption-configuration "{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\": \"AES256\"}}]}"

```


### Create Amazon S3 bucket
The s3 bucket is use for terraform state file versioning
and service as a single source of truth
```
 aws s3api create-bucket –bucket <bucket-name-here> –region us-east-2 –create-bucket-configuration LocationConstraint=us-east-2

 aws s3api put-bucket-encryption –bucket <bucket-name-here> –server-side-encryption-configuration "{\"Rules\": [{\"ApplyServerSideEncryptionByDefault\":{\"SSEAlgorithm\": \"AES256\"}}]}"
 
```

### Create a DynamoDB Table
A Terraform configuration uses the DynamoDB table to store the lock to prevent concurrent access to the terraform.tfstate file.

```
aws dynamodb create-table –table-name <table-name-here> –attribute-definitions AttributeName=LockID,AttributeType=S –key-schema AttributeName=LockID,KeyType=HASH –provisioned-throughput ReadCapacityUnits=5,WriteCapacityUnits=5

```





### Reference
- https://aws.plainenglish.io/terraform-deploy-an-eks-cluster-like-a-boss-9487eadcc3bb
- https://medium.com/devops-mojo/terraform-provision-amazon-eks-cluster-using-terraform-deploy-create-aws-eks-kubernetes-cluster-tf-4134ab22c594
- https://aws.github.io/aws-eks-best-practices/networking/subnets/
- https://skundunotes.com/2021/07/10/ci-cd-of-terraform-workspace-with-yaml-based-azure-pipelines/
- https://www.youtube.com/watch?v=yk_mm-hHirw
- https://stackoverflow.com/questions/74741993/0-1-nodes-are-available-1-pod-has-unbound-immediate-persistentvolumeclaims
- https://registry.terraform.io/providers/hashicorp/helm/latest
- https://github.com/hashicorp/terraform-provider-helm#getting-started
- https://betterprogramming.pub/how-to-set-up-argo-cd-with-terraform-to-implement-pure-gitops-d5a1d797926a
- https://registry.terraform.io/providers/hashicorp/helm/latest/docs
- https://developer.hashicorp.com/terraform/tutorials/kubernetes/helm-provider?in=terraform%2Fkubernetes&_ga=2.155087536.923481247.1674612086-2082629525.1674612086#review-the-helm-configuration
- https://docs.aws.amazon.com/eks/latest/APIReference/API_RemoteAccessConfig.html
- https://harshitdawar.medium.com/launching-a-vpc-with-public-private-subnet-nat-gateway-in-aws-using-terraform-99950c671ce9



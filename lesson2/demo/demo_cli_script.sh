aws sagemaker create-training-job --training-job-name  xgboost-cli-demo --role-arn arn:aws:iam::565094796913:role/execution_role --algorithm-specification TrainingImage=433757028032.dkr.ecr.us-west-2.amazonaws.com/xgboost:1,TrainingInputMode=File --input-data-config file://input_data_config.json  --output-data-config S3OutputPath=s3://sagemaker-us-west-2-565094796913/cli-output --resource-config InstanceType='ml.m4.xlarge',InstanceCount=1,VolumeSizeInGB=10  --stopping-condition MaxRuntimeInSeconds=60

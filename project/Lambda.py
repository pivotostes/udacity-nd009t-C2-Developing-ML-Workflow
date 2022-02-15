# First Lambda Function 

import json
import boto3
import base64

s3 = boto3.client('s3')

def lambda_handler(event, context):
    """A function to serialize target data from S3"""
    
    
    # Get the s3 address from the Step Function event input
    key = event['s3_key']
    bucket = event['s3_bucket']
    
    # Download the data from s3 to /tmp/image.png
    s3.download_file(bucket, key, '/tmp/image.png' )    
        
    # We read the data from a file
    with open("/tmp/image.png", "rb") as f:
        image_data = base64.b64encode(f.read())
    
    # Pass the data back to the Step Function
    print("Event:", event.keys())
    
    return {
        'statusCode': 200,
        'body': {
            "image_data": image_data,
            "s3_bucket": bucket,
            "s3_key": key,
            "inferences": []
        }
    }

# Second Lambda Function 

import json
import base64
import boto3

# Fill this in with the name of your deployed model
ENDPOINT = "image-classification-2022-02-13-21-30-58-612"

runtime = boto3.client("runtime.sagemaker")

def lambda_handler(event, context):

    # Decode the image data
    image = base64.b64decode(event['image_data'])
    

    # Instantiate a Predictor
    predictor = runtime.invoke_endpoint(
        EndpointName=ENDPOINT,
        ContentType='image/png',
        Body=image
        )

    # For this model the IdentitySerializer needs to be "image/png"
    # predictor.serializer = IdentitySerializer("image/png")
    
    # Make a prediction:
    
    inferences = json.loads(predictor['Body'].read().decode('utf-8'))
    
    # We return the data back to the Step Function    
    event["inferences"] = inferences
    
    print("event:", event)
    
    return {
        'statusCode': 200,
        'body': json.dumps(event)
    }


# Third Lambda Function 

import random
import boto3
import json


def generate_test_case():
    # Setup s3 in boto3
    s3 = boto3.resource('s3')
    
    # Randomly pick from sfn or test folders in our bucket
    objects = s3.Bucket(bucket).objects.filter(Prefix="test")
    
    # Grab any random object key from that folder!
    obj = random.choice([x.key for x in objects])
    
    return json.dumps({
        "image_data": "",
        "s3_bucket": bucket,
        "s3_key": obj
    })

test_case_list = []
for i in range(100):
    generate_test_case()
    test_case_list.append(json.loads(generate_test_case()))

with open("tests_case.json", 'w') as f:
    f.write('[' + '\n')
    for item in test_case_list:
        f.write(json.dumps(item) + ',' + "\n")
    f.write(']')
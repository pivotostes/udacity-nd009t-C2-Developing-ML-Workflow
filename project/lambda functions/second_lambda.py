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



import boto3
import json
import os
import logging
import base64
import re

# Set up logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    # Initialize S3 and Polly clients
    s3 = boto3.client('s3')
    polly = boto3.client('polly')

    # Get the bucket names from environment variables
    source_bucket = os.environ.get('Source_S3')
    destination_bucket = os.environ.get('Destination_S3')

    # Log the incoming event
    logger.info(f"Received event: {json.dumps(event)}")

    # Define CORS headers
    cors_headers = {
        'Access-Control-Allow-Origin': '*',
        'Access-Control-Allow-Methods': 'POST, OPTIONS',
        'Access-Control-Allow-Headers': 'Content-Type'
    }

    # Handle preflight OPTIONS request
    if event.get('httpMethod') == 'OPTIONS':
        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps('CORS preflight successful')
        }

    # Check if the environment variables are set
    if not source_bucket or not destination_bucket:
        logger.error("Missing source or destination S3 bucket environment variables")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps('Server Error: Missing environment variables for S3 buckets')
        }

    # Parse the request body
    if event.get('body'):
        body = event['body']

        # Decode Base64 if necessary
        if event.get('isBase64Encoded') and event['isBase64Encoded']:
            body = base64.b64decode(body).decode('utf-8')

        # Extract file content, filename, voice type, and engine using regex
        file_match = re.search(
            r'Content-Disposition: form-data; name="file"; filename="(.?)"\r\nContent-Type:.?\r\n\r\n(.*?)(?:\r\n--)', body, re.S)
        voice_match = re.search(
            r'Content-Disposition: form-data; name="voice"\r\n\r\n(.*?)\r\n', body)
        engine_match = re.search(
            r'Content-Disposition: form-data; name="engine"\r\n\r\n(.*?)\r\n', body)

        if file_match:
            filename = file_match.group(1).strip()
            text_content = file_match.group(2).strip()
        else:
            logger.error("File content is missing")
            return {
                'statusCode': 400,
                'headers': cors_headers,
                'body': json.dumps('Bad Request: File content is required')
            }

        voice_type = voice_match.group(1).strip() if voice_match else 'Joanna'
        engine = engine_match.group(1).strip() if engine_match else 'standard'
    else:
        logger.error("No body found in the event")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps('Bad Request: No body found in the request')
        }

    if not text_content:
        logger.error("Text content is missing")
        return {
            'statusCode': 400,
            'headers': cors_headers,
            'body': json.dumps('Bad Request: Text content is required')
        }

    try:
        # Send text to Polly
        response = polly.synthesize_speech(
            Text=text_content,
            OutputFormat='mp3',
            VoiceId=voice_type,
            Engine=engine
        )

        if 'AudioStream' not in response:
            logger.error("Polly response does not contain 'AudioStream'")
            return {
                'statusCode': 500,
                'headers': cors_headers,
                'body': json.dumps("Error: Polly response does not contain 'AudioStream'")
            }

        # Save audio file to S3
        audio_key = filename.replace('.txt', '.mp3')
        s3.put_object(Bucket=destination_bucket, Key=audio_key, Body=response['AudioStream'].read())

        # Generate a presigned URL
        presigned_url = s3.generate_presigned_url('get_object',
                                                  Params={'Bucket': destination_bucket,
                                                   'Key': audio_key,
                                                   'ResponseContentDisposition': 'attachment; filename="output.mp3"'},
                                                  ExpiresIn=3600)

        return {
            'statusCode': 200,
            'headers': cors_headers,
            'body': json.dumps({'message': 'Audio file successfully created', 'audio_url': presigned_url})
        }

    except Exception as e:
        logger.error(f"Error during text-to-speech processing: {str(e)}")
        return {
            'statusCode': 500,
            'headers': cors_headers,
            'body': json.dumps(f"An internal server error occurred: {str(e)}")
        }
# Serverless Text-to-Audio Conversion Platform with AWS Polly and S3

This project implements a cloud-based, serverless text-to-speech conversion system using AWS services. It allows users to upload text files (such as books or articles) and converts them into MP3 audiobooks using Amazon Polly. The generated audio is stored in an S3 bucket, making it available for easy download.

## Prerequisites

Before starting, ensure that you have:
- An active AWS account.
- Basic knowledge of AWS services (S3, Lambda, API Gateway, IAM).
- Node.js installed on your machine (for AWS Amplify setup).
- Access to the AWS Management Console.

## Step 1: Set Up AWS S3 Bucket for Storing Audiobooks

### 1. Create an S3 Bucket:
- Go to the **S3** service in the AWS Console.
- Click on **Create Bucket**.
- Name the bucket `audio-storage-polly` (or your preferred name).
- Disable **Block all public access** for the bucket to enable access for downloading audiobooks.
![Screenshot 2024-11-19 115236](https://github.com/user-attachments/assets/f3629bcb-4acf-40d3-a2e2-ef67bd3cf9b0)
![Screenshot 2024-11-19 115206](https://github.com/user-attachments/assets/8a3f545a-295a-45ff-a73d-619b20454a03)
![Screenshot 2024-11-19 115250](https://github.com/user-attachments/assets/6fc07bb0-9c6e-4285-b491-849f168c6b17)

## Step 2: Set Up IAM Policies for Polly and S3 Access

### 1. Create the S3 Access Policy:
- Go to the **IAM** service in the AWS Console.
- Create a new policy for **S3** access.
- Under **Specify ARNs**, choose **S3 bucket** and specify the ARN for your bucket, for example:  
  `arn:aws:s3:::audio-storage-polly/*`
- Add the necessary actions: `PutObject`, `PutObjectAcl`, `GetObject`, and `GetObjectAcl` to allow the policy to modify and access objects in this specific bucket.
 ![Screenshot 2024-11-19 114921](https://github.com/user-attachments/assets/5620081f-5534-4cae-bec3-8da1e44d99aa)
 ![Screenshot 2024-11-19 115053](https://github.com/user-attachments/assets/d52941e8-17e7-4ebe-a1d0-e3331e765454)
 ![Screenshot 2024-11-19 115103](https://github.com/user-attachments/assets/d16dbc2a-e1cb-43d9-ae10-9f36d32e2632)
  ![Screenshot 2024-11-19 115420](https://github.com/user-attachments/assets/bd8474ab-a804-4031-8584-46dfbad0f3ba)
 ![Screenshot 2024-11-19 115356](https://github.com/user-attachments/assets/0d5d0818-dd70-447f-9958-d5c71b9dd673)

  
### 2. Create the Polly Access Policy:
- In IAM, create another policy for **Polly** access.
- Add the `synthesize-speech` action.
 ![Screenshot 2024-11-19 115621](https://github.com/user-attachments/assets/18f1598a-b2f7-4879-824e-021e007439b6)
 ![Screenshot 2024-11-19 115703](https://github.com/user-attachments/assets/8bbc4a2d-5c8d-4a4f-a353-e518f79161b9)
Now we can see the created poilices:
![Screenshot 2024-11-19 115726](https://github.com/user-attachments/assets/381ec9ce-d2a3-4c70-afe2-9a758bfca60a)

## Step 3: Create the IAM Role for Lambda Execution

### 1. Create the IAM Role:
- Go to IAM > Roles and create a new role.
- Attach the **AWS Lambda execution role**, **S3 access policy**, and **Polly access policy** to the role.
- Name the role `polly-s3-lambda-role`.
 ![Screenshot 2024-11-19 115849](https://github.com/user-attachments/assets/e5e58859-043d-47ac-b168-e3c9e9cb1918)
  ![Screenshot 2024-11-19 120032](https://github.com/user-attachments/assets/e17d1eba-54ce-4659-b372-d230a1411773)
  ![Screenshot 2024-11-19 120110](https://github.com/user-attachments/assets/832a8be4-da3a-4f66-a4f1-9c8e1fe77639)
  ![Screenshot 2024-11-19 120157](https://github.com/user-attachments/assets/782fdf26-986b-499c-abd3-265a51bac3c1)
 ![Screenshot 2024-11-19 120212](https://github.com/user-attachments/assets/cd953b63-78f2-47e0-9fdb-c7461e64db63)
  
## Step 4: Set Up AWS Lambda Function

### 1. Create a New Lambda Function:
- Go to the **Lambda** service and create a new function.
- Name it (e.g., `text-to-speech-converter`).
- Choose **Python 3.12** as the runtime.
- Set the execution role to `polly-s3-lambda-role`.
  ![Screenshot 2024-11-19 120357](https://github.com/user-attachments/assets/08da8174-0874-42e5-b134-54ce5703b112)
  ![Screenshot 2024-11-19 120417](https://github.com/user-attachments/assets/37dfadb2-9911-4abc-8493-33fd1135f707)
  
### 2. Configure Lambda Function Trigger:
- Add a new **API Gateway** trigger to the Lambda function.
- Select **REST API** and configure the API for your function.
- Enable **CORS** for cross-origin requests and add binary media types: `*/*`, `audio/mpeg`, `text/plain`.
- MAKE SURE U ADD ALL THE BINARY MEDIA TYPES
    ![Screenshot 2024-11-19 120547](https://github.com/user-attachments/assets/38adb414-2456-4fe4-8f3b-e210b41121ef)
   ![Screenshot 2024-11-19 120555](https://github.com/user-attachments/assets/35a0ade0-970d-4488-8112-fe6ef83dac91)
   ![Screenshot 2024-11-19 120923](https://github.com/user-attachments/assets/1f3275e6-8cb8-412e-b968-e001f0fae1c4)
### 3. Deploy the API:
- After configuring the API Gateway, deploy it.
- Copy the **Invoke URL** for later use in Lambda.
  ![Screenshot 2024-11-19 121035](https://github.com/user-attachments/assets/c02aec22-7d35-40dd-9066-6e9077af9b52)
  ![Screenshot 2024-11-19 121104](https://github.com/user-attachments/assets/b43f0e31-9097-4640-afd9-1940291c1474)

## Step 5: Modify Lambda Code and Set Environment Variables

### 1. Modify Lambda Code:
- Open the Lambda function in the AWS Console.
- Modify the code to include the **Invoke URL** for the API Gateway.
- Ensure that your Lambda function is sending the request to the correct API endpoint for text-to-speech conversion.
  ![Screenshot 2024-11-19 121309](https://github.com/user-attachments/assets/0aa42c04-3813-4424-ad7d-ae66042b1461)
 ![Screenshot 2024-11-19 121254](https://github.com/user-attachments/assets/f102836b-c80f-4f4c-b1ec-ab1b0ffcadce)
### 2. Set Environment Variables:
- In the Lambda configuration, add an environment variable:
  - **Key**: `Destination_S3`
  - **Value**: `audio-storage-polly` (or your bucket name).
    ![Screenshot 2024-11-19 121402](https://github.com/user-attachments/assets/3a13c050-1923-4a48-800f-c0d17442223c)
   ![Screenshot 2024-11-19 121501](https://github.com/user-attachments/assets/1179fc41-cf9d-473f-a81c-4bed2f4aa9da)
    ![Screenshot 2024-11-19 121539](https://github.com/user-attachments/assets/529b0552-c517-4d27-9758-28254def147e)
## Step 6: Upload HTML for the Frontend (UI)

### 1. Create the HTML Interface:
- Create an `index.html` file for the UI, allowing users to upload text files for conversion to audio.
- Include an upload button and text display for showing conversion progress.
- Set up a function to handle file uploads and send requests to the Lambda function via API Gateway.
 ![Screenshot 2024-11-19 123938](https://github.com/user-attachments/assets/d7383f8c-08ce-491d-9ed3-196a610cf69b)


### 2. Deploy HTML on AWS Amplify:
- Set up **AWS Amplify** to deploy your HTML frontend.
- Connect the project to Amplify and deploy it.
- Ensure that the frontend is linked to the backend Lambda API for seamless text-to-speech conversion.
 ![Screenshot 2024-11-19 123820](https://github.com/user-attachments/assets/e7a9ba31-22b7-4acc-a209-b82558b5701a)

## Step 7: Testing and Verifying the Solution

### 1. Upload Text File and Convert:
- Test the full workflow by uploading a text file (e.g., a book) through the UI.
- Check if the text-to-speech conversion works, and the resulting MP3 file is stored in the S3 bucket.
 ![Screenshot 2024-11-19 124000](https://github.com/user-attachments/assets/a28b575a-5348-425b-a24f-ce4544b595ff)
  ![Screenshot 2024-11-19 124000](https://github.com/user-attachments/assets/a28b575a-5348-425b-a24f-ce4544b595ff)
## Step 8: Custom Test for Lambda Function

You can test the Lambda function to ensure it correctly converts text to an audio file. Here's how to create a custom test using base64-encoded input for the Lambda function:
### 1. Prepare Base64 Encoded Test Data:
   - First, encode your text input (e.g., a sample text or book) into base64.
   - For instance, using Python, you can do this:
     ```python
     import base64
     
     text = "This is a test text to convert to audio."
     encoded_text = base64.b64encode(text.encode('utf-8')).decode('utf-8')
     print(encoded_text)
     ```
   
   - This will give you the base64 encoded string of your input text.

### 2. Create a Test Event in Lambda:
   - In the AWS Lambda Console, navigate to the **Test** tab.
   - Create a new test event with the base64-encoded data. The event should look something like this:
     ```json
     {
       "body": "Base64_Encoded_Text_Here"
     }
     ```
   - Make sure to replace `"Base64_Encoded_Text_Here"` with your actual base64-encoded text.
### 3. Run the Test:
   - Save the test and click **Test**.
   - Check the **Execution Result** to see if the Lambda function processes the input and returns the correct audio output.

   - The response should include a link to the generated MP3 file stored in your S3 bucket.
    ![Screenshot 2024-11-19 121649](https://github.com/user-attachments/assets/131b409c-4f99-4b63-aa4d-a91bb31ccb1e)
     ![Screenshot 2024-11-19 123618](https://github.com/user-attachments/assets/f77b65b9-98f9-49d4-8364-b6781397c5ce)

## Conclusion

This project demonstrates a fully serverless text-to-speech conversion platform using AWS services like Polly, Lambda, S3, and API Gateway. By following the steps above, you can easily set up and deploy a system that converts text files into audiobooks and stores them for download.
## Contributors

This project was developed and maintained by:

- [R Bharath](https://github.com/bharathr31)
- [E NIKHILESHWAR REDDY ](https://github.com/Nckil1710)

Both contributed equally to the development and implementation of the project.

  

























  




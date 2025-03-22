import boto3
import csv
from botocore.exceptions import ClientError
from datetime import datetime
import re

# AWS session and clients
session = boto3.Session(profile_name='default')
sns_client = session.client('sns', region_name='eu-north-1')
s3_client = session.client('s3', region_name='eu-north-1')

# Config
sns_topic_arn = "arn:aws:sns:eu-north-1:423755635942:VulnCure"
s3_bucket_name = "myvulncurebucket"  # Replace with your bucket name

# Convert text report to CSV with timestamp
def convert_to_csv(text_file_path):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_file_path = f"trivy_report_{timestamp}.csv"
        
        with open(text_file_path, 'r') as file:
            lines = file.readlines()
        
        # Extract CVE details using regex
        pattern = re.compile(r"CVE:\s*(\S+),\s*Package:\s*(\S+),\s*Installed:\s*(\S+),\s*Fixed:\s*([\S, ]*),\s*Severity:\s*(\S+)")
        
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["CVE ID", "Package", "Installed Version", "Fixed Versions", "Severity"])
            
            for line in lines:
                match = pattern.search(line)
                if match:
                    writer.writerow(match.groups())
        print(f"CSV file generated successfully: {csv_file_path}")
        return csv_file_path
    except Exception as e:
        print(f"Error converting to CSV: {e}")
        return None

# Upload file to S3 and generate a pre-signed URL
def upload_to_s3(file_path, s3_bucket_name):
    file_name = file_path.split('/')[-1]
    try:
        s3_client.upload_file(file_path, s3_bucket_name, file_name)
        file_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': s3_bucket_name, 'Key': file_name},
            ExpiresIn=3600  # URL valid for 1 hour
        )
        print(f"File uploaded successfully. Pre-signed URL: {file_url}")
        return file_url
    except ClientError as e:
        print(f"Error uploading to S3: {e}")
        return None

# Send SNS Email with Pre-signed URL
def send_sns_email(text_file_path):
    csv_file_path = convert_to_csv(text_file_path)
    if not csv_file_path:
        return

    file_url = upload_to_s3(csv_file_path, s3_bucket_name)
    if not file_url:
        return

    subject = "Trivy Scan Report - Vulnerabilities Found"
    message = (f"Hello Team,\n\n"
               f"The Trivy scan report has been converted to CSV and uploaded to S3. Please download it using the following secure link (valid for 1 hour):\n"
               f"{file_url}\n\n"
               f"Best regards,\nVulnCure Team")

    try:
        response = sns_client.publish(
            TopicArn=sns_topic_arn,
            Message=message,
            Subject=subject
        )
        print(f"Email sent successfully! Message ID: {response['MessageId']}")
    except ClientError as e:
        print(f"Error sending email: {e}")

# Call function to send email
file_path = "parse_trivy_output.txt"
send_sns_email(file_path)

import boto3
import csv
from botocore.exceptions import ClientError

# AWS session and clients
session = boto3.Session(profile_name='default')
sns_client = session.client('sns', region_name='eu-north-1')
s3_client = session.client('s3', region_name='eu-north-1')

# Config
sns_topic_arn = "arn:aws:sns:eu-north-1:423755635942:VulnCure"
s3_bucket_name = "myvulncurebucket"  # Replace with your bucket name

# Convert text report to CSV
def convert_to_csv(text_file_path, csv_file_path):
    try:
        with open(text_file_path, 'r') as file:
            lines = file.readlines()
        
        # Assuming Trivy output follows a pattern: CVE, Severity, Description, etc.
        with open(csv_file_path, 'w', newline='') as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["CVE ID", "Severity", "Description"])
            
            for line in lines:
                parts = line.strip().split('|')  # Adjust delimiter if necessary
                if len(parts) >= 3:
                    writer.writerow(parts[:3])
        print("CSV file generated successfully.")
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
    csv_file_path = "trivy_report.csv"
    csv_file_path = convert_to_csv(text_file_path, csv_file_path)
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


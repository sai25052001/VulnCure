import boto3
from botocore.exceptions import ClientError

session = boto3.Session(profile_name='default')
sns_client = session.client('sns')
# AWS SNS client
sns_client = boto3.client('sns', region_name='eu-north-1')

# SNS Topic ARN (replace with your SNS topic ARN)
sns_topic_arn = "arn:aws:sns:eu-north-1:423755635942:VulnCure"

# Read the file content
def read_file_content(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read()
    except FileNotFoundError:
        print("Error: File not found.")
        return None

def send_sns_email(file_path):
    content = read_file_content(file_path)
    if content is None:
        return

    subject = "Trivy Scan Report - Vulnerabilities Found"
    message = f"Hello Team,\n\nPlease find the Trivy scan report below:\n\n{content}\n\nBest regards,\nVulnCure Team"

    try:
        # Publish message to SNS Topic
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


import json
import boto3


def extract_text(response, extract_by="LINE"):
    line_text = []
    for block in response["Blocks"]:
        if block["BlockType"] == extract_by:
            line_text.append(block["Text"])
    return line_text


def lambda_handler(event, context):
    textract = boto3.client("textract")
    if event:
        file_obj = event["Records"][0]
        bucketname = str(file_obj["s3"]["bucket"]["name"])
        filename = str(file_obj["s3"]["object"]["key"])

        print(f"Bucket: {bucketname} ::: Key: {filename}")

        response = textract.detect_document_text(
            Document={
                "S3Object": {
                    "Bucket": bucketname,
                    "Name": filename,
                }
            }
        )
        print(json.dumps(response))

        # change LINE by WORD if you want word level extraction
        raw_text = extract_text(response, extract_by="LINE")
        print(raw_text)
        

        file_name_json = filename.split('/')[-1].split('.')[0]+".json"
        s3 = boto3.client('s3')
        json_object = raw_text
        s3.put_object(Body=json.dumps(json_object), Bucket=bucketname, Key='object_json/'+file_name_json )
    
    
        return {
            "statusCode": 200,
            "body": json.dumps("Document processed successfully!"),
        }

    return {"statusCode": 500, "body": json.dumps("There is an issue!")}
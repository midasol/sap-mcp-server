import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
import os
import io
import base64
from google.api_core.client_options import ClientOptions
from google.cloud.speech_v2 import SpeechClient
from google.cloud.speech_v2.types import cloud_speech

import base64
import vertexai
from vertexai.generative_models import GenerativeModel, Part, SafetySetting
from google.cloud import storage
import uuid
import datetime
import json
import re

from http import cookies
from urllib.request import Request, urlopen

from base64 import b64encode

import xml.etree.ElementTree as ET

import ssl

import base64
import os
import pickle
from io import BytesIO
import uuid

import pandas as pd


from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.auth.transport.requests import Request as AuthRequest

from google import genai
from google.genai import types


storage_client = storage.Client()

# SAP_GATEWAY_URL = os.environ.get("SAP_GATEWAY_URL")  # 환경 변수 추가

def get_gmail_service():
    SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]
    creds = None

    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(AuthRequest())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "agents/client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)

        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)

    return build("gmail", "v1", credentials=creds)

def get_unread_emails():
    try:
        service = get_gmail_service()

        results = service.users().messages().list(
            userId="me", labelIds=["UNREAD"], q="is:unread"
        ).execute()

        messages = results.get("messages", [])

        if not messages:
            print("읽지 않은 메일이 없습니.")
            return "", []  # 빈 문자열과 빈 리스트 반환

        for message in messages:
            msg = service.users().messages().get(userId="me", id=message["id"]).execute()

            headers = msg["payload"]["headers"]
            subject = next(
                (h["value"] for h in headers if h["name"] == "Subject"), "제목 없음"
            )
            sender = next(
                (h["value"] for h in headers if h["name"] == "From"), "보낸 사람 없음"
            )

            print(f"\n제목: {subject}")
            print(f"보낸사람: {sender}")

            # 메일 본문 및 첨부파일 처리
            return process_message_parts(service, msg["payload"], message["id"])

    except Exception as e:
        print(f"오류 발생: {str(e)}")
        return "", []  # 오류 발생 시 빈 문자열과 빈 리스트 반환

def save_excel_as_text(
    filepath, output_folder="text_files", bucket_name="genai-sap-advanced-workshop-gck"
):
    """Excel 파일을 텍스트 파일로 변환하여 저장하고 GCS에 업로드"""
    try:
        # 엑셀 파일 읽기
        df = pd.read_excel(filepath)

        # DataFrame을 CSV 문자열로  (메모리에서 처리)
        csv_buffer = BytesIO()
        df.to_csv(csv_buffer, index=False, encoding="utf-8")
        csv_buffer.seek(0)

        # 고유한 텍스트 파일명 생성
        base_filename = os.path.splitext(os.path.basename(filepath))[0]
        filename = f"{uuid.uuid4()}--{base_filename}.csv"

        # Google Cloud Storage에 업로드
        try:
            bucket = storage_client.get_bucket(bucket_name)
            blob = bucket.blob(f"{output_folder}/{filename}")
            blob.upload_from_file(csv_buffer, content_type="text/csv")

            # 저장된 파일의 GCS 경로 반환
            file_url = f"gs://{bucket_name}/{output_folder}/{filename}"
            print(f"파일이 GCS에 업로드됨: {file_url}")
            return file_url

        except Exception as e:
            print(f"GCS 업로드 중 오류 발생: {str(e)}")
            return None

    except Exception as e:
        print(f"Excel 파일 처리 중 오류 발생: {str(e)}")
        return None

def process_message_parts(service, payload, message_id, folder="attachments"):
    """메일의 각 부분(첨부 파일, 본문 등) 처리"""
    email_text = ""
    attachment_urls = []

    if "parts" in payload:
        for part in payload["parts"]:
            if part.get("filename"):
                if "body" in part and "attachmentId" in part["body"]:
                    try:
                        attachment = (
                            service.users()
                            .messages()
                            .attachments()
                            .get(
                                userId="me",
                                messageId=message_id,
                                id=part["body"]["attachmentId"],
                            )
                            .execute()
                        )

                        file_data = base64.urlsafe_b64decode(attachment["data"])

                        os.makedirs(folder, exist_ok=True)
                        filepath = os.path.join(folder, part["filename"])
                        with open(filepath, "wb") as f:
                            f.write(file_data)
                        print(f"첨부파일 저장됨: {part['filename']}")

                        if filepath.lower().endswith((".xlsx", ".xls")):
                            file_url = save_excel_as_text(filepath)
                            if file_url:
                                attachment_urls.append(file_url)
                                print(f"Excel 파일이 CSV로 변환되어 로드됨: {file_url}")
                    except Exception as e:
                        print(f"첨부파일 처리 중 오류 발생: {str(e)}")
            else:
                sub_text, sub_urls = process_message_parts(
                    service, part, message_id
                )
                email_text += sub_text
                attachment_urls.extend(sub_urls)
    else:
        data = payload.get("body", {}).get("data")
        if data:
            email_text = base64.urlsafe_b64decode(data).decode()
            print(f"메일 내용:\n{email_text}")

    return email_text, attachment_urls

# Configure based on the new best practice example
gen_config = types.GenerateContentConfig(
    temperature = 0,
    top_p = 0.95,
    max_output_tokens = 8192,
    # Include safety_settings within GenerateContentConfig, using strings for categories
    safety_settings = [
        types.SafetySetting(
            category="HARM_CATEGORY_HATE_SPEECH",
            threshold="BLOCK_NONE" # Using enum value equivalent first
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_DANGEROUS_CONTENT",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_SEXUALLY_EXPLICIT",
            threshold="BLOCK_NONE"
        ),
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_NONE"
        ),
    ]
    # Note: The example also included speech_config and response_modalities
    # which are not in the original code. Leaving them out for now.
)

# Gemini 모델을 사용하여 주문 정보 생성
def generate_order_info(email_text, attachment_urls):
    # Define prompt first
    prompt = """A retail store will give you an text file with order details as the Input. You will identify the order details and provide an output as the following json format. You should not add any comment on it. The Box quantity should be arabic number. You can extract the item name from a given image or prompt. However, you should extract the retail store name or the quantity from only the text prompt but not the given image. All parameter values are strings. Set the value as \"\" if null case. Don\'t assume any parameters. **Do not wrap the JSON output in markdown code fences like ```json ... ```.**

    {
    \"function\":\"Z_SALES_ORDER_GENAI_SRV/zsd004Set\",
    \"parameters\":
        {
        \"Bstnk\": \"\",
        \"Auart\": \"\",
        \"Vkorg\": \"\",
        \"Vtweg\": \"\",
        \"Vkbur\": \"\",
        \"Vkgrp\": \"\",
        \"Spart\": \"\",
        \"Edatu\": \"\",
        \"Bstdk\": \"\",
        \"Inco1\": \"\",
        \"Inco2\": \"\",
        \"Bname\": \"\",
        \"Waerk\": \"\",
        \"Kunnr1\": \"\",
        \"Kunnr\": \"\",
        \"Matnr\": \"\",
        \"Kdmat\": \"\",
        \"Wmeng\": \"\",
        \"ItemCateg\": \"\",
        \"Kscha\": \"\",
        \"Kbetr\": \"\",
        \"Xblnr\": \"\",
        \"Kpein\": \"\",
        \"Charg\": \"\"
        }
    }
    If you are not clear on any parameter, provide the output as follows.
    {\\\"function\\\":\\\"None\\\"}

    You should not use the json markdown for the result.

    Input : """

    # Prepare parts for the request
    parts = [Part.from_text(prompt), Part.from_text(email_text)]
    for url in attachment_urls:
        parts.append(Part.from_uri(url, mime_type="text/csv"))

    # Initialize the model
    model_name = os.environ.get("GMAIL_PROCESS_MODEL", "gemini-2.0-flash-001")
    model = GenerativeModel(model_name)

    # Generate content
    try:
        responses = model.generate_content_stream(
            parts=parts,
            config=gen_config,
        )
        print("Generated Order Information:")
        full_response = ""
        for response in responses:
            full_response += response.text
            print(response.text, end="")
        print("\n")
        return full_response
    except Exception as e:
        print(f"Error during generation: {e}")
        return None

def create_order(model_response):
    """SAP Gateway 서비스에 주문 생성 요청"""

    print(f"Raw Response from Model: {model_response}") # Log raw response

    # Extract JSON part from the response string
    json_match = re.search(r'\{.*\}', model_response, re.DOTALL)
    if not json_match:
        error_message = f"모델 응답에서 JSON 객체를 찾을 수 없음 (Could not find JSON object in model response). Response: {model_response}"
        print(error_message)
        return error_message

    json_string = json_match.group(0)
    print(f"Extracted JSON String: {json_string}") # Log extracted JSON

    try:
        # 모델 응답 파싱
        try:
            response_json = json.loads(json_string) # Parse the extracted string
            function_name = response_json.get("function") # Use .get for safety
            parameters = response_json.get("parameters")

            if function_name is None or parameters is None:
                raise KeyError("'function' or 'parameters' key missing in JSON")

        except (json.JSONDecodeError, KeyError, IndexError) as e:
            error_message = f"모델 응답 파싱 오류 (Model response parsing error): {e}"
            print(error_message)
            return error_message

        # Construct the OData service URL
        SAP_IP = "34.64.166.83"
        #SAP_IP = "vhcals4sci.dummy.nodomain"
        url = f"https://{SAP_IP}:44300/sap/opu/odata/SAP/Z_SALES_ORDER_GENAI_SRV"
        get_url = f"{url}/zsd004Set"
        post_url = f"{url}/zsd004Set"

        # 1. Get CSRF token using a HEAD request (more efficient)
        _cookie = ''

        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        # Create a request object with the URL and data
        req_get = Request(get_url, method='GET')  # Use 'POST' or 'GET' as needed

        # Add basic authentication header
        username = "admin"
        password = "Ahfelqm2@13"

        credentials = f'{username}:{password}'

        encoded_credentials = b64encode(credentials.encode('ascii')).decode('ascii')
        # Add headers to the request
        headers = {
            'Content-Type': 'application/json',
            'X-CSRF-Token': 'Fetch',
            'Authorization' : f'Basic {encoded_credentials}'
        }

        # Attach headers to the request
        for key, value in headers.items():
            req_get.add_header(key, value)

        print("debug#1 ")
        # Send the request and receive the response
        with urlopen(req_get, context=ctx) as response:
            # Retrieve all response headers
            response_get_headers = response.getheaders()
            response_get_text = response.read().decode('utf-8')

        print("debug#2 ")
        print("response_get_text: " + response_get_text)
        x_csrf_token = response.getheader('x-csrf-token')

        # Filter out all 'Set-Cookie' headers
        set_cookie_headers = [value for name, value in response_get_headers if name.lower() == 'set-cookie']

        # Initialize a SimpleCookie object
        cookie_jar = cookies.SimpleCookie()

        # Load all cookies into the cookie jar
        for cookie_str in set_cookie_headers:
            cookie_jar.load(cookie_str)

        # Extract the 'SAP_SESSIONID_S4S_100' cookie
        if 'SAP_SESSIONID_S4S_100' in cookie_jar:
            sap_session_cookie = cookie_jar['SAP_SESSIONID_S4S_100']
            print('SAP_SESSIONID_S4S_100=', sap_session_cookie.value)
            _cookie = sap_session_cookie.value
        else:
            print('SAP_SESSIONID_S4S_100 cookie not found.')

        print("cookie: " + _cookie)
        print("x-csrf-token: " + x_csrf_token)

        # 3. Send POST request with CSRF token and parameters
        headers = {
            'Content-Type': 'application/json',
            'X-CSRF-Token': x_csrf_token,
            'Authorization' : f'Basic {encoded_credentials}',
            'cookie': f'SAP_SESSIONID_S4S_100={_cookie}'
        }

        data = json.dumps(parameters).encode('utf-8')

        req_post = Request(post_url, data=data, method='POST')  # Use 'POST' or 'GET' as needed
        # Attach headers to the request
        for key, value in headers.items():
            req_post.add_header(key, value)

        # Send the request and receive the response
        with urlopen(req_post, context=ctx) as sap_response:
            # Retrieve all response headers
            response_post_headers = sap_response.getheaders()
            status_code = sap_response.getcode()

            response_post_text = sap_response.read().decode('utf-8')
    
        print('response_post_text :' + response_post_text)
        xroot = ET.fromstring(response_post_text)

        return "Orders created successfully"

    except Exception as e:
        print(f"오류 발생: {e}")


if __name__ == "__main__":
    email_text, attachment_urls = get_unread_emails()

    # Check if there are any attachments and use the first one
    # document_url = attachment_urls[0] if attachment_urls else None

    # generate_with_gemini 함수를 호출하여 응답을 받음
    model_response = generate_order_info(email_text, attachment_urls)

    # create_order 함수에 모델 응답 전달
    if model_response:
        create_order(model_response)

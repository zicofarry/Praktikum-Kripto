import os, pickle
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

SCOPES = ['https://www.googleapis.com/auth/drive',
          'https://www.googleapis.com/auth/documents']

DOCX_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '2406010_laporan.docx')
TARGET_DOC_ID = '1qglhoi2rKr1MP8wcj3ZzpNqull4ShV9RJjt6KldjZ6s'

def authenticate():
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as f:
            creds = pickle.load(f)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('token.pickle', 'wb') as f:
            pickle.dump(creds, f)
    return creds

def main():
    creds = authenticate()
    drive = build('drive', 'v3', credentials=creds)

    # Upload DOCX, convert to Google Docs
    media = MediaFileUpload(DOCX_PATH, mimetype='application/vnd.openxmlformats-officedocument.wordprocessingml.document',
                            resumable=True)
    uploaded = drive.files().create(
        media_body=media,
        body={
            'name': '2406010_laporan',
            'mimeType': 'application/vnd.google-apps.document',
        },
        fields='id'
    ).execute()
    new_doc_id = uploaded.get('id')

    print(f'Dokumen baru berhasil dibuat!')
    print(f'Link: https://docs.google.com/document/d/{new_doc_id}/edit')

    # Copy content to existing doc
    # First, get all content from new doc
    docs = build('docs', 'v1', credentials=creds)
    source = docs.documents().get(documentId=new_doc_id).execute()

    # Build requests to copy content to target doc
    requests = []
    for el in source.get('body', {}).get('content', []):
        if 'paragraph' in el:
            para = el['paragraph']
            for run in para.get('elements', []):
                if 'textRun' in run:
                    text = run['textRun'].get('content', '')
                    style = run['textRun'].get('textStyle', {})
                    if text.strip() or text == '\n':
                        requests.append({
                            'insertText': {
                                'location': {'index': 9999999},
                                'text': text
                            }
                        })
                        requests.append({
                            'updateTextStyle': {
                                'range': {'startIndex': 9999999, 'endIndex': 9999999 + len(text)},
                                'textStyle': {
                                    'bold': style.get('bold', False),
                                    'fontSize': style.get('fontSize', {'magnitude': 11, 'unit': 'PT'}),
                                },
                                'fields': 'bold,fontSize'
                            }
                        })
        elif 'table' in el:
            # Skip tables for now - too complex
            pass

    print(f'Source doc: https://docs.google.com/document/d/{new_doc_id}/edit')

if __name__ == '__main__':
    main()

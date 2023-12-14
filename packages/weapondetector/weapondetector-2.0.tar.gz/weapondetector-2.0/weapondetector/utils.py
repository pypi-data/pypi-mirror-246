
import json
import boto3
import firebase_admin
from firebase_admin import credentials, firestore
import requests
import os
from time import gmtime, strftime

# from encryption import encrypt

encryption_key = "2b7e151628aed2a6abf7158809cf4f3c"

main_path = os.path.dirname(os.path.abspath(__file__))
cred = credentials.Certificate(f"{main_path}/secret-key.json")
app = firebase_admin.initialize_app(cred)
store = firestore.client()

school_id = os.environ["SCHOOLD_ID"]
print("School ID Received")

collection_name = 'schools'
fcm_field = 'school_fcm_token'

doc_ref = store.collection(collection_name).document(school_id)
fcm = doc_ref.get().get(fcm_field)

flags = {'alerts': 0,
         'critical_alerts': 0,
         'danger_alerts': 0,
         'red_alerts': 0}

s3 = boto3.resource(
    service_name='s3',
    region_name='eu-north-1',
    aws_access_key_id='AKIA4VAG3ZGWG3XQC2XJ',
    aws_secret_access_key='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'
)


def send_notification(device_tokens, data_dict):
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=AAAAOJr4TFQ:APA91bH_UTb1rB3TjD7gDScjUwUgnvO29ZZ6e5e6a6klg81rmxGdlnn2DkEtu2kHAk0wd9MbAqB6pqhp2ys7ujiAt87DDmkxPMzkUtQkSOdsZ0o-ScgYyYLSdtexpUgj3RB0gnP3VTm2',
    }

    payload = {
        'registration_ids': device_tokens,  # A list of device tokens
        'notification': {
            'title': f"Weapon Detected in {data_dict['location']}",
            'body': 'Tap to View the Video',

        },
        'data': data_dict
    }

    # print(payload)
    response = requests.post(
        'https://fcm.googleapis.com/fcm/send',
        headers=headers,
        data=json.dumps(payload),
    )
    return response


def uploading_thread(video_file_path, img_file_path, camera_name, acc):

    video_f_name = video_file_path.split('/')[-1]
    img_f_name = img_file_path.split('/')[-1]

    print(f"Uploading: {img_f_name}")
    s3.Bucket('weapondetection').upload_file(Filename=img_file_path, Key=f'thumbnails/{img_f_name}')
    print(f"Successfully Uploaded: {img_f_name}")

    print(f"Uploading: {video_f_name}")
    s3.Bucket('weapondetection').upload_file(Filename=video_file_path, Key=f'videos/{video_f_name}')
    print(f"Successfully Uploaded: {video_f_name}")

    vid_url = f"https://d3j29qile9de9p.cloudfront.net/videos/{video_f_name}"
    img_url = f"https://d3j29qile9de9p.cloudfront.net/thumbnails/{img_f_name}"

    current_time = strftime("%Y-%m-%d %H:%M:%S", gmtime())

    data = {'date_time': current_time,
            'location': camera_name,
            'thumbnail_url': img_url,
            'video_url': vid_url,
            'title': 'Weapon'
            }

    if acc <= 0.75:
        doc = 'alerts'

    elif (acc > 0.75 and acc <= 0.80):
        doc = 'critical_alerts'

    elif (acc > 0.80 and acc <= 0.85):
        doc = 'danger_alerts'

    elif (acc > 0.85):
        doc = 'red_alerts'

    notification_data = doc_ref.collection('notifications').document(doc)

    if flags[doc] == 0:

        resp = notification_data.set({
            'notification_list': firestore.ArrayUnion([data])
        })
        flags[doc] = 1
    else:
        resp = notification_data.update({
            'notification_list': firestore.ArrayUnion([data])
        })

    resp = doc_ref.update({
        'recent_detection': data
    })

    if resp:
        print(f"Successfully Uploaded {video_f_name} to Firebase!")

    resp = send_notification([fcm], data)

    while resp.status_code != 200:
        resp = send_notification([fcm], data)

    if resp.status_code == 200:
        print("Notification Sent Successfully!")

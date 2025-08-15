from flask import Flask, jsonify
import requests
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
import urllib.parse

app = Flask(__name__)

_sym_db = _symbol_database.Default()

DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(
    b'\n\ndata.proto\"\xbb\x01\n\x04\x44\x61ta\x12\x0f\n\x07\x66ield_2\x18\x02 \x01(\x05\x12\x1e\n\x07\x66ield_5\x18\x05 \x01(\x0b\x32\r.EmptyMessage\x12\x1e\n\x07\x66ield_6\x18\x06 \x01(\x0b\x32\r.EmptyMessage\x12\x0f\n\x07\x66ield_8\x18\x08 \x01(\t\x12\x0f\n\x07\x66ield_9\x18\t \x01(\x05\x12\x1f\n\x08\x66ield_11\x18\x0b \x01(\x0b\x32\r.EmptyMessage\x12\x1f\n\x08\x66ield_12\x18\x0c \x01(\x0b\x32\r.EmptyMessage\"\x0e\n\x0c\x45mptyMessageb\x06proto3'
)

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'data_pb2', _globals)

Data = _sym_db.GetSymbol('Data')
EmptyMessage = _sym_db.GetSymbol('EmptyMessage')

key = bytes([89, 103, 38, 116, 99, 37, 68, 69, 117, 104, 54, 37, 90, 99, 94, 56])
iv = bytes([54, 111, 121, 90, 68, 114, 50, 50, 69, 51, 121, 99, 104, 106, 77, 37])

# ... نفس الكود السابق ...

import json
from flask import Response

@app.route('/update_bio/<token>/<path:bio>', methods=['GET'])
def update_bio(token, bio):
    bio = urllib.parse.unquote(bio)
    if len(bio) >= 180:
        return Response(json.dumps({'error': 'Bio length must be less than 180 characters'}, ensure_ascii=False), 
                        content_type='application/json; charset=utf-8', status=400)

    data_msg = Data()
    data_msg.field_2 = 17
    data_msg.field_5.CopyFrom(EmptyMessage())
    data_msg.field_6.CopyFrom(EmptyMessage())
    data_msg.field_8 = bio
    data_msg.field_9 = 1
    data_msg.field_11.CopyFrom(EmptyMessage())
    data_msg.field_12.CopyFrom(EmptyMessage())

    data_bytes = data_msg.SerializeToString()
    padded_data = pad(data_bytes, AES.block_size)
    cipher = AES.new(key, AES.MODE_CBC, iv)
    encrypted_data = cipher.encrypt(padded_data)

    url = "https://clientbp.ggblueshark.com/UpdateSocialBasicInfo"
    headers = {
        'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; ASUS_Z01QD Build/PI)',
        'Connection': 'Keep-Alive',
        'Expect': '100-continue',
        'Authorization': f'Bearer {token}',
        'X-Unity-Version': '2018.4.11f1',
        'X-GA': 'v1 1',
        'ReleaseVersion': 'OB50',
        'Content-Type': 'application/octet-stream',
    }

    resp = requests.post(url, headers=headers, data=encrypted_data)

    response_data = {
        'message': 'تم تغيير البايو',
        'bio_new': bio,
        'developer': 'BNGX',
    }

    json_str = json.dumps(response_data, ensure_ascii=False)
    return Response(json_str, content_type='application/json; charset=utf-8')

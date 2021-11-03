import requests
import json

url = "https://10.181.35.51/configmgmt/api/v1/jobs"

payload = json.dumps({
  "data": {
    "type": "jobs",
    "attributes": {
      "maxConnections": 10,
      "scheduleTime": "2021-02-26T15:04:06Z",
      "scripts": [
        {
          "scriptName": "netconfCutThrough",
          "inputs": [
            {
              "cmdFile": "10x_L2VPN_create_v1",
              "protocolType": "netconf"
            }
          ],
          "relationships": {
            "userdata": {
              "data": {
                "type": "userdatas",
                "id": "0"
              }
            }
          }
        }
      ]
    },
    "relationships": {
      "connectionAttributes": {
        "data": [
          {
            "type": "connectionAttributes",
            "id": "5164_20"
          }
        ]
      }
    }
  },
  "included": [
    {
      "id": "5164_20",
      "type": "connectionAttributes",
      "attributes": {
        "neName": "5164_20",
        "neType": "5164",
        "typeGroup": "PN10x"
      }
    },
    {
      "type": "userdatas",
      "id": "0",
      "attributes": {
        "CLASSIFIER_NAME": "VLAN555",
        "CLASSIFIER_PRECEDENCE": "555",
        "VLAN_ID": "555",
        "FD_NAME": "l2vpn555",
        "FP_NAME": "fpl2vpn555_P2",
        "MODE": "vpls",
        "PORT_NUM": "2",
        "MTU_SIZE": "1500",
        "PEER_IP": "192.168.127.21",
        "PW_ID": "111555",
        "PW_NAME": "l2vpn555_PW1",
        "PW_MODE": "mesh",
        "NAME": "l2vpn555",
        "SVC_TYPE": "ethernet",
        "SIGNALING": "ldp"
      }
    }
  ]
})
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer a3467cb02c1302ad2e84',
  'Accept': 'application/json',
  'Cookie': 'uac.csrftoken=K1GQJ1uaJdJhVmUFsjnYVpJMkdTTWxNE'
}

response = requests.request("POST", url, headers=headers, data=payload, verify=False)

print(response.text)

import requests


def pushevpl(nodeName, uniPort, cVid, PEERLbkIP):

    url = "https://10.181.35.51/configmgmt/api/v1/jobs"

    prepayload = {
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
                "id": f"{nodeName}"
            }
            ]
        }
        }
    },
    "included": [
        {
        "id": f"{nodeName}",
        "type": "connectionAttributes",
        "attributes": {
            "neName": f"{nodeName}",
            "neType": "5164",
            "typeGroup": "PN10x"
        }
        },
        {
        "type": "userdatas",
        "id": "0",
        "attributes": {
            "CLASSIFIER_NAME": f"VLAN{cVid}",
            "CLASSIFIER_PRECEDENCE": f"{cVid}",
            "VLAN_ID": f"{cVid}",
            "FD_NAME": f"l2vpn{cVid}",
            "FP_NAME": f"fpl2vpn{cVid}_P{uniPort}",
            "MODE": "vpls",
            "PORT_NUM": f"{uniPort}",
            "MTU_SIZE": "1500",
            "PEER_IP": f"{PEERLbkIP}",
            "PW_ID": f"111{cVid}",
            "PW_NAME": f"l2vpn{cVid}_PW1",
            "PW_MODE": "mesh",
            "NAME": f"l2vpn{cVid}",
            "SVC_TYPE": "ethernet",
            "SIGNALING": "ldp"
        }
        }
    ]
    }

    payload = json.dumps(prepayload)

    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer 2337d80c76737961da9f',
    'Accept': 'application/json',
    'Cookie': 'uac.csrftoken=K1GQJ1uaJdJhVmUFsjnYVpJMkdTTWxNE'
    }
    response = requests.request("POST", url, headers=headers, data=payload, verify=False)

    print(response.status_code)
    print(response.text)
    print(response)

    return response

def pullevpl(nodeName, uniPort, cVid, PEERLbkIP):
    print("hit delete function")
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
                "cmdFile": "10x_L2VPN_delete_v1",
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
                "id": f"{nodeName}"
            }
            ]
        }
        }
    },
    "included": [
        {
        "id": f"{nodeName}",
        "type": "connectionAttributes",
        "attributes": {
            "neName": f"{nodeName}",
            "typeGroup": "PN10x"
        }
        },
        {
        "type": "userdatas",
        "id": "0",
        "attributes": {
            "NAME": f"l2vpn{cVid}",
            "PW_NAME": f"l2vpn{cVid}_PW1",
            "FP_NAME": f"fpl2vpn{cVid}_P{uniPort}",
            "FD_NAME": f"l2vpn{cVid}",
            "CLASSIFIER_NAME": f"VLAN{cVid}"
        }
        }
    ]
    })
    headers = {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer e4655c09b56d0ec3f6f3',
    'Accept': 'application/json',
    'Cookie': 'uac.csrftoken=K1GQJ1uaJdJhVmUFsjnYVpJMkdTTWxNE'
    }

    response = requests.request("POST", url, headers=headers, data=payload, verify=False)
    print(response.text)

    return response

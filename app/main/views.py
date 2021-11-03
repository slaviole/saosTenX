from flask import Flask, render_template, session, redirect, url_for, flash
from .. import db
from ..models  import Node
from . import main
from .forms import * #Flasky only pulls in NameForm but it only has one. OK.
import json
import requests
from . import ncModule
from . import restModule

from mytenxtemplates import *
from ncclient import manager
import untangle

# 10.x Startup Views
# ==================

@main.route('/sethostname', methods=['GET', 'POST'])
def sethostname():
    hostName = None
    form = SETHostName()
    if form.validate_on_submit():
        hostName = form.hostName.data
    return render_template('hostname.html', form=form, hostName=hostName)

@main.route('/oobmgmt', methods=['GET', 'POST'])
def oobmgmt():
    oobIP = None
    oobSubnet = None
    oobGateway = None
    defaultRoute = None
    defaultRouteSubnet = None
    form = OOBForm()
    if form.validate_on_submit():
        oobIP = form.oobIP.data
#        form.oobIP.data = ''
        oobSubnet = form.oobSubnet.data
#        form.oobSubnet.data = ''
        defaultRoute = form.defaultRoute.data
        defaultRouteSubnet = form.defaultRouteSubnet.data
        oobGateway = form.oobGateway.data
#        form.oobGateway.data = ''
    return render_template('oobmgmt.html', form=form, oobIP=oobIP, oobSubnet=oobSubnet, defaultRoute=defaultRoute, defaultRouteSubnet=defaultRouteSubnet, oobGateway=oobGateway)

@main.route('/addntp', methods=['GET', 'POST'])
def addntp():
    ntpIP = None
    form = ADDntp()
    if form.validate_on_submit():
        ntpIP = form.ntpIP.data
    return render_template('addntp.html', form=form, ntpIP=ntpIP)

@main.route('/addlicenseserver', methods=['GET', 'POST'])
def addlicenseserver():
    licenseServerIP = None
    form = ADDlicenseServer()
    if form.validate_on_submit():
        licenseServerIP = form.licenseServerIP.data
    return render_template('addlicenseserver.html', form=form, licenseServerIP=licenseServerIP)


# Transport Infrastructure Views
# ==============================

def EXPANDIP(IPaddress):
    indices = []
    start = 0
    for num, char in enumerate(IPaddress):
        if char == ".":
            indices.append(IPaddress[start:num].zfill(3))
            start = num + 1
            if len(indices) == 3:
                indices.append(IPaddress[start:].zfill(3))
    tempIP = ''.join(indices)
    newformatIP = tempIP[0:4] + "." + tempIP[4:8] + "." + tempIP[8:]
    return newformatIP


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
    'Authorization': 'Bearer e4655c09b56d0ec3f6f3',
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

@main.route('/')
def index():
    return render_template('index.html')



@main.route('/createport', methods=['GET', 'POST'])
def createport():
    logicalPort = None
    vlanId = None
    dataPortIp = None
    peerIp = None
    dataPortMask = None
    form = CREATEPort()
    if form.validate_on_submit():
        logicalPort = form.logicalPort.data
        vlanId = form.vlanId.data
        dataPortIp = form.dataPortIp.data
        peerIp = form.peerIp.data
        dataPortMask = form.dataPortMask.data
    return render_template('createPort.html', form=form, logicalPort=logicalPort, vlanId=vlanId, dataPortIp=dataPortIp, peerIp=peerIp, dataPortMask=dataPortMask)

@main.route('/createlbk', methods=['GET', 'POST'])
def createlbk():
    form = CREATELbk()
    if form.validate_on_submit():
        session['lbkIP'] = form.lbkIP.data
        return redirect(url_for('.createlbk'))
    return render_template('createLbk.html', form=form, lbkIP=session.get('lbkIP'))

@main.route('/addsr', methods=['GET', 'POST'])
def addsr():
    lbkIP = None
    startSid = None
    isisLevel = None
    form = ADDSr()
    if form.validate_on_submit():
        lbkIP = form.lbkIP.data
        startSid = form.startSid.data
        isisLevel = form.isisLevel.data
    return render_template('addsr.html', form=form, lbkIP=lbkIP, startSid=startSid, isisLevel=isisLevel)

@main.route('/addbgp', methods=['GET', 'POST'])
def addbgp():
    lbkIP = None
    ASNum = None
    form = ADDBgp()
    if form.validate_on_submit():
        lbkIP = form.lbkIP.data
        ASNum = form.ASNum.data
    return render_template('addbgp.html', form=form, lbkIP=lbkIP, ASNum=ASNum)

@main.route('/addbgppeer', methods=['GET', 'POST'])
def addbgppeer():
    ASNum = None
    PEERLbkIP = None
    form = ADDBgpPeer()
    if form.validate_on_submit():
        ASNum = form.ASNum.data
        PEERLbkIP = form.PEERLbkIP.data
    return render_template('addbgppeer.html', form=form, ASNum=ASNum, PEERLbkIP=PEERLbkIP)

@main.route('/createl3vpn', methods=['GET', 'POST'])
def createl3vpn():
    ASNum = None
    uniPort = None
    cVid = None
    vrfIP = None
    vrfMask = None
    rtTarget = None
    rtDist = None
    form = CREATEL3vpn()
    if form.validate_on_submit():
        ASNum = form.ASNum.data
        uniPort =  form.uniPort.data
        cVid = form.cVid.data
        vrfIP = form.vrfIP.data
        vrfMask = form.vrfMask.data
        rtTarget = form.rtTarget.data
        rtDist = form.rtDist.data
    return render_template('createl3vpn.html', form=form, ASNum=ASNum, uniPort=uniPort, cVid=cVid, vrfIP=vrfIP, vrfMask=vrfMask, rtTarget=rtTarget, rtDist=rtDist)

@main.route('/createevpnvpws', methods=['GET', 'POST'])
def createevpnvpws():
    ASNum = None
    uniPort = None
    cVid = None
    rtTarget = None
    rtDist = None
    form = CREATEEvpnVpws()
    if form.validate_on_submit():
        ASNum = form.ASNum.data
        uniPort =  form.uniPort.data
        cVid = form.cVid.data
        rtTarget = form.rtTarget.data
        rtDist = form.rtDist.data
    return render_template('createevpnvpws.html', form=form, ASNum=ASNum, uniPort=uniPort, cVid=cVid, rtTarget=rtTarget, rtDist=rtDist)



@main.route('/enabletldp', methods=['GET', 'POST'])
def enabletldp():
    lbkIP = None
    form = ENABLETLdp()
    if form.validate_on_submit():
        lbkIP = form.lbkIP.data
    return render_template('enabletldp.html', form=form, lbkIP=lbkIP)

@main.route('/createevpline', methods=['GET', 'POST'])
def createevpline():
    uniPort = None
    cVid = None
    PEERLbkIP = None
    form = CREATEEvpLine()
    if form.validate_on_submit():
        uniPort =  form.uniPort.data
        cVid = form.cVid.data
        PEERLbkIP = form.PEERLbkIP.data
    return render_template('createevpline.html', form=form, uniPort=uniPort, cVid=cVid, PEERLbkIP=PEERLbkIP)




@main.route('/createisis', methods=['GET', 'POST'])
def createisis():
    areaId = None
    lbkIp = None
    lbkIpXtd = None
    isisLevel = None
    form = CREATEIsis()
    if form.validate_on_submit():
        areaId = form.areaId.data
        lbkIp = form.lbkIp.data
        lbkIpXtd = EXPANDIP(form.lbkIp.data)
        isisLevel = form.isisLevel.data
    return render_template('createIsisInst.html', form=form, areaId=areaId, lbkIp=lbkIp, lbkIpXtd=lbkIpXtd, isisLevel=isisLevel)

@main.route('/setettps', methods=['GET', 'POST'])
def setettps():
    logicalPort = None
    portSpeed = None
    form = SETEttps()
    if form.validate_on_submit():
        logicalPort = form.logicalPort.data
        portSpeed = form.portSpeed.data
    return render_template('setEttps.html', form=form, portSpeed=portSpeed, logicalPort=logicalPort)




# Virtualized Edge config generation

@main.route('/base6x', methods=['GET', 'POST'])
def base6x():
    nodeName = None
    nodeIP = None
    nodeSubnet = None
    defaultGateway = None
    form = BASE6x()
    if form.validate_on_submit():
        nodeName = form.nodeName.data
        nodeIP = form.nodeIP.data
        nodeSubnet = form.nodeSubnet.data
        defaultGateway = form.defaultGateway.data
    return render_template('base6x.html', form=form, nodeName=nodeName, nodeIP=nodeIP, nodeSubnet=nodeSubnet, defaultGateway=defaultGateway)

@main.route('/versa6x', methods=['GET', 'POST'])
def versa6x():
    wan0 = None
    wan1 = None
    lan0 = None
    lan1 = None
    form = VERSA6x()
    if form.validate_on_submit():
        wan0 = form.wan0.data
        wan1 = form.wan1.data
        lan0 = form.lan0.data
        lan1 = form.lan1.data
    return render_template('versa6x.html', form=form, wan0=wan0, wan1=wan1, lan0=lan0, lan1=lan1)

@main.route('/vyos6x', methods=['GET', 'POST'])
def vyos6x():
    wan0 = None
    lan0 = None
    form = VYOS6x()
    if form.validate_on_submit():
        wan0 = form.wan0.data
        lan0 = form.lan0.data
    return render_template('vyos6x.html', form=form, wan0=wan0, lan0=lan0)


@main.route('/vEdgeBase', methods=['GET', 'POST'])
def vedgebase():
    oobIP = None
    oobSubnet = None
    oobGateway = None
    defaultRoute = None
    defaultRouteSubnet = None
    ntpIP = None
    licenseServerIP = None
    form = FRUBase()
    if form.validate_on_submit():
        oobIP = form.oobIP.data
        oobSubnet = form.oobSubnet.data
        defaultRoute = form.defaultRoute.data
        defaultRouteSubnet = form.defaultRouteSubnet.data
        oobGateway = form.oobGateway.data
        ntpIP = form.ntpIP.data
        licenseServerIP = form.licenseServerIP.data
    return render_template('vedgebase.html', form=form, oobIP=oobIP, oobSubnet=oobSubnet, defaultRoute=defaultRoute, defaultRouteSubnet=defaultRouteSubnet, oobGateway=oobGateway, ntpIP=ntpIP, licenseServerIP=licenseServerIP)

@main.route('/vyosDownload', methods=['GET', 'POST'])
def vyosDownload():
    form = VYOSDownload()
#    if form.validate_on_submit():
#        pass
    return render_template('vyosdownload.html', form=form)

@main.route('/vnfspec', methods=['GET', 'POST'])
def vnfspec():
    imageName = None
    numCpus = None
    ram = None
    form = VNFSpec()
    if form.validate_on_submit():
        imageName = form.imageName.data
        numCpus = form.numCpus.data
        ram = form.ram.data
    return render_template('vnfspec.html', form=form, imageName=imageName, numCpus=numCpus, ram=ram)

@main.route('/createclassifier', methods=['GET', 'POST'])
def createclassifier():
    return render_template('createclassifier.html')

@main.route('/createsff', methods=['GET', 'POST'])
def createsff():
    return render_template('createsff.html')





# Node Config
# ==============
'''
@main.route('/showcfg', methods=['GET', 'POST'])
def showcfg():
    nodeName = None
    cfgObj = None
    TenXObj = None
    form = SHOWCfgPulldown()
    if form.validate_on_submit():
        nodeToDisplay = Node.query.filter_by(nodeName=str(form.nodeName.data)).first()
        cfgObj = str(form.cfgObj.data)
        try:
            TenXObj = ncModule.get_nc_obj(nodeToDisplay,cfgObj)
        except:
            return render_template('404.html')
    return render_template('showCfg.html', form=form, cfgObj=cfgObj, TenXObj = TenXObj)
'''

@main.route('/configevpl', methods=['GET', 'POST'])
def configevpl():
    nodeName = None
    uniPort = None
    cVid = None
    PEERLbkIP = None
    pushResponse = None
    form = CONFIGevpl()
    if form.validate_on_submit():
        nodeName = form.nodeName.data
        uniPort =  form.uniPort.data
        cVid = form.cVid.data
        PEERLbkIP = form.PEERLbkIP.data
        try:
            pushResponse = pushevpl(nodeName, uniPort, cVid, PEERLbkIP)
        except:
            print("Hit the except case")
            return render_template('404.html')
#    return redirect(url_for('main.configevpl'))
    return render_template('configevpl.html', form=form, nodeName=nodeName, uniPort=uniPort, cVid=cVid, PEERLbkIP=PEERLbkIP, pushResponse=pushResponse)

@main.route('/deleteevpl', methods=['GET', 'POST'])
def deleteevpl():
    nodeName = None
    uniPort = None
    cVid = None
    PEERLbkIP = None
    pullResponse = None
    form = DELETEevpl()
    if form.validate_on_submit():
        nodeName = form.nodeName.data
        uniPort =  form.uniPort.data
        cVid = form.cVid.data
        PEERLbkIP = form.PEERLbkIP.data
        try:
            pullResponse = pullevpl(nodeName, uniPort, cVid, PEERLbkIP)
        except:
            return render_template('404.html')
    return render_template('deleteevpl.html', form=form, nodeName=nodeName, uniPort=uniPort, cVid=cVid, PEERLbkIP=PEERLbkIP, pullResponse=pullResponse)

@main.route('/configevplaz', methods=['GET', 'POST'])
def configevplaz():
    nodeNameA = None
    uniPortA = None
    cVid = None
    PEERLbkIPA = None
    pushResponseA = None
    nodeNameZ = None
    uniPortZ = None
    PEERLbkIPZ = None
    pushResponseZ = None
    form = CONFIGevplAZ()
    if form.validate_on_submit():
        nodeNameA = form.nodeNameA.data
        uniPortA =  form.uniPortA.data
        cVid = form.cVid.data
        PEERLbkIPA = form.PEERLbkIPA.data
        nodeNameZ = form.nodeNameZ.data
        uniPortZ =  form.uniPortZ.data
        PEERLbkIPZ = form.PEERLbkIPZ.data
        try:
            pushResponseA = pushevpl(nodeNameA, uniPortA, cVid, PEERLbkIPA)
        except:
            return render_template('404.html')
        try:
            pushResponseZ = pushevpl(nodeNameZ, uniPortZ, cVid, PEERLbkIPZ)
        except:
            return render_template('404.html')
#    return redirect(url_for('main.configevpl'))
    return render_template('configevplaz.html', form=form, nodeNameA=nodeNameA, uniPortA=uniPortA, cVid=cVid, PEERLbkIPA=PEERLbkIPA, nodeNameZ=nodeNameZ, uniPortZ=uniPortZ, PEERLbkIPZ=PEERLbkIPZ, pushResponseA=pushResponseA, pushResponseZ=pushResponseZ)

@main.route('/deleteevplaz', methods=['GET', 'POST'])
def deleteevplaz():
    nodeNameA = None
    uniPortA = None
    cVid = None
    PEERLbkIPA = None
    pullResponseA = None
    nodeNameZ = None
    uniPortZ = None
    PEERLbkIPZ = None
    pullResponseZ = None
    form = CONFIGevplAZ()
    if form.validate_on_submit():
        nodeNameA = form.nodeNameA.data
        uniPortA =  form.uniPortA.data
        cVid = form.cVid.data
        PEERLbkIPA = form.PEERLbkIPA.data
        nodeNameZ = form.nodeNameZ.data
        uniPortZ =  form.uniPortZ.data
        PEERLbkIPZ = form.PEERLbkIPZ.data
        try:
            pullResponseA = pullevpl(nodeNameA, uniPortA, cVid, PEERLbkIPA)
        except:
            return render_template('404.html')
        try:
            pullResponseZ = pullevpl(nodeNameZ, uniPortZ, cVid, PEERLbkIPZ)
        except:
            return render_template('404.html')
    return render_template('deleteevplaz.html', form=form, nodeNameA=nodeNameA, uniPortA=uniPortA, cVid=cVid, PEERLbkIPA=PEERLbkIPA, nodeNameZ=nodeNameZ, uniPortZ=uniPortZ, PEERLbkIPZ=PEERLbkIPZ, pullResponseA=pullResponseA, pullResponseZ=pullResponseZ)

@main.route('/undoevplaz', methods=['GET', 'POST'])
def undoevplaz():
    form = CONFIGevplAZ()
    if form.validate_on_submit():
        nodeNameA = form.nodeNameA.data
        uniPortA =  form.uniPortA.data
        cVid = form.cVid.data
        PEERLbkIPA = form.PEERLbkIPA.data
        nodeNameZ = form.nodeNameZ.data
        uniPortZ =  form.uniPortZ.data
        PEERLbkIPZ = form.PEERLbkIPZ.data
        try:
            pullResponseA = restModule.pullevpl(nodeNameA, uniPortA, cVid, PEERLbkIPA)
        except:
            return render_template('404.html')
        try:
            pullResponseZ = restModule.pullevpl(nodeNameZ, uniPortZ, cVid, PEERLbkIPZ)
        except:
            return render_template('404.html')
    return render_template('deleteevplaz.html', form=form, nodeNameA=nodeNameA, uniPortA=uniPortA, cVid=cVid, PEERLbkIPA=PEERLbkIPA, nodeNameZ=nodeNameZ, uniPortZ=uniPortZ, PEERLbkIPZ=PEERLbkIPZ, pullResponseA=pullResponseA, pullResponseZ=pullResponseZ)




"""
@main.route('/pushcfg', methods=['GET', 'POST'])
def pushcfg():
    try:
        pushResponse = pushevpl("555")
    except:
        return render_template('404.html')
#    return render_template('createuniti.html', nodeName=nodeName, uniPort=uniPort, cVid=cVid, PEERLbkIP=PEERLbkIP)
    return redirect(url_for('main.configevpl')) 

@main.route('/deletecfg', methods=['GET', 'POST'])
def deletecfg():
    nodeName = None
    uniPort = None
    cVid = None
    PEERLbkIP = None
    try:
        pushResponse = deleteevpl()
    except:
        return render_template('404.html')
#    return render_template('createuniti.html', nodeName=nodeName, uniPort=uniPort, cVid=cVid, PEERLbkIP=PEERLbkIP)
    return redirect(url_for('main.configevpl')) 
"""
# S3 Lab Admin
# =============

@main.route('/backupnodes', methods=['GET', 'POST'])
def backupnodes():
    nodeNames = None
    projectName = None
    suffix = None
    form = BACKUPNodes()
    if form.validate_on_submit():
        nodeNames = form.nodeNames.data
        print(nodeNames)
        projectName = form.projectName.data
        print(projectName)
        suffix = form.suffix.data
        print(suffix)
        # This is where the try/except block goes
    return render_template('backupNodes.html', form=form, nodeNames=nodeNames, projectName=projectName, suffix=suffix)


# Admin
# =====

@main.route('/showcfg', methods=['GET', 'POST'])
def showcfg():
    nodeName = None
    cfgObj = None
    TenXObj = None
    form = SHOWCfgPulldown()
    if form.validate_on_submit():
        nodeToDisplay = Node.query.filter_by(nodeName=str(form.nodeName.data)).first()
        cfgObj = str(form.cfgObj.data)
        try:
            TenXObj = ncModule.get_nc_obj(nodeToDisplay,cfgObj)
        except:
            return render_template('404.html')
    return render_template('showCfg.html', form=form, cfgObj=cfgObj, TenXObj = TenXObj)

@main.route('/addnode', methods=['GET', 'POST'])
def addnode():
    form = ADDNode()
    if form.validate_on_submit():
        node = Node.query.filter_by(nodeName=form.nodeName.data).first()
        if node is None:
            node = Node(nodeName=form.nodeName.data, nodeIP=form.nodeIP.data, userID=form.userID.data, password=form.password.data)
            db.session.add(node)
            db.session.commit()
            session['known'] = False
        else:
            session['known'] = True
        session['node'] = form.nodeName.data
        form.nodeName.data = ''
    return render_template('addNode.html', form=form, nodelist=Node.query.all())

@main.route('/deletenode', methods=['GET', 'POST'])
def deletenode():
    form = QueryAllNode()
#    form = DELETENode()
    if form.validate_on_submit():
        nodeToDelete = Node.query.filter_by(nodeName=str(form.nodeName.data)).first()
        if nodeToDelete is not None:
            db.session.delete(nodeToDelete)
            db.session.commit()
            return redirect(url_for('.deletenode'))
        form.nodeName.data = ''
    return render_template('deleteNode.html', form=form, nodelist=Node.query.all())


def edit_nc_obj(nc_creds, template):
    ''' Takes D-NFVI server login credentials, makes a Netconf get for all config and oper data.
        Returns an Untangle object with the parsed xml tree.
    '''
    print()
    with manager.connect(host=nc_creds['ip'],
                             port=830,
                             username=nc_creds['user'],
                             password=nc_creds['pwd'],
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False
                             ) as netconf_manager:

        data = netconf_manager.edit_config(target='running', config=template)
    data_str = str(data)
    d_obj = untangle.parse(data_str)
    return d_obj


# Endpoint below will push netconf to device using list of nodes
@main.route('/nc_createclassifier', methods=['GET', 'POST'])
def nc_createclassifier():
    nodeToConfig = None
    vlanId = None
    form = CREATEclassifier()
    if form.validate_on_submit():
        nodeToConfig = Node.query.filter_by(nodeName=str(form.nodeName.data)).first()
        vlanId = form.vlanId.data
        vlanIdDict = {'operation': 'replace', 'vlanid': vlanId}
        print(vlanIdDict)
        rendered_template = editClassifiers.render(vlanIdDict)
        print(rendered_template)
        creds = {'ip': "10.181.34.2",
        'user': 'user',
        'pwd': 'ciena123'
        }
        dnfvi_obj = edit_nc_obj(creds, rendered_template)
    return render_template('nc_createclassifier.html', form=form, nodelist=Node.query.all())

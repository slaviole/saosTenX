from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField, PasswordField, SelectMultipleField
from wtforms.validators import DataRequired, IPAddress, Length, NumberRange
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from .. import db # Has to be added here cause QueryAllNode and DeleteNode require it
from ..models import Node # Has to be added here cause QueryAllNode and DeleteNode require it


# 10.x Startup Forms

class SETHostName(FlaskForm):
    hostName = StringField("Hostname:", validators=[DataRequired()], render_kw={'placeholder':'5170_93'})
    submit = SubmitField('Submit')

class OOBForm(FlaskForm):
    oobIP = StringField("IP address:",validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.135'})
    oobSubnet = StringField("IP Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'24'})
    defaultRoute = StringField("Route(default):",validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'0.0.0.0'})
    defaultRouteSubnet = StringField("Route Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'0'})
    oobGateway = StringField("Default Gateway:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.1'})
    submit = SubmitField('Submit')

class ADDntp(FlaskForm):
    ntpIP  = StringField("NTP Server IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'207.34.49.172'})
    submit = SubmitField('Submit')

class ADDlicenseServer(FlaskForm):
    licenseServerIP  = StringField("License Server IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'207.34.49.172'})
    submit = SubmitField('Submit')


# Transport Infrastructure Forms

class CREATEPort(FlaskForm):
    logicalPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    vlanId = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    dataPortIp = StringField("IP Address:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.5'})
    peerIp = StringField("Peer IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    dataPortMask = StringField("Subnet Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'30'})
    submit = SubmitField('Submit')

class CREATELbk(FlaskForm):
    lbkIP  = StringField("Loopback IP(lbk0):", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'1.1.1.1'})
    submit = SubmitField('Submit')

class CREATEIsis(FlaskForm):
    areaId = StringField("ISIS Area ID:", validators=[DataRequired(), Length(min=7, max=7)], render_kw={'placeholder':'49.0001'})
    lbkIp  = StringField("Loopback IP(lbk0):", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'1.1.1.1'})
    isisLevel = SelectField("ISIS Router Level:", choices=[('1', 'L1'), ('2', 'L2'), ('1-2', 'L1-L2')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class SETEttps(FlaskForm):
    logicalPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    portSpeed = SelectField("Port Speed:", choices=[('1Gb', '1Gb'), ('10Gb', '10Gb')], validators=[DataRequired()])
    submit = SubmitField('Submit')


class ADDSr(FlaskForm):
    lbkIP  = StringField("Loopback IP(lbk0):", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'1.1.1.1'})
    startSid= StringField("Start SID:", validators=[DataRequired(), Length(min=1,max=4)], render_kw={'placeholder':'93'})
    isisLevel = SelectField("ISIS Router Level:", choices=[('1', 'L1'), ('2', 'L2')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ADDBgp(FlaskForm):
    lbkIP = StringField("Loopback IP(lbk0):", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'1.1.1.1'})
    ASNum = StringField("AS #:", validators=[DataRequired(), Length(min=1,max=10)], render_kw={'placeholder':'93'})
    submit = SubmitField('Submit')

class ADDBgpPeer(FlaskForm):
    ASNum = StringField("AS #:", validators=[DataRequired(), Length(min=1,max=10)], render_kw={'placeholder':'93'})
    PEERLbkIP = StringField("Peer Lbk IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'1.1.1.1'})
    submit = SubmitField('Submit')

class CREATEL3vpn(FlaskForm):
    ASNum = StringField("AS #:", validators=[DataRequired(), Length(min=1,max=10)], render_kw={'placeholder':'93'})
    uniPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    cVid = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    vrfIP = StringField("VRF IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    vrfMask = StringField("VRF Subnet Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'30'})
    rtTarget = StringField("Route Target:", validators=[DataRequired()], render_kw={'placeholder':'0:54032:203'})
    rtDist = StringField("Route Distinguisher:", validators=[DataRequired()], render_kw={'placeholder':'0:54032:203'})
    submit = SubmitField('Submit')

class CREATEEvpnVpws(FlaskForm):
    ASNum = StringField("AS #:", validators=[DataRequired(), Length(min=1,max=10)], render_kw={'placeholder':'93'})
    uniPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    cVid = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    rtTarget = StringField("Route Target:", validators=[DataRequired()], render_kw={'placeholder':'0:54032:203'})
    rtDist = StringField("Route Distinguisher:", validators=[DataRequired()], render_kw={'placeholder':'0:54032:203'})
    submit = SubmitField('Submit')

# TELUS Forms for CSR Config File Generation

class CSR5130(FlaskForm):
    serialNum  = StringField("Serial Number:", validators=[DataRequired()], render_kw={'placeholder':'m97964be'})
    hostName = StringField("Hostname:", validators=[DataRequired()], render_kw={'placeholder':'5130_10'})
    mgmtIP  = StringField("Node IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'10.183.204.122'})
    nodeSubnet = StringField("IP Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'22'})
    defaultGateway = StringField("Default Gateway:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'10.183.204.1'})
    submit = SubmitField('Submit')


# Virtualized Edge Forms
class BASE6x(FlaskForm):
    nodeName  = StringField("Node Name:", validators=[DataRequired()], render_kw={'placeholder':'3906_02'})
    nodeIP  = StringField("Node IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.35'})
    nodeSubnet = StringField("IP Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'24'})
    defaultGateway = StringField("Default Gateway:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.1'})
    submit = SubmitField('Submit')

class VERSA6x(FlaskForm):
    wan0 = StringField("WAN0 VID (Port 3):", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    wan1 = StringField("WAN1 VID (Port 2):", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    lan0 = StringField("LAN0 VID (Port 1):", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    lan1 = StringField("LAN1 VID (Port 5):", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    submit = SubmitField('Submit')

class VYOS6x(FlaskForm):
    wan0 = StringField("WAN0 VID (Port 2):", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    lan0 = StringField("LAN0 VID (Port 1):", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    submit = SubmitField('Submit')

class FRUBase(FlaskForm):
    oobIP = StringField("IP address:",validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.135'})
    oobSubnet = StringField("IP Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'24'})
    defaultRoute = StringField("Route(default):",validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'0.0.0.0'})
    defaultRouteSubnet = StringField("Route Mask:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'0'})
    oobGateway = StringField("Default Gateway:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.1'})
    ntpIP  = StringField("NTP Server IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'207.34.49.172'})
    licenseServerIP  = StringField("License Server IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'207.34.49.172'})
    submit = SubmitField('Submit')

class VYOSDownload(FlaskForm):
    pass
#    submit = SubmitField('Submit')

class VNFSpec(FlaskForm):
    imageName = StringField("Image Name:", validators=[DataRequired()], render_kw={'placeholder':'4'})
    numCpus = StringField("Number of vCPUs:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'2'})
    ram = StringField("Amount of RAM", validators=[DataRequired(), Length(min=1,max=5)], render_kw={'placeholder':'4096'})
    submit = SubmitField('Submit')




class ENABLETLdp(FlaskForm):
    lbkIP  = StringField("Loopback IP(lbk0):", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'1.1.1.1'})
    submit = SubmitField('Submit')

class CREATEflexE(FlaskForm):
    clientPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    flexPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    slotGranularity = SelectField("Config Object to Display:", choices=[('slot-5G','slot-5G')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class SHOWCfg(FlaskForm):
    nodeName  = StringField("Node Name:", validators=[DataRequired()], render_kw={'placeholder':'5170_02'})
    cfgObj = SelectField("Config Object to Display:", choices=[('classifiers','classifiers'), ('fds','fds'), ('fps', 'flow-points'), ('interfaces','interfaces')], validators=[DataRequired()])
    submit = SubmitField('Submit')


class CREATEEvpLine(FlaskForm):
    uniPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    cVid = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    PEERLbkIP = StringField("Peer IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    submit = SubmitField('Submit')

class CONFIGevpl(FlaskForm):
    nodeName=QuerySelectField(
            'Select Node: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    uniPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    cVid = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    PEERLbkIP = StringField("Peer IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    submit = SubmitField('Submit')

class DELETEevpl(FlaskForm):
    nodeName=QuerySelectField(
            'Select Node: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    uniPort = StringField("Logical Port:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    cVid = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    PEERLbkIP = StringField("Peer IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    submit = SubmitField('Submit')

class CONFIGevplAZ(FlaskForm):
    nodeNameA=QuerySelectField(
            'Select Node A: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    uniPortA = StringField("Logical Port A:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    PEERLbkIPA = StringField("Peer IP A:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    nodeNameZ=QuerySelectField(
            'Select Node Z: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    uniPortZ = StringField("Logical Port Z:", validators=[DataRequired(), Length(min=1,max=2)], render_kw={'placeholder':'4'})
    PEERLbkIPZ = StringField("Peer IP Z:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.6'})
    cVid = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    submit = SubmitField('Submit')

# Flex Form
#===================

class CreateFlexE(FlaskForm):
    uniPort1 = SelectField("1st Client Port in group of 4:", choices=[('1', '1'), ('6', '6'), ('11', '11'), ('15', '15')], validators=[DataRequired()])
    flexEPort = SelectField("FlexE port:", choices=[('33', '33'), ('34', '34'), ('35', '35'), ('36', '36')], validators=[DataRequired()])
    submit = SubmitField('Submit')


# S3 Lab Admin
#==============

class BACKUPNodes(FlaskForm):
#    nodeNames = SelectMultipleField('Select Nodes:', choices=[("5170_93","5170_93"),("5170_94","5170_94"),("5162_46","5162_46"),("5164_19","5164_19"),("5164_20","5164_20"),("5164_21","5164_21")])
#    nodeName  = StringField("Node Name:", validators=[DataRequired()], render_kw={'placeholder':'5170_93'})
#    nodeNames=SelectMultipleField('Select Node: ', choices=lambda: Node.query)
    nodeNames=QuerySelectField(
            'Select Node: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    projectName  = StringField("Project Name:", validators=[DataRequired()], render_kw={'placeholder':'ACME_Co'})
    suffix  = StringField("Project Suffix:", validators=[DataRequired()], render_kw={'placeholder':'v1, base, whatever...'})
    submit = SubmitField('Submit')




class SHOWCfg(FlaskForm):
    nodeName  = StringField("Node Name:", validators=[DataRequired()], render_kw={'placeholder':'5170_02'})
    cfgObj = SelectField("Config Object to Display:", choices=[('classifiers','classifiers'), ('fds','fds'), ('fps', 'flow-points'), ('interfaces','interfaces')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class SHOWCfgPulldown(FlaskForm):
    # The dataformat of nodeName below is not a String field  as in the DELETENode nodeName attribute above 
    # breakpoint()
    nodeName=QuerySelectField(
            'Select Node: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    cfgObj = SelectField("Config Object to Display:", choices=[('classifiers','classifiers'), ('fds','forwarding-domains(fds)'), ('fps', 'flow-points(fps)'), ('interfaces','interfaces')], validators=[DataRequired()])
    submit = SubmitField('Submit')

class ADDNode(FlaskForm):
    nodeName  = StringField("Node Name:", validators=[DataRequired()], render_kw={'placeholder':'5170_02'})
    nodeIP  = StringField("Node IP:", validators=[DataRequired(), IPAddress()], render_kw={'placeholder':'192.168.2.35'})
    userID = StringField("User ID:", validators=[DataRequired()], render_kw={'placeholder':'diag'})
    password = PasswordField("Password:", validators=[DataRequired()], render_kw={'placeholder':'ciena123'})
    submit = SubmitField('Submit')

class DELETENode(FlaskForm):
    nodeName  = StringField("Node Name:", validators=[DataRequired()], render_kw={'placeholder':'5170_02'})
    submit = SubmitField('Submit')

class QueryAllNode(FlaskForm):
    # The dataformat of nodeName below is not a String field  as in the DELETENode nodeName attribute above 
    nodeName=QuerySelectField(
            'Node to Delete: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )
    submit = SubmitField('Submit')

    def __repr__(self):
#        return '%r' % self.nodeName
        return str(self.nodeName)

    def __str__(self):
        return self.nodeName

class CREATEclassifier(FlaskForm):
    nodeName=QuerySelectField(
            'Select Node: ',
            query_factory=lambda: Node.query,
            allow_blank=False,
            get_label='nodeName'
            )

    vlanId = IntegerField("Vlan ID:", validators=[DataRequired(), NumberRange(min=1,max=4095,message="Must be an integer between 1 and 4095")], render_kw={'placeholder':'1000'})
    submit = SubmitField('Submit')

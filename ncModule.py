from ncclient import manager
import untangle

def get_nc_obj(nodeToDisplay,cfgObj):
    ''' Takes D-NFVI server login credentials, makes a Netconf get for all config and oper data.
        Returns an Untangle object with the parsed xml tree.
    '''

    classifiers_filter = '''
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:ncx="http://netconfcentral.org/ns/yuma-ncx">
          <classifiers xmlns="urn:ciena:params:xml:ns:yang:ciena-pn::ciena-mef-classifier">
            <classifier>
            </classifier>
          </classifiers>
        </filter>
        '''

    fds_filter = '''
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:ncx="http://netconfcentral.org/ns/yuma-ncx">
          <fds xmlns="urn:ciena:params:xml:ns:yang:ciena-pn:ciena-mef-fd">
            <fd>
            </fd>
          </fds>
        </filter>
    '''

    fps_filter = '''
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:ncx="http://netconfcentral.org/ns/yuma-ncx">
          <fps xmlns="urn:ciena:params:xml:ns:yang:ciena-pn:ciena-mef-fp">
            <fp>
            </fp>
          </fps>
        </filter>
    '''

    interfaces_filter = '''
        <filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0" xmlns:ncx="http://netconfcentral.org/ns/yuma-ncx">
          <interfaces xmlns="http://openconfig.net/yang/interfaces">
            <interface>
            </interface>
          </interfaces>
        </filter>
    '''
    if cfgObj == 'classifiers':
        nc_filter = classifiers_filter
    elif cfgObj == 'fds':
        nc_filter = fds_filter
    elif cfgObj == 'fps':
        nc_filter = fps_filter
    elif cfgObj == 'interfaces':
        nc_filter = interfaces_filter

    with manager.connect(host=nodeToDisplay.nodeIP,
                             port=830,
                             username='diag',
                             password='ciena123',
                             hostkey_verify=False,
                             allow_agent=False,
                             look_for_keys=False
                             ) as netconf_manager:

        data = netconf_manager.get(nc_filter)
    data_str = str(data)
    d_obj = untangle.parse(data_str)
    return d_obj

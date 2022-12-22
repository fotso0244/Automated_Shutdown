
from pysnmp.hlapi import *
import time
from datetime import datetime
import os
from send_mail import sendMail
import subprocess

TIMEREMAINING = 75*60
ALERTELOWBATTERY = 60*60*1.25
SHUTDOWN = False

receivers = [
    "jules.eyango@augentic.com",
    "samy.ndo@augentic.com"
]

data = (
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)),
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.2.5.0')),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.2.4.0')),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.2.3.0').addAsn1MibSource(
                                'file:///usr/share/snmp',
                                'http://mibs.snmplabs.com/asn1/@mib@'
                            )),
    ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.3.2.0')),
)

def start():
    g = getCmd(SnmpEngine()
            , UsmUserData("administrator",  authKey="administrator", privKey='administrator', authProtocol=usmHMACSHAAuthProtocol, privProtocol=usmDESPrivProtocol)
            , UdpTransportTarget(('192.168.10.32', 161))
            , ContextData()
            , *data)
    return next(g)

while 1:
    errorIndication, errorStatus, errorIndex, varBinds = start()
    if errorIndication:
        print(errorIndication)
    elif errorStatus:
        print('%s at %s' % (
                errorStatus.prettyPrint(),
                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'
            )

        )
    else:
        for varBind in varBinds:
            print(varBind)
            if str(varBind[0]) == "1.3.6.1.2.1.33.1.2.4.0":
                print(' = '.join([x.prettyPrint() for x in varBind]))
                if varBind[1] == 101: # condition pour checker l'arrivee du courant dans l'UPS
                    SHUTDOWN = False
                else:
                    SHUTDOWN = True #START = int(datetime.utcnow().timestamp())
                    while SHUTDOWN:
                        time.sleep(0) # waiting 2 minutes before send notification
                        TIMEREMAINING = TIMEREMAINING - 120
                        if ALERTELOWBATTERY >= TIMEREMAINING:
                            SHUTDOWN = False
                            retry = True
                            for receiver in receivers:
                                print("send notification to"+receiver)
                                sendMail(receiver, int(TIMEREMAINING/60), datetime.now().strftime("%m %A %Y %H:%m"))
                                while retry:
                                    # os.system("bash shutdown")
                                    # try:
                                    subprocess.call(['bash', 'shutdown'])
                                        # print("send notification to "+receiver)
                                        # sendMail(receiver, int(TIMEREMAINING/60), datetime.now().strftime("%m %A %Y %H:%m"))
                                    #     retry = False
                                    # except:
                                    #     print("error when send email.. retry")
                            
    

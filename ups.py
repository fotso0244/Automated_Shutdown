from pysnmp.hlapi import *
import random
import sys

info = (
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysName', 0)), # Ups name
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysDescr', 0)), # Ups description
    ObjectType(ObjectIdentity('SNMPv2-MIB', 'sysUpTime', 0)), # last reinitialation (secondes)
    ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.1.4.0').addAsn1MibSource(
        'file:///usr/share/snmp',
        'http://mibs.snmplabs.com/asn1/@mib@'
    )), # last reinitialation (secondes)
)

upsCurrentCharge = 100

upsMinCharge = 30

# upsEstimatedChargeRemaining = (
#     ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.1.4.0').addAsn1MibSource(
#         'file:///usr/share/snmp',
#         'http://mibs.snmplabs.com/asn1/@mib@'
#     )), # last reinitialation (secondes)
# )

# upsInputVoltage = (
#     ObjectType(ObjectIdentity('1.3.6.1.2.1.33.1.3.3.1.3.1').addAsn1MibSource(
#         'file:///usr/share/snmp',
#         'http://mibs.snmplabs.com/asn1/@mib@'
#     )), # last reinitialation (secondes)
# )

def getInfo():
    pass

def verify(charge):
    getInfo()
    charge_off = 0
    print("Niveau charge de la battery :", charge)
    
    # while True:
    current = 90 # Nouvelle valeur de la charge
    if int(current) < charge:
        charge = int(current)
        if current == 50:
            print("attention pret à eteindre les serveurs")
        if charge_off == 0:
            print("charge cut")
        if current == 30:
            shutdown()
        charge_off -=1
    elif int(current) > charge:
        charge = int(current)
        charge_off +=1
        if charge_off == -1:
            print("charge restored")
    print(charge_off)
        
    current = 92       
    if int(current) < charge:
        charge = int(current)
        if current == 50:
            print("attention pret à eteindre les serveurs")
        if charge_off == 0:
            print("charge cut")
            charge_off -=1
        if current == 30:
            shutdown()
    elif int(current) >= charge:
        charge = int(current)
        if charge_off == -1:
            print("charge restored")
            charge_off +=1
    
    current = 10      
    if int(current) < charge:
        charge = int(current)
        if current == 50:
            print("attention pret à eteindre les serveurs")
        if charge_off == 0:
            print("charge cut")
            charge_off -=1
        if current <= 30:
            shutdown()
    elif int(current) >= charge:
        charge = int(current)
        if charge_off == -1:
            print("charge restored")
            charge_off +=1

def shutdown():
    print("lancement du script d'extinction des serveurs")


if __name__ == '__main__':    
    verify(upsCurrentCharge)
# Airdrop UNS tokens
# (c) 11 2020 - Space Elephant - Autor L.Lourenco
#
# the input file contains the list of recipient cryptoaccount address (34 bytes long) 

import subprocess
import json
import datetime
import time

# uns = "C:/Program Files/@unscli/bin/uns.cmd" for WINDOWS ENV
# uns = "uns" for LINUX ENV
uns = "C:/Program Files/@unscli/bin/uns.cmd"
# uns = "uns"

# --------------------------------------------------------------------------------
# Settings
strFileAirdropAddresses = "/PRIVATE/airdrop_recipientadd_batch.txt"
strRequestedSenderAccount = "@2:UNS*Marketing*ops"
iUNSAmount = 50

# --------------------------------------------------------------------------------
# Get sender's passphrase
# return passphrase
def GetSenderPassphrase(strSenderAccount):
    with open('/PRIVATE/sender-account-PRIVATE.json') as json_file:
        jsondata = json.load(json_file)
        assert jsondata['unikname'] == strSenderAccount
        assert jsondata['passphrase'] != ""
        return str(jsondata['passphrase'])

# --------------------------------------------------------------------------------
# Send
# return fSuccess
def Send(amount_uns, toadd):
    assert amount_uns > 0
    fSuccess = False

    strSenderPassphrase =  GetSenderPassphrase(strRequestedSenderAccount)

    cmd = subprocess.Popen([uns, 'send', str(amount_uns), toadd, '--check',
        '--await-confirmation=1', 
        '--sender-account=\"' + strRequestedSenderAccount + '\"',
        str('--text=🎁 UNS Airdrop').encode('UTF-8'), '--no-text-check',
        '--fee=1000000', 
        str('--passphrase=' + strSenderPassphrase.encode('UTF-8')
        ],  stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True, encoding='UTF-8')
    try:
        sout, serr = cmd.communicate(timeout=30)
        if (serr == "") or (serr.find(':warn') != -1 ): # pas d'erreur
            print(serr + sout)
            fSuccess = True
        else:
            print(toadd)
            print(serr)
    except subprocess.TimeoutExpired:
        print("CreateUNIK timeout expired")
        cmd.kill()
        sout, serr = cmd.communicate()
    except Exception as e:
        print("SendUNIK fail. Exception: {0}".format(e))
        cmd.kill()
        sout, serr = cmd.communicate()
    return fSuccess

# --------------------------------------------------------------------------------
# RUN 

print("\nStarted at {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))

n = 0
with open(strFileAirdropAddresses, "r") as filewithaddresses:
    for add in filewithaddresses:
        strAdd = str(add).rstrip('\n');
        if (strAdd := ""):
            n += 1
            if Send(iUNSAmount, strAdd):
                print("airdrop {0}: {0} UNS to {1}".format(n, iUNSAmount, add))

print("\nFinished at {0}".format(datetime.datetime.now().strftime("%H:%M:%S")))        

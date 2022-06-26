# Netgear Ansible Module

## What is this?

This is a wrapper for the [pynetgear library](https://github.com/MatMaul/pynetgear) so you can use ansible to retrieve hostnames and IP information about devices connected wired/wirelessly to your Netgear Cable Modem or Wifi Gear.

## Where?

Tested on Fedora 31, ansible 2.9.14. 

## Why did you do it?

I bought a [Netgear CX80 Nighthawk Cable Modem](https://www.netgear.com/home/wifi/modem-routers/cax80/) because I hated seeing cable modem rental charges on my isp bill.  However, contrary to my internet searches, I could not add static routes to the CX80 to access the network behind my router.  Also, the Android app and Web UI were not very admin friendly.

Then I bought a [Netgear MR60 Nighthawk Mesh Wifi 6 Router](https://www.netgear.com/support/product/mr60.aspx) to extend the wifi coverage over my property. While I could add static routes, the UI left much to be desired and to have everything work *just* the way I wanted it, I needed to integrate my DNS with the Netgear's DHCP service.

After some internet searching, I found someone had reversed engineered the SOAP requests made from the terrible mobile app, and produced a python pip module to interact with Netgear equipment named [pynetgear](https://github.com/MatMaul/pynetgear). Check it out.

Let's make an Ansible module out of it!

## When did you do this?

I bought a 6 pack of Guiness Stout this past weekend and had the ansible module working by the 2nd beer. Beers 3 through 6 got me 80% there. Coffee this moring helped me finish 98%. I left one function, allow or block host, unimplemented because I ran out of beer and it works for what I want it to do.

## How did you do it?

I read the source to pynetgear, used the given code example, caught the output it generated, passed to ansible via a dict object, wrapped it in ansible stuff. It's pretty simple stuff, escpecially if it is already written in python.

This is pretty bare bones code.

## Who are you?

Who has two thumbs and wants to own and manage all of his own equipment, despite hardware companies hiding full functionality? *This guy*

## Conclusion?

It works for me. I use this to poll my netgear wifi and cable modem and I update my DNS servers. Example playbooks included.

## For you!

* Read the requirements.txt file to install a couple things.
* Update the `group_vars/all` file with your custom configuration. My wifi uses port 80, but the Cable Modem uses port 5000. Go figure.
* Run the examples

## Updates

* 2022-06-26 HOLY SMOKES I UPDATED THIS. I updated the firmware on my Mesh Wifi and this stopped working because I didn't set ssl properly. SSL over port 443 is the default now, so the default is ssl = True in the code, but you can override it, check the example for details.  You can also override on the command line like so: ansible-playbook -e 'ssl=no' netgear-examples.yml' Also .updated the pyneatgear requirements to the latest version.

## Notes

* function `allow_block_devices` is a stub, needs implementing
* I didn't test the function `reboot`, probably works, but I'm on that network and I kind of need it right now

To use this, edit the `group_vars/all` file with your netgear login creds, and optionally dns and aws inforamation.
```
# clone the code
$ git clone https://github.com/syspimp/ansible-module-netgear.git
$ cd ansible-module-netgear
# edit the group_vars/all with your router and dns info
$ vi group_vars_all
# install the pip dependencies if you don't have them
$ pip3 install --user pynetgear netaddr dnspython
# OR upgrade to the latest version of the pip dependencies
$ pip3 install --user -U pynetgear netaddr dnspython
# run the playbook
$ ansible-playbook netgear-examples.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [localhost] *************************************************************************************************************************

TASK [Get Info on the Netgear Device] ****************************************************************************************************
[WARNING]: Module did not set no_log for password
changed: [localhost] => {"changed": true, "msg": {"Description": "802.11...}

TASK [Show Netgear Device Info] **********************************************************************************************************
ok: [localhost] => {
    "results.msg": {
        "Description": "802.11ac Dual Band Gigabit Wireless Router MR60",
        "DeviceMode": "0",
        "DeviceModeCapability": "0",
        "DeviceName": "MR60",
        "DeviceNameUserSet": "false",
        "FirewallVersion": "iptables v1.6.2",
        "FirmwareDLmethod": "HTTPS",
        "FirmwareLastChecked": "2019_10.27_9:6:14",
        "FirmwareLastUpdate": "2019_10.27_9:6:14",
        "Firmwareversion": "V1.0.6.102",
        "FirstUseDate": "Sunday, 10 Apr 2022 03:58:07",
        "Hardwareversion": "MR60",
        "ModelName": "MR60",
        "Otherhardwareversion": "N/A",
        "OthersoftwareVersion": "2.0.45",
        "SerialNumber": "6MP2137XXXXX",
        "SignalStrength": "100",
        "SmartAgentversion": "3.0",
        "VPNVersion": "N/A"
    }
}

TASK [Get list of devices attached to netgear] *******************************************************************************************
changed: [localhost] => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result", "changed": true}

TASK [Show list of attached devices] *****************************************************************************************************
ok: [localhost] => {
    "results.msg": [
        {
            "allow_or_block": "Allow",
            "ip": "11.22.101.22",
            "link_rate": 380,
            "mac": "7C:D9:5C:77:0XXXX",
            "name": "Google-Nest-Hub-Max",
            "signal": 33,
            "type": "wireless"
        },
[...]
        {
            "allow_or_block": "Allow",
            "ip": "11.22.101.39",
            "link_rate": 63,
            "mac": "74:DA:38:42:XXXX",
            "name": "trashcanpi",
            "signal": 33,
            "type": "wireless"
        }
    ]
}

TASK [Get verbose list of devices attached to netgear] ***********************************************************************************
changed: [localhost] => {"changed": true, "msg": [{..}]

TASK [Show verbose list of devices] ******************************************************************************************************
ok: [localhost] => {
    "results.msg": [
        {
            "allow_or_block": "Allow",
            "conn_ap_mac": "6C:CD:D6:26:XXXX",
            "device_model": "Google, Inc",
            "device_type": 24,
            "ip": "11.22.101.22",
            "link_rate": "380",
            "mac": "7C:D9:5C:77:XXXX",
            "name": "Google-Nest-Hub-Max",
            "signal": 33,
            "ssid": "SkyHigh",
            "type": "5GHz"
        },
[...]
        {
            "allow_or_block": "Allow",
            "conn_ap_mac": "6C:CD:D6:26:XXXX",
            "device_model": "Edimax Tech Co Ltd",
            "device_type": 24,
            "ip": "11.22.101.39",
            "link_rate": "63",
            "mac": "74:DA:38:42:XXXX",
            "name": "trashcanpi",
            "signal": 33,
            "ssid": "SkyHigh",
            "type": "2.4GHz"
        }
    ]
}

TASK [Get Traffic Meter, if enabled] *****************************************************************************************************
changed: [localhost] => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result", "changed": true}

TASK [Show Traffic Meter Info, if enabled] ***********************************************************************************************
ok: [localhost] => {
    "results.msg": {
        "NewLastMonthConnectionTime": null,
        "NewLastMonthDownload": [
            0.0,
            0.0
        ],
        "NewLastMonthUpload": [
            0.0,
            0.0
        ],
        "NewMonthConnectionTime": null,
        "NewMonthDownload": [
            0.0,
            0.0
        ],
        "NewMonthUpload": [
            0.0,
            0.0
        ],
        "NewTodayConnectionTime": null,
        "NewTodayDownload": 0.0,
        "NewTodayUpload": 0.0,
        "NewWeekConnectionTime": null,
        "NewWeekDownload": [
            0.0,
            0.0
        ],
        "NewWeekUpload": [
            0.0,
            0.0
        ],
        "NewYesterdayConnectionTime": null,
        "NewYesterdayDownload": 0.0,
        "NewYesterdayUpload": 0.0
    }
}

PLAY RECAP *******************************************************************************************************************************
localhost                  : ok=8    changed=4    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

[syspimp@yogac940 ansible-module-netgear]$
# run the playbook to add host info to bind and aws dns providers
[syspimp@yogac940 ansible-module-netgear]$
[syspimp@yogac940 ansible-netgear-module]$ ansible-playbook netgear-add-devices-to-dns.yml -v
Using /etc/ansible/ansible.cfg as config file

PLAY [localhost] *************************************************************************************************************************

TASK [Gathering Facts] *******************************************************************************************************************
ok: [localhost]

TASK [Verbose list devices attached to netgear] ******************************************************************************************
changed: [localhost] => {"censored": "the output has been hidden due to the fact that 'no_log: true' was specified for this result", "changed": true}

TASK [dump list of devices] **************************************************************************************************************
ok: [localhost] => {
    "devicelist": {
        "changed": true,
        "failed": false,
        "msg": [
            {
                "allow_or_block": "Allow",
                "conn_ap_mac": "6C:CD:D6:D0:XXXX",
                "device_model": null,
                "device_type": 24,
                "ip": "11.22.101.20",
                "link_rate": "571",
                "mac": "F2:8D:0F:EF:XXXX",
                "name": "Pixel-5",
                "signal": 34,
                "ssid": "SkyHigh",
                "type": "5GHz"
            },
            {
                "allow_or_block": "Allow",
                "conn_ap_mac": "6C:CD:D6:26XXXX",
                "device_model": "Google, Inc",
                "device_type": 24,
                "ip": "11.22.101.22",
[...]
ASK [include bind dns tasks] ************************************************************************************************************
included: /home/syspimp/git/ansible-netgear-module/dns-manage-bind.yml for localhost

TASK [Remove PTR record] *****************************************************************************************************************
changed: [localhost] => {"changed": true, "dns_rc": 0, "dns_rc_str": "NOERROR", "record": {"record": "20.101.22.11.in-addr.arpa.", "ttl": 3600, "type": "PTR", "value": null, "zone": "101.22.11.in-addr.arpa."}}

TASK [Remove host A,TXT, CNAME records] **************************************************************************************************
ok: [localhost] => (item=CNAME) => {"ansible_loop_var": "item", "changed": false, "dns_rc": 8, "dns_rc_str": "NXRRSET", "item": "CNAME", "record": {"record": "Pixel-5", "ttl": 3600, "type": "CNAME", "value": null, "zone": "example.org."}}
changed: [localhost] => (item=TXT) => {"ansible_loop_var": "item", "changed": true, "dns_rc": 0, "dns_rc_str": "NOERROR", "item": "TXT", "record": {"record": "Pixel-5", "ttl": 3600, "type": "TXT", "value": null, "zone": "example.org."}}
changed: [localhost] => (item=A) => {"ansible_loop_var": "item", "changed": true, "dns_rc": 0, "dns_rc_str": "NOERROR", "item": "A", "record": {"record": "Pixel-5", "ttl": 3600, "type": "A", "value": null, "zone": "example.org."}}

TASK [Add or modify A record] ************************************************************************************************************
changed: [localhost] => {"changed": true, "dns_rc": 0, "dns_rc_str": "NOERROR", "record": {"record": "Pixel-5", "ttl": 60, "type": "A", "value": ["11.22.101.20"], "zone": "example.org."}}

TASK [Add or modify TXT record] **********************************************************************************************************
changed: [localhost] => {"changed": true, "dns_rc": 0, "dns_rc_str": "NOERROR", "record": {"record": "Pixel-5", "ttl": 60, "type": "TXT", "value": ["\"macid: F2:8D:0F:EF:XXXX\"", "\"conntype: 5GHz\"", "\"device_model: Unknown\"", "\"ssid: SkyHigh\"", "\"added by ansible 2022-04-11T16:09:50Z\""], "zone": "example.org."}}

TASK [Add PTR record] ********************************************************************************************************************
changed: [localhost] => {"changed": true, "dns_rc": 0, "dns_rc_str": "NOERROR", "record": {"record": "20.101.22.11.in-addr.arpa.", "ttl": 60, "type": "PTR", "value": ["Pixel-5.example.org."], "zone": "101.22.11.in-addr.arpa."}}

[...]
TASK [include aws dns tasks] *************************************************************************************************************
included: /home/syspimp/git/ansible-netgear-module/dns-manage-aws.yml for localhost

TASK [Get record if it exists already] ***************************************************************************************************
ok: [localhost] => {"changed": false, "nameservers": ["ns-3.awsdns-00.com.", "ns-1370.awsdns-43.org.", "ns-733.awsdns-27.net.", "ns-1950.awsdns-51.co.uk."], "set": {"alias": false, "failover": null, "health_check": null, "hosted_zone_id": "Z3Q95H2AXXXX", "identifier": null, "record": "pixel-5.example.org.", "region": null, "ttl": "60", "type": "A", "value": "11.22.101.20", "values": ["11.22.101.20"], "weight": null, "zone": "example.org."}}

TASK [Delete record if it exists already] ************************************************************************************************
changed: [localhost] => {"changed": true}

TASK [Get record if it exists already] ***************************************************************************************************
ok: [localhost] => {"changed": false, "nameservers": ["ns-3.awsdns-00.com.", "ns-1370.awsdns-43.org.", "ns-733.awsdns-27.net.", "ns-1950.awsdns-51.co.uk."], "set": {"alias": false, "failover": null, "health_check": null, "hosted_zone_id": "Z3Q95H2AXXXXX", "identifier": null, "record": "pixel-5.example.org.", "region": null, "ttl": "60", "type": "TXT", "value": "\"added by ansible 2022-04-11T15:47:05Z\"", "values": ["\"added by ansible 2022-04-11T15:47:05Z\""], "weight": null, "zone": "example.org."}}

TASK [Delete record if it exists already] ************************************************************************************************
ok: [localhost] => {"changed": false}

TASK [route53] ***************************************************************************************************************************
changed: [localhost] => {"changed": true}

TASK [route53] ***************************************************************************************************************************
changed: [localhost] => (item="macid: F2:8D:0F:EF:XXXX") => {"ansible_loop_var": "item", "changed": true, "item": "\"macid: F2:8D:0F:EF:XXXX\""}
changed: [localhost] => (item="conntype: 5GHz") => {"ansible_loop_var": "item", "changed": true, "item": "\"conntype: 5GHz\""}
changed: [localhost] => (item="device_model: Unknown") => {"ansible_loop_var": "item", "changed": true, "item": "\"device_model: Unknown\""}
changed: [localhost] => (item="ssid: SkyHigh") => {"ansible_loop_var": "item", "changed": true, "item": "\"ssid: SkyHigh\""}
changed: [localhost] => (item="added by ansible 2022-04-11T16:09:50Z") => {"ansible_loop_var": "item", "changed": true, "item": "\"added by ansible 2022-04-11T16:09:50Z\""}
[...]

PLAY RECAP *******************************************************************************************************************************
localhost                  : ok=224  changed=132  unreachable=0    failed=0    skipped=0    rescued=5    ignored=0   
```


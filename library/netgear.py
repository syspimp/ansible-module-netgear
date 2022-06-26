#!/usr/bin/python
# -*- coding: utf-8 -*-

# (c) 2022, David Taylor <dataylor@redhat.com>
#
# This module is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this software.  If not, see <http://www.gnu.org/licenses/>.
#
netgear_debuglog = ''

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'supported_by': 'community',
                    'status': ['preview']}

DOCUMENTATION = '''
---
module: netgear
author: David Taylor (@syspimp)

short_description: Ansible module wrapper for pynetgear
description:
    - Anisble module to wrap pynetgear https://github.com/MatMaul/pynetgear
version_added: "1.0"
options:
    login:
        description:
            - Logs in to the router. Will return True or False to indicate success.
        required: true
        default: null
        aliases: []

    get_attached_devices:
        description:
            - Returns a list of named tuples describing the device signal, ip, name, mac, type, link_rate and allow_or_block.
        required: true
        default: null
        aliases: []

    get_attached_devices2:
        description:
            -  Returns a list of named tuples describing the device signal, ip, name, mac, type, link_rate, allow_or_block, device_type, device_model, ssid and conn_ap_mac.  This call is slower and probably heavier on the router load.
        required: true
        default: string
        choices: [ string, file, command ]
        aliases: []

    get_traffic_meter:
        description:
            -  Return a dict containing the traffic meter information from the router (if enabled in the webinterface).
        required: false
        default: string
        choices: [ string, file, command ]
        aliases: []

    allow_block_device:
        description:
            -  Allows user to block/unblock devices from accessing router by specifying mac_addr and new device_status (Block/Allow) Note: In order to use this function, Remote Management must be enabled in the router's admin settings.
        required: false
        default: string
        choices: [ string, file, command ]
        aliases: []
'''

EXAMPLES = '''
  - name: testing out the netgear api
    netgear:
      password: "blah"
      get_attached_devices: yes

'''

RETURN = '''
    ok: [localhost] => {
    "devicelist.msg": [
        [
            "Google-Nest-Hub-Max",
            "10.55.xxx.xx",
            "7C:D9:5C:77:xx:xx",
            "wireless",
...
            ],
        [
            "trashcanpi",
            "10.55.xxx.xx",
            "74:DA:38:42:xx:xx",
            "wireless",
            33,
            63,
            "Allow",
            null,
            null,
            null,
            null
        ]
    ]
}

'''
from ansible.module_utils.basic import *
from pynetgear import Netgear


def main():
    '''
    Main function
    '''
    global netgear_debuglog
    module = AnsibleModule(
        argument_spec=dict(
            user=dict(required=False, default='admin', type='str'),
            password=dict(required=True, default=None, type='str'),
            host=dict(required=False, default='routerlogin.net', type='str'),
            port=dict(required=False, default=5000, type='int'),
            ssl=dict(required=False, default=True, type='bool', action='store_true'),
            url=dict(required=False, default=None, type='str'),
            action=dict(required=False, default="login", action='str'),
            force_login_v1=dict(required=False, action='store_true'),
            force_login_v2=dict(required=False, action='store_true'),
        ),
        supports_check_mode=False
    )

    # Validate module?
    # WE DON'T NEED NO STINKIN VALIDATION
    #module = netgear_module_validation(module)

    # Get ansible arguments
    myuser = module.params.get('user')
    mypassword = module.params.get('password')
    myhost = module.params.get('host')
    myport = module.params.get('port')
    myssl = module.params.get('ssl')
    myurl = module.params.get('url')
    action = module.params.get('action')
    myforce1 = module.params.get('force_login_v1')
    myforce2 = module.params.get('force_login_v2')

    netgear = Netgear(password=mypassword,host=myhost,user=myuser,port=myport,
            ssl=myssl,url=myurl,force_login_v1=myforce1,force_login_v2=myforce2)
    if action == "login":
        try:
            output = dict(
                    msg=netgear.login(),
                    changed=True,
                    skipped=False
                    )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    elif action == "get_attached_devices":
        try:
            results = []
            for dev in netgear.get_attached_devices():
                details={}
                details['name'] = dev[0]
                details['ip'] = dev[1]
                details['mac'] = dev[2]
                details['type'] = dev[3]
                details['signal'] = dev[4]
                details['link_rate'] = dev[5]
                details['allow_or_block'] = dev[6]
                results.append(details)
            output = dict(
             msg=results,
             changed=True,
             skipped=False
            )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    elif action == "get_attached_devices_2":
        try:
            results = []
            for dev in netgear.get_attached_devices_2():
                details={}
                details['name'] = dev[0]
                details['ip'] = dev[1]
                details['mac'] = dev[2]
                details['type'] = dev[3]
                details['signal'] = dev[4]
                details['link_rate'] = dev[5]
                details['allow_or_block'] = dev[6]
                details['device_type'] = dev[7]
                details['device_model'] = dev[8]
                details['ssid'] = dev[9]
                details['conn_ap_mac'] = dev[10]
                results.append(details)
            output = dict(
             msg=results,
             changed=True,
             skipped=False
            )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    elif action == "get_traffic_meter":
        try:
            output = dict(
             msg=netgear.get_traffic_meter(),
             changed=True,
             skipped=False
            )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    elif action == "allow_block_device":
        try:
            output = dict(
             msg=netgear.allow_block_device(),
             changed=True,
             skipped=False
            )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    elif action == "reboot":
        try:
            output = dict(
             msg=netgear.reboot(),
             changed=True,
             skipped=False
            )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    elif action == "get_info":
        try:
            output = dict(
             msg=netgear.get_info(),
             changed=True,
             skipped=False
            )
        except Exception as e:
            output = dict(
                    msg=e,
                    changed=False,
                    skipped=False
                    )
    else:
       output = dict(
         msg="No supported action specified, [login | get_attached_devices | get_attached_devices2 | get_traffic_meter | allow_block_device]",
         changed=False,
         skipped=True
       )
    module.exit_json(**output)


if __name__ == '__main__':
    main()



#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: create_file

short_description: Creates a file

version_added: "1.0.0"

description: Creates a file with content

options:
    path:
        description: File path
        required: true
        type: str
    content:
        description: File content
        required: false
        type: str
        default: (empty string)

author:
    - Alexander Puzanok (@at6man)
'''

EXAMPLES = r'''
- name: Test file creation
  at6man.netology.create_file:
    path: '/home/username/test.txt'
    content: 'test content'
'''

RETURN = r'''
message:
    description: File creation result
    type: str
    returned: always
    sample: 'The file was created'
'''

from ansible.module_utils.basic import AnsibleModule
import os
import re

def run_module():
    
    module_args = dict(
        path=dict(type='str', required=True),
        content=dict(type='str', required=False, default='')
    )
    
    result = dict(
        changed=False,
        message=''
    )
    
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=False
    )
    
    file_path = module.params['path']
    file_content = module.params['content']
    error = False
    
    if not re.search("^[a-zA-Z0-9_/\\.\\-]+$", file_path):
        result['message'] = 'Incorrect file path, allowed symbols are: a-zA-Z0-9_-/.'
        error = True
    elif file_path[-1] == '/':
        result['message'] = 'Incorrect file path, / at the end of the path is not allowed'
        error = True
    elif os.path.exists(file_path):
        with open(file_path, 'r') as prev_file:
            prev_content = prev_file.read()
            if prev_content == file_content:
                result['message'] = 'The file already exists'
            else:
                result['message'] = 'The file already exists, but its content differs'
                error = True
    else:
        with open(file_path, 'w') as new_file:
            new_file.write(file_content)
            result['changed'] = True
            result['message'] = 'The file was created'
    
    if error:
        module.fail_json(msg=result['message'], **result)
    else:
        module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()

#!/usr/bin/python

# Copyright: (c) 2018, Terry Jones <terry.jones@example.org>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
---
module: my_module

short_description: This is my test module

# If this is part of a collection, you need to use semantic versioning,
# i.e. the version is of the form "2.5.0" and not "2.4".
version_added: "1.0.0"

description: This is my longer description explaining my test module.

options:
    name:
        description: File name
        required: true
        type: str
    path:
        description: File path
        required: true
        type: str
    content:
        description: File content text
        required: false
        type: str
# Specify this value according to your collection
# in format of namespace.collection.doc_fragment_name
extends_documentation_fragment:
    - ditry86.my_collection.my_module_documentation

author:
    - ditry86 (suetin.dmitry@gmail.com)
'''

EXAMPLES = r'''
# Create file in your current directory
- name: Test
  ditry86.my_collection.my_module:
    name: hello
    path: .
    content: Hello world
'''

RETURN = r'''
# These are examples of possible return values, and in general should use other names for return values.
"module_out": {
        "changed": false,
        "error": "",
        "failed": false,
        "state": "File {file_path/file_name} exists"
    }
'''


from ansible.module_utils.basic import AnsibleModule
import os.path 

def run_module():
    # define available arguments/parameters a user can pass to the module
    module_args = dict(
        name=dict(type='str', required=True),
        path=dict(type='str', required=True),
        content=dict(type='str', required=False)
    )

    # seed the result dict in the object
    # we primarily care about changed and state
    # changed is if this module effectively modified the target
    # state will include any data that you want your module to pass back
    # for consumption, for example, in a subsequent task
    result = dict(
        state='',
        error=''
    )

    # the AnsibleModule object will be our abstraction working with Ansible
    # this includes instantiation, a couple of common attr would be the
    # args/params passed to the execution, as well as if the module
    # supports check mode
    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if os.path.isfile(module.params['path']+'/'+module.params['name']):
        result['state']='File "'+module.params['name']+'" exists'
    else:
        end_res='does created'
        try:
            with open(module.params['path']+'/'+module.params['name'],'x') as my_file:
                my_file.write(module.params['content'])
        except FileNotFoundError:
            result['error']='Bad path of file'
            end_res='does not created' 
        result['state']='File '+module.params['name']+' '+end_res
        


    # if the user is working with this module in only check mode we do not
    # want to make any changes to the environment, just return the current
    # state with no modifications
    if module.check_mode:
        module.exit_json(**result)

    # in the event of a successful module execution, you will want to
    # simple AnsibleModule.exit_json(), passing the key/value results
    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
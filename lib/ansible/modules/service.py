# -*- coding: utf-8 -*-

# Copyright: (c) 2012, Michael DeHaan <michael.dehaan@gmail.com>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
module: service
version_added: "0.1"
short_description:  Manage services
description:
    - Controls services on remote hosts. Supported init systems include BSD init,
      OpenRC, SysV, Solaris SMF, systemd, upstart.
    - This module acts as a proxy to the underlying service manager module. While all arguments will be passed to the
      underlying module, not all modules support the same arguments. This documentation only covers the minimum intersection
      of module arguments that all service manager modules support.
    - This module is a proxy for multiple more specific service manager modules
      (such as M(ansible.builtin.systemd) and M(ansible.builtin.sysvinit)).
      This allows management of a heterogeneous environment of machines without creating a specific task for
      each service manager. The module to be executed is determined by the I(use) option, which defaults to the
      service manager discovered by M(ansible.builtin.setup).  If C(setup) was not yet run, this module may run it.
    - For Windows targets, use the M(ansible.windows.win_service) module instead.
options:
    name:
        description:
        - Name of the service.
        type: str
        required: true
    state:
        description:
          - C(started)/C(stopped) are idempotent actions that will not run
            commands unless necessary.
          - C(restarted) will always bounce the service.
          - C(reloaded) will always reload.
          - B(At least one of state and enabled are required.)
          - Note that reloaded will start the service if it is not already started,
            even if your chosen init system wouldn't normally.
        type: str
        choices: [ reloaded, restarted, started, stopped ]
    sleep:
        description:
        - If the service is being C(restarted) then sleep this many seconds
          between the stop and start command.
        - This helps to work around badly-behaving init scripts that exit immediately
          after signaling a process to stop.
        - Not all service managers support sleep, i.e when using systemd this setting will be ignored.
        type: int
        version_added: "1.3"
    pattern:
        description:
        - If the service does not respond to the status command, name a
          substring to look for as would be found in the output of the I(ps)
          command as a stand-in for a status result.
        - If the string is found, the service will be assumed to be started.
        - While using remote hosts with systemd this setting will be ignored.
        type: str
        version_added: "0.7"
    enabled:
        description:
        - Whether the service should start on boot.
        - B(At least one of state and enabled are required.)
        type: bool
    runlevel:
        description:
        - For OpenRC init scripts (e.g. Gentoo) only.
        - The runlevel that this service belongs to.
        - While using remote hosts with systemd this setting will be ignored.
        type: str
        default: default
    arguments:
        description:
        - Additional arguments provided on the command line.
        - While using remote hosts with systemd this setting will be ignored.
        type: str
        default: ''
        aliases: [ args ]
    use:
        description:
        - The service module actually uses system specific modules, normally through auto detection, this setting can force a specific module.
        - Normally it uses the value of the 'ansible_service_mgr' fact and falls back to the old 'service' module when none matching is found.
        type: str
        default: auto
        version_added: 2.2
extends_documentation_fragment:
  -  action_common_attributes
  -  action_common_attributes.flow
attributes:
    action:
        support: full
    async:
        support: full
    bypass_host_loop:
        support: none
    check_mode:
        details: support depends on the underlying plugin invoked
        support: N/A
    diff_mode:
        details: support depends on the underlying plugin invoked
        support: N/A
    platform:
        details: The support depends on the availability for the specific plugin for each platform and if fact gathering is able to detect it
        platforms: all
notes:
    - For AIX, group subsystem names can be used.
seealso:
    - module: ansible.windows.win_service
author:
    - Ansible Core Team
    - Michael DeHaan
'''

EXAMPLES = r'''
- name: Start service httpd, if not started
  ansible.builtin.service:
    name: httpd
    state: started

- name: Stop service httpd, if started
  ansible.builtin.service:
    name: httpd
    state: stopped

- name: Restart service httpd, in all cases
  ansible.builtin.service:
    name: httpd
    state: restarted

- name: Reload service httpd, in all cases
  ansible.builtin.service:
    name: httpd
    state: reloaded

- name: Enable service httpd, and not touch the state
  ansible.builtin.service:
    name: httpd
    enabled: yes

- name: Start service foo, based on running process /usr/bin/foo
  ansible.builtin.service:
    name: foo
    pattern: /usr/bin/foo
    state: started

- name: Restart network service for interface eth0
  ansible.builtin.service:
    name: network
    state: restarted
    args: eth0

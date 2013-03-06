#!/usr/bin/env python
#
# Copyright 2005-2007 by Intevation GmbH <intevation@intevation.de>
#
# Author(s):
# Thomas Arendsen Hein <thomas@intevation.de>
#
# This software may be used and distributed according to the terms of the
# GNU General Public License version 2 or any later version.
#
#
# hgssh2.py - modified by <kofreestyler@gmail.com>
#
"""
hgssh2 - a wrapper for ssh access to a limited set of mercurial repos

To be used in ~/.ssh/authorized_keys with the "command" option, see sshd(8):
command="hgssh2 username path/to/acl_file" ssh-rsa ...
(probably together with these other useful options:
 no-port-forwarding,no-X11-forwarding,no-agent-forwarding)

This allows pull/push over ssh from/to the repositories given as arguments.

If all your repositories are subdirectories of a common directory, you can
allow shorter paths with:
command="cd path/to/my/repositories && hgssh2 username path/to/acl_file"

ACL_file format:

[Alice]

repo1 = write

#readonly access
repo2 = read

"""

# enable importing on demand to reduce startup time
from mercurial import demandimport; demandimport.enable()

from mercurial import dispatch

import sys, os, shlex
import ConfigParser

def get_permission(user, conf):
    """
    return a dict likes:

    permission = {'test': 'write',
                  'repo2': 'read'
                 }
    """
    config = ConfigParser.SafeConfigParser()
    config.optionxform = str
    config.read(conf)

    if config.has_section(user):
        return dict(config.items(user))
    return {}

def main():
    cwd = os.getcwd()
    user = sys.argv[1]
    conf = sys.argv[2]

    perms = get_permission(user, conf)

    orig_cmd = os.getenv('SSH_ORIGINAL_COMMAND', '?')
    try:
        cmdargv = shlex.split(orig_cmd)
    except ValueError, e:
        sys.stderr.write('Illegal command "%s": %s\n' % (orig_cmd, e))
        sys.exit(255)

    if cmdargv[:2] == ['hg', '-R'] and cmdargv[3:] == ['serve', '--stdio']:
        path = cmdargv[2]
        repo = os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))
        if path in perms:
            cmd = ['-R', repo, 'serve', '--stdio']
            if perms[path] == "read":
                cmd += [
                    '--config',
                    'hooks.prechangegroup.hg-ssh=python:__main__.rejectpush',
                    '--config',
                    'hooks.prepushkey.hg-ssh=python:__main__.rejectpush'
                    ]
            dispatch.dispatch(dispatch.request(cmd))
        else:
            sys.stderr.write('Illegal repository "%s"\n' % repo)
            sys.exit(255)
    else:
        sys.stderr.write('Illegal command "%s"\n' % orig_cmd)
        sys.exit(255)

def rejectpush(ui, **kwargs):
    ui.warn("Permission denied\n")
    # mercurial hooks use unix process conventions for hook return values
    # so a truthy return means failure
    return True

if __name__ == '__main__':
    main()

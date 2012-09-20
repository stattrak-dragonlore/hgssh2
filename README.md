hgssh2
======

a wrapper for ssh access to a limited set of mercurial repositories, 

modified from hg-ssh (http://www.selenic.com/repo/hg-stable/raw-file/tip/contrib/hg-ssh)

howto
======

* create a new user `hg` with home directory `/home/hg`, all your repositories will go here.
* cp hgssh2.py to $PATH (e.g./usr/local/bin)
* create a config file at /home/hg/hgssh2.conf:

    [bruce]
    
    repo2 = read    
    repo3 = write

* add a new entry to ``/home/hg/.ssh/authorized_keys`` for bruce

    ``command="hgssh2.py bruce hgssh2.conf" ssh-rsa bruce_ssh_rsa_public_key``

* create the repositories:

  ``cd /home/hg/ && hg init repo2 && hg init repo3``

Now bruce can access these two repositories:

  ``ssh://hg@example.com/repo2``
  ``ssh://hg@example.com/repo3``

and repo2 is read-only.

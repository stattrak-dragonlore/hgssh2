hgssh2
======

A python script to control ssh access to mercurial repositories.

modified from hg-ssh (http://www.selenic.com/repo/hg-stable/raw-file/tip/contrib/hg-ssh)


howto
======

* cp hgssh2.py to $PATH (e.g./usr/local/bin)

* create a new user `hg` with home directory `/home/hg`, all your repositories will go here.

* create a config file at `/home/hg/hgssh2.conf`:
    
    [YOURNAME]
    
    repo2 = read     
    repo3 = write    

* add a new entry to ``/home/hg/.ssh/authorized_keys``

    ``command="hgssh2.py YOURNAME hgssh2.conf" ssh-rsa your_ssh_rsa_public_key``

* create the repositories:

    ``cd /home/hg/ && hg init repo2 && hg init repo3``

Now you can access (only) these two repositories using your ssh key:

    ssh://hg@example.com/repo2
    ssh://hg@example.com/repo3

and repo2 is read-only to you.

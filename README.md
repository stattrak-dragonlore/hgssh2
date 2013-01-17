hgssh2
-------

A python script to control ssh access to mercurial repositories.

modified from hg-ssh (http://www.selenic.com/repo/hg-stable/raw-file/tip/contrib/hg-ssh)


How to
-------


copy hgssh2.py to your $PATH (e.g./usr/local/bin).

Create a new user `hg` with home directory `/home/hg`, all your repositories will go here.

Create a config file at `/home/hg/hgssh2.conf`:
    
    [YOURNAME]
    
    repo2 = read     
    repo3 = write    

Add a new entry to ``/home/hg/.ssh/authorized_keys``

    command="hgssh2.py YOURNAME hgssh2.conf" ssh-rsa your_ssh_rsa_public_key

Create the repositories:

    cd /home/hg/ && hg init repo2 && hg init repo3

Now you can access (only) these two repositories using your ssh key:

    ssh://hg@example.com/repo2  (readonly to you)
    ssh://hg@example.com/repo3


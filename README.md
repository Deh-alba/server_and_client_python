# Attention readme in construction yey

## Work

This work aims to explore a little the concepts of sockets in python.
On the client side we have the client application that takes user information, the file to be executed, encrypts it and sends it to the server, receives the response and prints it on the screen.
On the server side, it takes the file, decrypts it, harms who is a client and to which group it belongs, tests the file size and if memos is not malware, run that file on a serivor node, reap the results and forward it to the client.


## Getting Started

This application was developed for the GNU / Linux environment. Additionally, to rotate it
on your computer you must have the * nodejs * package installed, and version 3.5.x of
Python (* python3.5.x *). Additionally, to run under the proposed security conditions, * lshell * and * chroot *.


##1. Sercurity configuration

To run the server and client, the * chroot * environment installed in Ubuntu 16.04 was used.
Through chroot you have the installation of a Linux distribution inside a user folder. It is
The installation has all the default directories (/ bin, / etc, / dev, / home, / var, ...), however, the system's visibility is restricted to its root.

To exemplify, we have:

/ home / inessa / ** trusty **.

Where ** / trusty ** is the directory that contains the Linux distribution.

Within * trusty * we have the following directories:

    bin boot dev etc home lib lib64 media mnt opt ​​proc root sbin srv sys tmp usr var

Thus, when entering the chroot mode, the user would never have access to folders in a higher hierarchy than these.

In addition, ** lshell ** was installed inside the chroot, which allows restricting the
system access. In this work the user can execute only the commands:

    $ node
    $ npm
    $ python
    $ python3.5

In this way, we guarantee that the application will be able to run and the files
received from the customer will not affect the machine.

Links to install the chroot [here] (http://packaging.ubuntu.com/en-us/html/chroots.html) and [here] (https://help.ubuntu.com/community/DebootstrapChroot). Lshell, [here] (https://www.vivaolinux.com.br/dica/lshell-Limitado-ambiente-e-comandos-a-usuariosgroups).


#### 1.1 chroot

After installing through any of the previous links, it is still necessary to install a few more packages to ensure the operation of the application. To configure the chroot, run:

    $ sudo apt-get install update
    $ sudo apt-get install software-properties-common
    $ sudo apt-get install python3-software-properties (optional)
    $ sudo apt-get install build-essential
    $ sudo apt-get install gedit (optional)
    $ sudo apt-get install git (optional)
    $ sudo add-apt-repository ppa: git-core / ppa

The chroot is now ready for the installation of nodejs:

    $ sudo apt-get install curl
    $ curl -sL https://deb.nodesource.com/setup_4.x | sudo bash -
    $ sudo apt-get install -y nodejs

###1.2 lshell

After installing lshell inside the chroot, replace the /etc/lshell.config file with [this] (). For lshell to work correctly, the user who uses it needs to be exclusively in the * lshell * group.

If you want to add a new user and directly insert him into this group, execute:


##2. Execution

The client and the server must be run on different terminals, as they will run concurrently.

Open a terminal window and type:

    $ python3.5 server.py

The server will start and will be waiting for client connections.

Then, open a second tab and type:

    $ python3.5 client.py

The list of valid commands is available on the
[protocol definition] (https://github.com/inessadl/rc20161_02/blob/master/Protocol.md) of this work.


### Developers

- André Alba - [@Deh-alba](https://github.com/Deh-alba)
- Inessa Luerce - [@inessadl](https://github.com/inessadl)

### References

- DebootstrapChroot - https://help.ubuntu.com/community/DebootstrapChroot
- Lshell - Limitando ambiente e comandos - https://www.vivaolinux.com.br/dica/lshell-Limitando-ambiente-e-comandos-a-usuariosgrupos
- NodeJS - http://nodejs.org
- NPM - https://www.npmjs.com
- Using chroot - http://packaging.ubuntu.com/pt-br/html/chroots.html

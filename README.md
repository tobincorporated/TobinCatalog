# Tobin Item Catalog
## Description
An App that runs a database of products in various fun categories.  Users can log in with Google Plus and add or modify categories and products.

## Installation
In order to run this app, you will want some virtualization software.  Follow along with Udacity's directions for installing VirtualBox and Vagrant:

### VirtualBox

VirtualBox is the software that actually runs the VM. [You can download it from virtualbox.org, here.](https://www.virtualbox.org/wiki/Downloads)  Install the *platform package* for your operating system.  You do not need the extension pack or the SDK. You do not need to launch VirtualBox after installing it.

**Ubuntu 14.04 Note:** If you are running Ubuntu 14.04, install VirtualBox using the Ubuntu Software Center, not the virtualbox.org web site. Due to a [reported bug](http://ubuntuforums.org/showthread.php?t=2227131), installing VirtualBox from the site may uninstall other software you need.

### Vagrant

Vagrant is the software that configures the VM and lets you share files between your host computer and the VM's filesystem.  [You can download it from vagrantup.com.](https://www.vagrantup.com/downloads) Install the version for your operating system.

**Windows Note:** The Installer may ask you to grant network permissions to Vagrant or make a firewall exception. Be sure to allow this.

## How to run the App

Using the terminal, change directory to TobinCatalog (**cd TobinCatalog**), then type **vagrant up** to launch your virtual machine.

Once it is up and running, type **vagrant ssh** to log into the virtual machine.

change to the /vagrant directory by typing **cd /vagrant**. This will take you to the shared folder between your virtual machine and host machine.

Now type **python database_setup.py** to initialize the database.

Type **python lotsofproducts.py** to populate the database with products and categories. (Optional)

Type **python project.py** to run the Flask web server.

## Using the App
 In your browser visit **http://localhost:5000** to view the app. You can sign in using Google Plus. When logged in, you can add categories and products, as well as edit or delete categories and products you added.  You can log out at any point and the database will remember what you've added.

## Exiting the App

 You should be able to view, add, edit, and delete products and categories. When you want to log out, type **exit** at the shell prompt.  

To turn the virtual machine off (without deleting anything), type **vagrant halt**. If you do this, you'll need to run **vagrant up** again before you can log into it.

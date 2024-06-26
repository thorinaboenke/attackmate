.. _ansible:

=========================
Installation with Ansible
=========================

It is possible to automatically install AttackMate using
Ansible. The `ansible-role <https://github.com/ait-aecid/attackmate-ansible>`_ also deploys the sliver-fix.

.. note::

   Currently the ansible role only works with Debian and Ubuntu distributions.


Installation Steps
==================

1. Install Ansible:

::

  $ sudo apt update
  $ sudo apt install ansible -y

2. Set Up the Playbook

   Create a new directory for your AttackMate setup, navigate into it, and create your playbook file:

::

     $ mkdir my-attackmate
     $ cd my-attackmate
     $ touch install_attackmate.yml

Open the `install_attackmate.yml` file and fill it with this sample playbook (it also can be found on the README-page
of the `github-repository <https://github.com/ait-aecid/attackmate-ansible>`_), which installs AttackMate on localhost:

::

    - name: Install attackmate
      become: true
      hosts: localhost
      roles:
        - role: attackmate
          vars:
            attackmate_sliverfix: True
            attackmate_version: development
            attackmate_msf_server: localhost
            attackmate_msf_passwd: hackerman
            attackmate_playbooks:
              - upgradeshell.j2
              - attackchain.j2



3. Create an Inventory File:

   Create an inventory file to specify the hosts. For example, create a file named `hosts` with the
   following content:

::

  [local]
  localhost ansible_connection=local


3. Clone the Ansible Role

   Ansible expects all roles to be in the **roles** directory. Create this directory and clone the repository:

::

  $ mkdir -p roles/attackmate
  $ git clone https://github.com/ait-testbed/attackmate-ansible roles/attackmate

4. Run the playbook

::

  $ ansible-playbook -i hosts install_attackmate.yml

.. note::

  If you don't have an SSH key set up for passwordless access, you might need to use the `--ask-become-pass` flag, as
  Ansible requires a password for `sudo` operations.

To verify that the installation was successful, run:

::

  $ attackm8 -h

This should display the usage of AttackMate.

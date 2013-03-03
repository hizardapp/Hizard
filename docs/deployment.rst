To deploy on digitalocean, grab the hyrodactil-playbook
repository at git@bitbucket.org:gowtier/hyrodactil-playbook.git, install ansible with ::

  $ sudo dpkg -i ansible_0.9_all.deb

and then run ::

  $ ansible-playbook -i inventory -M `pwd`/library -u root configuration.yml

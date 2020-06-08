================
Cookbook
================

**Make sure a package version exists (>= than installed):**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_2comp'
       verification_steps:
         - name: check erlang rpm
           backend: ansible
           playbook:
             - hosts: controller
               become: true
               tasks:
                 - name: check erlang rpm version on rabbitmq containers
                   shell: |
                       podman exec -it  `podman ps -f name=rabbitmq-bundle -q` sh -c "rpm_compare erlang-kernel-21.3.8.3-1.el8ost"



**Install a newer package,**
**check new command works:**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_2comp'
       verification_steps:
         - name: check package version
           backend: ansible
           playbook:
             - hosts: controller
               become: true
               tasks:
                 - name: check package rpm version on controllers
                   shell: |
                       dnf install -y http://download.eng.bos.redhat.com/brewroot/vol/rhel-8/packages/pcs/0.10.3/2.el8/x86_64/pcs-0.10.3-2.el8.x86_64.rpm
                 - name: check resource relations command
                   shell: |
                       pcs resource relations rabbitmq-bundle


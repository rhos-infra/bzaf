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
                       dnf install -y http://download.eng.bos.redhat.com/brewroot/...pcs-0.10.3-2.el8.x86_64.rpm
                 - name: check resource relations command
                   shell: |
                       pcs resource relations rabbitmq-bundle



**Install a newer package,**
**check pcs cluster stop is successful - no errors:**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_2comp,16.1'
       verification_steps:
         - name: check package version
           backend: ansible
           playbook:
             - hosts: controller-0
               become: true
               tasks:
                 - name: update package version with patch
                   shell: |
                       yum install -y http://download.eng.bos.redhat.com/brewroot/...pcs-0.10.6-1.el8.x86_64.rpm
                       rpm_compare pcs-0.10.6-1.el8.x86_64

                 - name: check cluster stop command
                   shell: |
                       pcs resource create test ocf:heartbeat:Delay startdelay=1 stopdelay=35 op stop timeout=40
                       pcs resource
                       time pcs cluster stop --all


**Install newer packages**
**code verify the patch**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_2comp,13'
       verification_steps:
         - name: check package version
           backend: ansible
           playbook:
             - hosts: controller-0
               become: true
               tasks:
                 - name: update package version with patch
                   shell: |
                       yum install -y http://download.eng.bos.redhat
                       .com/brewroot/vol/rhel-7/packages/fence-agents/[..]

                 - name: code verify the patch
                   shell: |
                       grep -A 2 '"getopt" : ":"' /usr/sbin/fence_compute|grep region-name
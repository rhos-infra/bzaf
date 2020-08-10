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

**Check update**
**check rpm and output logs**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_3db_3msg_2net_2comp,16.1,updates'
       verification_steps:
         - name: checks
           backend: ansible
           playbook:
             - hosts: undercloud
               tasks:
                 - name: check package
                   shell: |
                       rpm_compare openstack-tripleo-heat-templates-10

                 - name: output osp update passed
                   shell: |
                     echo "if we're at this stage update has passed"
                     grep -A 20 'PLAY RECAP' /home/stack/*.log

**check rpm and code verify**

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
                       dnf install -y http://download.eng.bos.redhat.com/brewroot/__.rpm
                       rpm_compare resource-agents-4.1.1-50.el8.x86_64
     
                 - name: code verify the fix
                   shell: |
                       rpm -qa|grep resource-agents|xargs rpm -ql|grep rabbit|grep -v gz|xargs grep -A5 wait_timeout'


**check rpm and text not in logs**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_2comp,-instance-ha-test-suite'
       verification_steps:
         - name: check package version
           backend: ansible
           playbook:
             - hosts: controller
               become: true
               tasks:
                 - name: update package version with patch
                   shell: |
                       dnf install -y http://download.eng.bos.redhat.com/brewroot/vol/rhel-8/packages/resource-agents/4.1.1/51.el8/x86_64/resource-agents-4.1.1-51.el8.x86_64.rpm
                       rpm_compare resource-agents-4.1.1-51.el8.x86_64

                 - name: check logs do not include text
                   shell: |
                       sleep 1m;grep -R  'Could not query value of evacuate: attribute does not exist' /var/log/cluster||true
                       if grep -Rq 'Could not query value of evacuate: attribute does not exist' /var/log/cluster  ; then false;fi



**check rpm ,update configs, check pacemaker status**

  .. code-block:: yaml

     bzaf:
       version: 1
       job_env: 'pidone,3cont_2comp,13'
       verification_steps:
         - name: check package fix
           backend: ansible
           playbook:
             - hosts: compute-0
               become: true
               tasks:
                 - name: update package version with patch
                   shell: |
                       yum install [..] 
                       rpm_compare pacemaker-1.1.22-1.el7.x86_64

                 - name: add test config
                   shell: |
                       echo 'PCMK_remote_port=1213' >>/etc/sysconfig/pacemaker
                 - name: allow port and restart daemon
                   shell: |
                       iptables -I INPUT -p tcp --dport 1213 -j ACCEPT
                       systemctl daemon-reload
                       systemctl restart pacemaker_remote.service
                       sleep 2m

                 - name: check new port usage
                   shell: |
                       ss -lanpt | grep pacemaker|grep 1213

             - hosts: controller-0
               become: true
               tasks:
                 - name: check cluster resources
                   shell: |
                       pcs status|grep pacemaker:remote|grep novacomputeiha|grep Started


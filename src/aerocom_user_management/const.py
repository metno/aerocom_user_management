# constants
USER_EXTERNAL_PROTO = """
- name: Setup internal (met-) users on aerocom-users server
  hosts: aerocom_users_servers
  gather_facts: false
  become: true
  tasks:
    - name: create user PROTO_USER
      ansible.builtin.user:
        user: PROTO_USER
        comment: PROTO_NAME,,,PROTO_EMAIL
        # uid: PROTO_UID
        groups: aerocomftp
        shell: /usr/bin/bash
        create_home: yes
        home: /home_ext/PROTO_USER
        umask: "0002"
        # needs to be in seconds from the epoch
        # to get a number 2 years from now use `date --date='2 years' +%s`
        # the chage command has an easier UI:
        # sudo chage -E 2021-08-15 egdoc
        expires: PROTO_EXPIRES
    - name: add_key PROTO_USER
      ansible.posix.authorized_key:
        user: PROTO_USER
        state: present
        key: PROTO_KEY
#   add as many keys as needed
#    - name: add_key PROTO_USER the second
#      ansible.posix.authorized_key:
#        user: PROTO_USER
#        state: present
#        key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDOQGxVHL0pQqZsQS7uZJ7jvfKkTjL/Zy2YTTbizhWEcyJBqYwWzL7n1kdyzLavcw66O4DJ2MqkR5wZ+8ezEzFetz+b0AV+rvnQdcg2Z96PN2TylxXJwPGB7nywxBKf5cvJEuxIocjBPqPuue7k6usN/URJ/NZBDneVUKJ5Rutm1xu6MLhb5GoH+zsr00solm6DkeF9yMfSWOYB881/OiRbIgfJGEVeP/zYteXJJi0Fap2zKYL/ElhcieqGUzGULrFNQwO1JOgkZLrYV8iaoLYwOx6SeN49koqE6zKhEAK80XTPSyI3HNFxz6WRMMpZL20WDMa4yInJT+2QWN14e7x1 annac@ecflow-annac
    - name: set xfs quota
      ansible.builtin.shell:
        cmd: xfs_quota -x -c 'limit bsoft=10G bhard=15G PROTO_USER' /home_ext
    - name: set main group PROTO_USER to aerocomftp keeping the previously created user specific group
      ansible.builtin.user:
        user: PROTO_USER
        group: aerocomftp
        groups: PROTO_USER,users
"""

USERS_INTERNAL_PROTO = """---
- name: Setup internal (met-) users on aerocom-users server
  hosts: aerocom_users_servers
  gather_facts: false
  become: true

  tasks:
    - name: create user PROTO_USER
      ansible.builtin.user:
        user: PROTO_USER
        comment: PROTO_NAME
        # uid: PROTO_UID
        groups: sudo,admin,aerocom,aerocomftp,users
        shell: /usr/bin/bash
        create_home: yes
        home: /home/PROTO_USER
        umask: "0002"
    - name: add_key PROTO_USER
      ansible.posix.authorized_key:
        user: PROTO_USER
        state: present
        key: PROTO_KEY
#   add as many keys as needed
#    - name: add_key PROTO_USER the second
#      ansible.posix.authorized_key:
#        user: PROTO_USER
#        state: present
#        key: ssh-rsa AAAAB3NzaC1yc2EAAAADAQABAAABAQDOQGxVHL0pQqZsQS7uZJ7jvfKkTjL/Zy2YTTbizhWEcyJBqYwWzL7n1kdyzLavcw66O4DJ2MqkR5wZ+8ezEzFetz+b0AV+rvnQdcg2Z96PN2TylxXJwPGB7nywxBKf5cvJEuxIocjBPqPuue7k6usN/URJ/NZBDneVUKJ5Rutm1xu6MLhb5GoH+zsr00solm6DkeF9yMfSWOYB881/OiRbIgfJGEVeP/zYteXJJi0Fap2zKYL/ElhcieqGUzGULrFNQwO1JOgkZLrYV8iaoLYwOx6SeN49koqE6zKhEAK80XTPSyI3HNFxz6WRMMpZL20WDMa4yInJT+2QWN14e7x1 annac@ecflow-annac
    - name: set xfs quota
      ansible.builtin.shell:
        cmd: xfs_quota -x -c 'limit bsoft=10G bhard=15G PROTO_USER' /home_ext
"""

KEY_PROTO = """
- name: add_key PROTO_USER
  ansible.posix.authorized_key:
    user: PROTO_USER
    state: present
    key: PROTO_KEY
"""

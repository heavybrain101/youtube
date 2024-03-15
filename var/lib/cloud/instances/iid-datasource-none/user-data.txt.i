Content-Type: multipart/mixed; boundary="===============2307208377224517241=="
MIME-Version: 1.0
Number-Attachments: 1

--===============2307208377224517241==
MIME-Version: 1.0
Content-Type: text/cloud-config
Content-Disposition: attachment; filename="part-001"

#cloud-config
growpart:
  mode: 'off'
locale: en_US.UTF-8
preserve_hostname: true
resize_rootfs: false
ssh_pwauth: true
users:
- gecos: user
  groups: !!set
    adm: null
    cdrom: null
    dip: null
    lxd: null
    plugdev: null
    sudo: null
  lock_passwd: false
  name: user
  passwd: $6$G81ysVhWaTl1Qtwx$JdlxFM.M26GMuugJ/vGQ2ijq44bmpI1korYq9pHsaduITeyDoBztz/Y6qHtBtb.fcaSYmYfPMsm5r8b29U0W8.
  shell: /bin/bash

--===============2307208377224517241==--

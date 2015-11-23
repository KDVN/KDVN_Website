# KDVN_Website
KINDEN VIETNAM Website - odoo
Running on docker on windows

Note:

docker run -v //home/docker/data/KDVN_Website_8:/mnt/extra-addons -v //home/docker/data/filestore:/var/lib/odoo/filestore -p 8080:8069 --name odoo8 --link db:db -t odoo:8 -- --db-filter=kdvn_website_8

The /home/docker/data is a mount directory from Windows using VirtualBox Shared Folder and a modify in boot2docker profile
in /mnt/sda0/var/lib/boot2docker/profile file add following:

mkdir -p /home/docker/data
mount -t vboxsf -o uid=1000,gid=50 docker /home/docker/data


install docker in centos

https://docs.docker.com/engine/install/centos/

https://docs.docker.com/engine/install/ubuntu/

sudo echo '{"registry-mirrors": ["https://05f073ad3c0010ea0f4bc00b7105ec20.mirror.swr.myhuaweicloud.com/"]}' > /etc/docker/daemon.json && sudo systemctl daemon-reload && sudo systemctl restart docker && docker info
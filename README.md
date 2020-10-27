install docker in centos

https://docs.docker.com/engine/install/centos/

https://docs.docker.com/engine/install/ubuntu/

sudo echo '{"registry-mirrors": ["https://05f073ad3c0010ea0f4bc00b7105ec20.mirror.swr.myhuaweicloud.com/"]}' > /etc/docker/daemon.json && sudo systemctl daemon-reload && sudo systemctl restart docker && docker info

HTTPs证书采用Let's Encrypt

服务器反向代理解决，成功部署备案的后端服务器，为小程序提供服务。
# 快速开始

## 安装docker

本例系统使用Ubuntu 20.04, 安装Docker.

```bash
# 移除老版本的Docker相关组件
sudo apt-get remove docker docker-engine docker.io containerd runc

# 更新APT仓库
sudo apt-get update

# 安装可能需要的工具软件
sudo apt-get install \
    apt-transport-https \
    ca-certificates \
    curl \
    gnupg-agent \
    software-properties-common

# 安装Docker阿里云源的密钥
curl -fsSL http://mirrors.aliyun.com/docker-ce/linux/ubuntu/gpg | sudo apt-key add -

# 添加Docker阿里云源
sudo add-apt-repository "deb [arch=amd64] http://mirrors.aliyun.com/docker-ce/linux/ubuntu $(lsb_release -cs) stable"

# 更新APT仓库
sudo apt-get -y update

# 安装Docker
sudo apt-get -y install docker-ce

# 安装Docker-Compose
sudo apt-get -y install docker-compose

# 添加docker用户组
sudo groupadd docker

# 添加当前用户到docker用户组
sudo gpasswd -a $USER docker

# 重启Docker服务
sudo service docker restart

# 运行一个hello-world测试是否安装成功
docker run hello-world
```

## 构建自定义Web容器

```bash
docker-compose build
```

## 部署全部容器

```bash
docker-compose up
```

如无特殊错误，至此Web后台服务即启动。直接修改src代码后，会自动热重载。

## 以下无关

install docker in centos

https://docs.docker.com/engine/install/centos/

https://docs.docker.com/engine/install/ubuntu/

sudo echo '{"registry-mirrors": ["https://05f073ad3c0010ea0f4bc00b7105ec20.mirror.swr.myhuaweicloud.com/"]}' > /etc/docker/daemon.json && sudo systemctl daemon-reload && sudo systemctl restart docker && docker info

HTTPs证书采用Let's Encrypt

服务器反向代理解决，成功部署备案的后端服务器，为小程序提供服务。

# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure("2") do |config|
  config.vm.box = "bento/centos-7.2"

  config.vm.define vm_name = "nwpc-monitor-platform"
  config.vm.hostname = vm_name

  config.vm.network :forwarded_port, guest:80, host:6280
  # ssh port
  config.vm.network :forwarded_port, guest:22, host:2300
  # develop port
  config.vm.network :forwarded_port, guest:6200, host:6200
  config.vm.network :forwarded_port, guest:6201, host:6201
  # local develop port
  config.vm.network :forwarded_port, guest:6220, host:6220
  config.vm.network :forwarded_port, guest:6221, host:6221

  config.ssh.private_key_path = "C:/Users/wangdp/.ssh/id_rsa"
  config.ssh.password = "vagrant"

  config.vm.synced_folder ".", "/vagrant", type: "virtualbox"
  config.vm.synced_folder "D:/windroc/project/nwp/sms/smslog", "/smslog", type: "virtualbox"

  config.vm.provider :virtualbox do |vb|
      vb.gui = false
      vb.customize ["modifyvm", :id, "--memory", "2048"]
  end

  config.vm.provision "shell", inline: <<-SHELL
    echo "Installing softwares..."
    yum groups mark convert
    yum group install -y "Development tools"
    yum install -y zlib-devel bzip2-devel openssl-devel ncurses-devel sqlite-devel readline-devel tk-devel gdbm-devel db4-devel libpcap-devel xz-devel
    yum install -y epel-release
    yum upgrade
    yum install -y mariadb-devel

    echo "Installing python 3..."
    cd /home/vagrant
    mkdir app
    cd app
    wget -q https://www.python.org/ftp/python/3.5.2/Python-3.5.2.tgz
    tar -xvf Python-3.5.2.tgz
    cd Python-3.5.2
    ./configure --enable-unicode=ucs4
    make
    make install
    chown -R vagrant:vagrant /home/vagrant/app

    echo "Installing MySQL Connector/Python..."
    cd /home/vagrant
    test -d app || mkdir app
    cd app
    wget http://cdn.mysql.com//Downloads/Connector-Python/mysql-connector-python-2.1.3.tar.gz
    tar -xvf mysql-connector-python-2.1.3.tar.gz
    cd mysql-connector-python-2.1.3
    python3 setup.py build
    sudo /usr/local/bin/python3 setup.py install

    echo "Installing python packages..."
    sudo /usr/local/bin/pip3 install pymongo redis flask flask-sqlalchemy pyyaml kafka-python celery alembic requests fabric3
  SHELL
end

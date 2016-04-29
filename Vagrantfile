Vagrant.configure("2") do |c|
  c.ssh.insert_key = false
  c.vm.define 'centos72' do |v|
    v.vm.hostname = 'centos7-2.test.net'
    v.vm.box = 'puppetlabs/centos-7.0-64-nocm'
    v.vm.box_url = 'https://vagrantcloud.com/puppetlabs/boxes/centos-7.0-64-nocm'
    v.vm.box_check_update = 'true'
    v.vm.network :private_network, ip: "10.255.233.156", :netmask => "255.255.0.0", :mac => "080027E36203"
    v.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', '1024', '--cpus', '1']
    end
  end

  c.vm.define 'centos66' do |v|
    v.vm.hostname = 'centos66'
    v.vm.box = 'puppetlabs/centos-6.6-64-nocm'
    v.vm.box_url = 'https://vagrantcloud.com/puppetlabs/boxes/centos-6.6-64-nocm'
    v.vm.box_check_update = 'true'
    v.vm.network :private_network, ip: "10.255.44.245", :netmask => "255.255.0.0", :mac => "0800279685F7"
    v.vm.provider :virtualbox do |vb|
      vb.customize ['modifyvm', :id, '--memory', '1024', '--cpus', '1']
    end
  end
end

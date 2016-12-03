#!/usr/bin/env ruby

require 'fileutils'

unless File.directory?('dist')
  FileUtils.mkdir('dist')
end

src_dir = 'src'
el6_version = '8.0.39'
el7_version = '8.0.39'
el6_target = "apache-tomcat-#{el6_version}.tar.gz"
el7_target = "apache-tomcat-#{el7_version}.tar.gz"
url_src = 'http://archive.apache.org/dist/tomcat/tomcat-8/v%%VERSION%%/bin/apache-tomcat-%%VERSION%%.tar.gz'
rpmdir = %x(rpm --eval %{_topdir}).strip

# Need v30 for EL6
unless File.exist?(File.join(src_dir,el6_target))
  %x(curl -o #{File.join(src_dir,el6_target)} #{url_src.gsub('%%VERSION%%',el6_version)})
end

# Also need a newer version of APR for EL6

apr = 'apr-1.5.2'

FileUtils.mkdir('apr') unless File.directory?('apr')

Dir.chdir('apr') do
  unless File.exist?("#{apr}.tar.bz2")
    %x(curl -O http://mirror.cc.columbia.edu/pub/software/apache/apr/#{apr}.tar.bz2)
  end

  unless File.exist?("#{apr}-1.src.rpm")
    %x(rpmbuild -ts #{apr}.tar.bz2)
    Dir.glob("#{rpmdir}/SRPMS/apr*.rpm").each do |rpm|
      FileUtils.mv(rpm,Dir.pwd)
    end
  end

  unless File.exist?("#{apr}-1.x86_64.rpm")
    %x(mock -r epel-6-x86_64 --resultdir=#{Dir.pwd} #{apr}-1.src.rpm)
  end
end

%x(mock -r epel-6-x86_64 --buildsrpm --resultdir=`pwd`/dist --source=`pwd`/src --spec=`pwd`/src/tomcat.spec)
%x(mock -r epel-6-x86_64 --install `pwd`/apr/*4.rpm)
%x(mock -r epel-6-x86_64 --resultdir=`pwd`/dist --no-clean dist/*el6*.src.rpm)

# Need v33 for EL6
unless File.exist?(File.join(src_dir,el7_target))
  %x(curl -o #{File.join(src_dir,el7_target)} #{url_src.gsub('%%VERSION%%',el7_version)})
end

%x(mock -r epel-7-x86_64 --buildsrpm --resultdir=`pwd`/dist --source=`pwd`/src --spec=`pwd`/src/tomcat.spec)
%x(mock -r epel-7-x86_64 --resultdir=`pwd`/dist --no-clean dist/*el7*.src.rpm)

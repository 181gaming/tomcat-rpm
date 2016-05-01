#!/usr/bin/env ruby

require 'fileutils'

unless File.directory?('dist')
  FileUtils.mkdir('dist')
end

%x(mock -r epel-6-x86_64 --buildsrpm --resultdir=`pwd`/dist --source=`pwd`/src --spec=`pwd`/src/tomcat.spec)
%x(mock -r epel-6-x86_64 --install `pwd`/apr/*4.rpm)
%x(mock -r epel-6-x86_64 --resultdir=`pwd`/dist --no-clean dist/*el6*.src.rpm)

%x(mock -r epel-7-x86_64 --buildsrpm --resultdir=`pwd`/dist --source=`pwd`/src --spec=`pwd`/src/tomcat.spec)
%x(mock -r epel-7-x86_64 --resultdir=`pwd`/dist --no-clean dist/*el7*.src.rpm)

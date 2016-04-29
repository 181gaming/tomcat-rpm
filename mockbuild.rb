#!/usr/bin/env ruby

require 'fileutils'

unless File.directory?('dist')
  FileUtils.mkdir('dist')
end

[
  '7'
].each do |ver|
  %x(mock -r epel-#{ver}-x86_64 --buildsrpm --resultdir=`pwd`/dist --source=`pwd`/src --spec=`pwd`/src/tomcat.spec)
  %x(mock -r epel-#{ver}-x86_64 --resultdir=`pwd`/dist --no-cleanup-after dist/*el7*.src.rpm)
end

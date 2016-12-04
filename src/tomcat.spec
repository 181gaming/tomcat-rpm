%define major_version 8
%define minor_version 0
# EL6 Doesn't support anything greater than version 30 due to incompatibilities
# with the native OpenSSL

%if 0%{?el6:1}
%define micro_version 30
%else
%define micro_version 33
%endif

%define appname tomcat
%define distname %{name}-%{version}

%define basedir %{_var}/lib/%{name}
%define appdir %{basedir}/webapps
%define bindir %{_datadir}/%{name}/bin
%define libdir %{_datadir}/%{name}/lib
%define confdir %{_sysconfdir}/%{name}
%define homedir %{_datadir}/%{name}
%define logdir %{_var}/log/%{name}
%define piddir %{_var}/run/%{name}
%define cachedir %{_var}/cache/%{name}
%define tempdir %{cachedir}/temp
%define workdir %{cachedir}/work

%define appuser tomcat
%define appuid 91
%define appgid 91

%if 0%{?rhel}%{?fedora}
%define _java_home %{_jvmdir}/java
%endif

Name: tomcat8
Version: %{major_version}.%{minor_version}.%{micro_version}
Release: 0%{?dist}
Epoch: 0
Summary: Open source software implementation of the Java Servlet and JavaServer Pages technologies.
Group: System Environment/Daemons
License: ASL 2.0
URL: http://tomcat.apache.org
Source0: http://www.apache.org/dist/tomcat/tomcat-%{major_version}/v%{version}/bin/apache-%{appname}-%{version}.tar.gz
Source1: tomcat.sysconfig
Source2: tomcat.init.sh
Source3: tomcat.logrotate.sh
Source4: tomcat-digest.script
Source5: setenv.sh
Source7: tomcat.service
Source14: tomcat.conf
Source15: tomcat-functions
Source16: tomcat-jsvc.service
Source18: tomcat-named.service
Source19: tomcat-preamble
Source20: tomcat-server
Source22: tomcat-tool-wrapper.script
Source23: tomcat.wrapper
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: x86_64

# The _jdk_require is passed via `rpmbuild --define "_jdk_require ..."`
%if 0%{?rhel}%{?fedora}
Requires: java >= 1.7
Requires: java-devel >= 1.7
%else
Requires: jdk >= 1.7
%endif

Requires: apr >= 0:1.4.0
Requires: libtool
Requires: libcap

%if 0%{?rhel}%{?fedora}
BuildRequires: java >= 1.7
BuildRequires: java-devel >= 1.7
%else
BuildRequires: jdk >= 1.7
%endif

BuildRequires: apr-devel >= 0:1.4.0
BuildRequires: openssl-devel >= 0:0.9.7
BuildRequires: autoconf, libtool, doxygen
BuildRequires: libcap-devel

%description
Tomcat is the servlet container that is used in the official Reference
Implementation for the Java Servlet and JavaServer Pages technologies.
The Java Servlet and JavaServer Pages specifications are developed by
Sun under the Java Community Process.


%package manager
Summary: The management web application of Apache Tomcat.
Group: System Environment/Applications
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description manager
The management web application of Apache Tomcat.

%package host-manager
Summary: The host-management web application of Apache Tomcat.
Group: System Environment/Applications
Requires: %{name} = %{version}-%{release}
BuildArch: noarch

%description host-manager
The host-management web application of Apache Tomcat.

%package javadoc
Group: Documentation
Summary: Javadoc generated documentation for Apache Tomcat
Requires: jpackage-utils

%description javadoc
Javadoc generated documentation for Apache Tomcat.

%prep
%setup -q -b 0 -T -n apache-%{appname}-%{version}

%build
# The _java_home is passed via `rpmbuild --define "_java_home ..."`
cd bin
tar -xzf tomcat-native.tar.gz
tcnative=`ls -d tomcat-native-*-src | head -1`
%if 0%{?el6:1}
ln -s $tcnative/jni tcnative
%else
ln -s $tcnative tcnative
%endif

cd tcnative/native
./configure --with-apr=/usr/bin/apr-1-config --with-ssl=yes --with-java-home=%{_java_home}
make -I%{_java_home}/include/linux
cd -

tar -xzf commons-daemon-native.tar.gz
commons_daemon=`ls -d commons-daemon-*-native-src | head -1`
ln -s $commons_daemon commons-daemon
cd commons-daemon/unix
./configure --with-java=%{_java_home}
make -I%{_java_home}/include/linux
cd -

%install
# build initial path structure
rm -rf %{buildroot}

%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -d -m 0755 %{buildroot}%{_sbindir}
%{__install} -d -m 0755 %{buildroot}%{_javadocdir}/%{name}
%{__install} -d -m 0755 %{buildroot}%{_systemddir}
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -d -m 0755 %{buildroot}%{appdir}
%{__install} -d -m 0755 %{buildroot}%{bindir}
%{__install} -d -m 0775 %{buildroot}%{confdir}
%{__install} -d -m 0775 %{buildroot}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 %{buildroot}%{confdir}/conf.d
/bin/echo "Place your custom *.conf files here. Shell expansion is supported." > %{buildroot}%{confdir}/conf.d/README
%{__install} -d -m 0755 %{buildroot}%{libdir}
%{__install} -d -m 0775 %{buildroot}%{logdir}
/bin/touch %{buildroot}%{logdir}/catalina.out
%{__install} -d -m 0775 %{buildroot}%{_localstatedir}/run
%{__install} -d -m 0775 %{buildroot}%{_localstatedir}/lib/tomcats
/bin/touch %{buildroot}%{_localstatedir}/run/%{name}.pid
/bin/echo "%{name}-%{major_version}.%{minor_version}.%{micro_version} RPM installed" >> %{buildroot}%{logdir}/catalina.out
%{__install} -d -m 0775 %{buildroot}%{homedir}
%{__install} -d -m 0775 %{buildroot}%{tempdir}
%{__install} -d -m 0775 %{buildroot}%{workdir}

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%{__install} -d -m 0755 %{buildroot}%{_unitdir}
%else
%{__install} -d -m 0755 %{buildroot}%{_initddir}
%endif

%{__install} -d -m 0755 %{buildroot}%{_libexecdir}/%{name}

pushd %{buildroot}/%{homedir}
    # %{__ln_s} %{appdir} webapps
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
popd

pushd %{buildroot}/%{basedir}
    %{__ln_s} %{confdir} conf
    %{__ln_s} %{logdir} logs
    %{__ln_s} %{tempdir} temp
    %{__ln_s} %{workdir} work
popd

%{__install} -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Copy Tomcat files to package root
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/bin/*.{jar,xml} %{buildroot}%{bindir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/bin/*.sh %{buildroot}%{bindir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/conf/*.{policy,properties,xml} %{buildroot}%{confdir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/lib/*.jar %{buildroot}%{libdir}
# %{__cp} -a %{_builddir}/apache-%{appname}-%{version}/webapps/{ROOT,manager,host-manager} %{buildroot}%{appdir}

# javadoc
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE14} \
    > %{buildroot}%{confdir}/%{appname}.conf
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE1} \
    > %{buildroot}%{_sysconfdir}/sysconfig/%{name}
%{__install} -m 0644 %{SOURCE23} \
    %{buildroot}%{_sbindir}/%{name}

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%{__install} -m 0644 %{SOURCE16} \
    %{buildroot}%{_unitdir}/%{name}-jsvc.service
%{__install} -m 0644 %{SOURCE7} \
    %{buildroot}%{_unitdir}/%{name}.service
%{__install} -m 0644 %{SOURCE18} %{buildroot}%{_unitdir}/%{name}@.service
%else
%{__install} -m 0644 %{SOURCE2} \
    %{buildroot}%{_initddir}/%{name}
%endif

%{__sed} -e "s|\@\@\@TCLOG\@\@\@|%{logdir}|g" %{SOURCE3} \
    > %{buildroot}%{_sysconfdir}/logrotate.d/%{name}
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE4} \
    > %{buildroot}%{_bindir}/%{name}-digest
%{__sed} -e "s|\@\@\@TCHOME\@\@\@|%{homedir}|g" \
   -e "s|\@\@\@TCTEMP\@\@\@|%{tempdir}|g" \
   -e "s|\@\@\@LIBDIR\@\@\@|%{_libdir}|g" %{SOURCE22} \
    > %{buildroot}%{_bindir}/%{name}-tool-wrapper

%{__install} -m 0644 %{SOURCE15} %{buildroot}%{_libexecdir}/%{name}/functions
%{__install} -m 0644 %{SOURCE19} %{buildroot}%{_libexecdir}/%{name}/preamble
%{__install} -m 0644 %{SOURCE20} %{buildroot}%{_libexecdir}/%{name}/server

# Substitute libnames in catalina-tasks.xml
sed -i \
   "s,el-api.jar,%{name}-el-%{elspec}-api.jar,;
    s,servlet-api.jar,%{name}-servlet-%{servletspec}-api.jar,;
    s,jsp-api.jar,%{name}-jsp-%{jspspec}-api.jar,;" \
    %{buildroot}%{bindir}/catalina-tasks.xml

# Copy Tomcat Native files to package root
%{__install} -m 0755 %{SOURCE5} %{buildroot}%{bindir}
cd bin/tcnative/native
make install DESTDIR=%{buildroot}
cd -

# Copy JSVC to the package
%{__install} -m 0755 bin/commons-daemon/unix/jsvc %{buildroot}%{bindir}

mkdir -p %{buildroot}%{_prefix}/lib/tmpfiles.d
cat > %{buildroot}%{_prefix}/lib/tmpfiles.d/%{name}.conf <<EOF
f %{_localstatedir}/run/%{name}.pid 0644 tomcat tomcat -
EOF

chmod +x %{buildroot}%{bindir}/*.sh
chmod +x %{buildroot}%{bindir}/jsvc

%clean
%{__rm} -rf %{buildroot}

%pre
%{_sbindir}/groupadd -g %{appgid} -r %{appuser} 2>/dev/null || :
%{_sbindir}/useradd -c "Apache Tomcat" -u %{appuid} -g %{appuser} -s /bin/sh -r -d %{homedir} %{appuser} 2>/dev/null || :

%post
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%systemd_post %{name}.service
%else
  /usr/bin/libtool --finish /usr/local/apr/lib
  /sbin/chkconfig --add %{name}
%endif

%preun
%{__rm} -rf %{workdir}/* %{tempdir}/*
if [ "$1" = "0" ]; then

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%systemd_preun %{name}.service
%else
  %{_initddir}/%{name} stop >/dev/null 2>&1
  /sbin/chkconfig --del %{name}
%endif

fi
/sbin/ldconfig

%postun
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%systemd_postun_with_restart %{name}.service
%endif

%files
%{bindir}

%defattr(0664,root,tomcat,0755)
%doc {LICENSE,NOTICE,RELEASE*}
%{basedir}
%attr(0755,root,root) %{_bindir}/%{name}-digest
%attr(0755,root,root) %{_bindir}/%{name}-tool-wrapper
%attr(0755,root,root) %{_sbindir}/%{name}

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%attr(0644,root,root) %{_unitdir}/%{name}-jsvc.service
%attr(0644,root,root) %{_unitdir}/%{name}.service
%attr(0644,root,root) %{_unitdir}/%{name}@.service
%else
%attr(0755 root root) %{_initddir}/%{name}
%endif

%attr(0755,root,root) %dir %{_libexecdir}/%{name}
%attr(0755,root,root) %dir %{_localstatedir}/lib/tomcats
%attr(0644,root,root) %{_libexecdir}/%{name}/functions
%attr(0755,root,root) %{_libexecdir}/%{name}/preamble
%attr(0755,root,root) %{_libexecdir}/%{name}/server
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{name}
%config(noreplace) %{_sysconfdir}/sysconfig/%{name}
%attr(0755,root,tomcat) %dir %{basedir}
%attr(0755,root,tomcat) %dir %{confdir}
%defattr(0664,tomcat,root,0770)
%attr(0770,tomcat,root) %dir %{logdir}
%defattr(0664,root,tomcat,0770)
%attr(0660,tomcat,tomcat) %{logdir}/catalina.out
%attr(0644,tomcat,tomcat) %{_localstatedir}/run/%{name}.pid
%attr(0770,root,tomcat) %dir %{cachedir}
%attr(0770,root,tomcat) %dir %{tempdir}
%attr(0770,root,tomcat) %dir %{workdir}
%defattr(0664,root,tomcat,0775)
%attr(0775,root,tomcat) %dir %{appdir}
%attr(0775,root,tomcat) %dir %{confdir}/Catalina
%attr(0775,root,tomcat) %dir %{confdir}/Catalina/localhost
%attr(0775,root,tomcat) %dir %{confdir}/conf.d
%attr(0664,tomcat,tomcat) %{confdir}/conf.d/README
%attr(0664,tomcat,tomcat) %config(noreplace) %{confdir}/%{appname}.conf
%attr(0664,tomcat,tomcat) %config(noreplace) %{confdir}/*.policy
%attr(0664,tomcat,tomcat) %config(noreplace) %{confdir}/*.properties
%attr(0664,tomcat,tomcat) %config(noreplace) %{confdir}/context.xml
%attr(0664,tomcat,tomcat) %config(noreplace) %{confdir}/server.xml
%attr(0660,tomcat,tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%attr(0664,tomcat,tomcat) %config(noreplace) %{confdir}/web.xml
%dir %{homedir}
%{_prefix}/lib/tmpfiles.d/%{name}.conf
%{homedir}/lib
%{homedir}/temp
%{homedir}/work
%{homedir}/logs
%{homedir}/conf
%{homedir}/webapps

# Tomcat native files
%attr(0755 root root) /usr/local/apr/

# %files manager
# %defattr(0644 root root 0755)
# %{appdir}/manager

# %files host-manager
# %defattr(0644 root root 0755)
# %{appdir}/host-manager

%files javadoc
%defattr(-,root,root,-)
%{_javadocdir}/%{name}

%changelog
* Fri Dec 02 2016 Nicholas Houle <181gaming@gmail.com> - 8.0.30%{?dist}
- Removed webapps hostmanager and manager
* Tue Aug 16 2016 Nicholas Houle <181gaming@gmail.com> - 8.0.30%{?dist}
- Updated Tomcat to version 8.0.30
* Mon May 18 2015 James Sumners <james.sumners@gmail.com> - 8.0.22%{?dist}
- Updated Tomcat to version 8.0.22
* Tue Feb 03 2015 James Sumners <james.sumners@gmail.com> - 8.0.18%{?dist}
- Updated Tomcat to version 8.0.18
* Fri Dec 19 2014 James Sumners <james.sumners@gmail.com> - 8.0.15%{?dist}
- Updated Tomcat to version 8.0.15
* Wed Feb 19 2014 James Sumners <james.sumners@gmail.com> - 7.0.52%{?dist}
- Updated Tomcat version to 7.0.52 (fixes CVE-2014-0050)
* Mon Feb 03 2014 James Sumners <james.sumners@gmail.com> - 7.0.50%{?dist}
- Updated Tomcat version to 7.0.50
* Wed Dec 04 2013 James Sumners <james.sumners@gmail.com> - 7.0.47%{?dist}
- Updated to use predefined variables for the Java home and JDK virtual package
- Added requires line for libtool to the base apache-tomcat package
* Wed Oct 30 2013 James Sumners <james.sumners@gmail.com> - 7.0.47%{?dist}
- Added Tomcat Native
- Added JSVC
* Fri Nov 30 2012 Joseph Lamoree <jlamoree@ecivis.com> - 7.0.33-1%{?dist}
- First packaging of Apache Tomcat for eCivis apps
- TODO Tomcat native connector
- TODO Support for multiple instances

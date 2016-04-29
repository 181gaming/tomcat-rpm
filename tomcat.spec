%define major_version 8
%define minor_version 0
%define micro_version 33
%define appname tomcat
%define distname %{name}-%{version}

%define basedir %{_var}/lib/%{appname}
%define appdir %{basedir}/webapps
%define bindir %{_datadir}/%{appname}/bin
%define libdir %{_datadir}/%{appname}/lib
%define confdir %{_sysconfdir}/%{appname}
%define homedir %{_datadir}/%{appname}
%define logdir %{_var}/log/%{appname}
%define piddir %{_var}/run/%{appname}
%define cachedir %{_var}/cache/%{appname}
%define tempdir %{cachedir}/temp
%define workdir %{cachedir}/work

%define appuser tomcat
%define appuid 91
%define appgid 91

%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
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
Source4: tomcat-native.tar.gz
Source5: setenv.sh
Source6: commons-daemon-native.tar.gz
Source7: tomcat.service
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: x86_64

# The _jdk_require is passed via `rpmbuild --define "_jdk_require ..."`
%if 0%{?rhel}%{?fedora}
Requires: java-devel >= 1.7
%else
Requires: jdk >= 1.7
%endif
Requires: apr >= 0:1.1.29
Requires: libtool
Requires: libcap

%if 0%{?rhel}%{?fedora}
BuildRequires: java-devel >= 1.7
%else
BuildRequires: jdk >= 1.7
%endif
BuildRequires: apr-devel >= 0:1.1.29
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

%prep
%setup -q -b 0 -T -n apache-%{appname}-%{version}
%setup -q -b 4 -T -n tcnative
%setup -q -b 6 -T -n commons-daemon

# Without this, RPM likes to think the main source
# directory is the previously unpacked tarball.
# That's not true and it makes the %files section bomb.
%setup -q -b 0 -T -n apache-%{appname}-%{version}

# The _java_home is passed via `rpmbuild --define "_java_home ..."`
%build
cd %{_topdir}/BUILD/tcnative/native
./configure --with-apr=/usr/bin/apr-1-config --with-ssl=yes --with-java-home=%{_java_home}
make -I%{_java_home}/include/linux

cd %{_topdir}/BUILD/commons-daemon/unix
./configure --with-java=%{_java_home}
make -I%{_java_home}/include/linux

%install
rm -rf %{buildroot}
%{__install} -d -m 0755 %{buildroot}%{_bindir}
%{__install} -d -m 0755 %{buildroot}%{_sbindir}
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%{__install} -d -m 0755 %{buildroot}%{_unitdir}
%else
%{__install} -d -m 0755 %{buildroot}%{_initrddir}
%endif
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/logrotate.d
%{__install} -d -m 0755 %{buildroot}%{_sysconfdir}/sysconfig
%{__install} -d -m 0775 %{buildroot}%{appdir}
%{__install} -d -m 0755 %{buildroot}%{bindir}
%{__install} -d -m 0755 %{buildroot}%{libdir}
%{__install} -d -m 0755 %{buildroot}%{confdir}
%{__install} -d -m 0775 %{buildroot}%{confdir}/Catalina/localhost
%{__install} -d -m 0775 %{buildroot}%{logdir}
%{__install} -d -m 0775 %{buildroot}%{piddir}
%{__install} -d -m 0775 %{buildroot}%{homedir}
%{__install} -d -m 0775 %{buildroot}%{tempdir}
%{__install} -d -m 0775 %{buildroot}%{workdir}

pushd %{buildroot}/%{homedir}
    %{__ln_s} %{appdir} webapps
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
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%{__install} -m 0644 %{SOURCE7} %{buildroot}%{_unitdir}/%{name}.service
%else
%{__install} -m 0755 %{SOURCE2} %{buildroot}%{_initrddir}/%{name}
%endif
%{__install} -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/logrotate.d/%{name}

# Copy Tomcat files to package root
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/bin/*.{jar,xml} %{buildroot}%{bindir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/bin/*.sh %{buildroot}%{bindir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/conf/*.{policy,properties,xml} %{buildroot}%{confdir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/lib/*.jar %{buildroot}%{libdir}
%{__cp} -a %{_builddir}/apache-%{appname}-%{version}/webapps/{ROOT,manager,host-manager} %{buildroot}%{appdir}

# Copy Tomcat Native files to package root
%{__install} -m 0755 %{SOURCE5} %{buildroot}%{bindir}
cd %{_topdir}/BUILD/tcnative/native
make install DESTDIR=%{buildroot}

# Copyt JSVC to the package
%{__install} -m 0755 %{_builddir}/commons-daemon/unix/jsvc %{buildroot}%{bindir}

%clean
%{__rm} -rf %{buildroot}

%pre
%{_sbindir}/groupadd -g %{appgid} -r %{appuser} 2>/dev/null || :
%{_sbindir}/useradd -c "Apache Tomcat" -u %{appuid} -g %{appuser} -s /bin/sh -r -d %{homedir} %{appuser} 2>/dev/null || :

%post
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
systemctl enable %{appname}
%else
  /usr/bin/libtool --finish /usr/local/apr/lib
  /sbin/chkconfig --add %{appname}
%endif

%preun
%{__rm} -rf %{workdir}/* %{tempdir}/*
if [ "$1" = "0" ]; then
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
  systemctl stop %{appname}
  systemctl disable %{appname}
%else
  %{_initrddir}/%{appname} stop >/dev/null 2>&1
  /sbin/chkconfig --del %{appname}
%endif
fi
/sbin/ldconfig


# RPM 4.8 has a bug in defattr() with dir mode
%files
#%defattr(0644 root root 0755)
%doc LICENSE NOTICE RELEASE-NOTES
%attr(0775 root tomcat) %dir %{logdir}
%attr(0775 tomcat tomcat) %dir %{piddir}
%if 0%{?rhel} >= 7 || 0%{?fedora} >= 20
%attr(0644 root root) %{_unitdir}/%{name}.service
%else
%attr(0755 root root) %{_initrddir}/%{appname}
%endif
%attr(0644 root root) %config(noreplace) %{_sysconfdir}/logrotate.d/%{appname}
%config(noreplace) %{_sysconfdir}/sysconfig/%{appname}
%dir %{basedir}
%{basedir}/conf
%{basedir}/logs
%{basedir}/temp
%{basedir}/work
%attr(0775 root tomcat) %dir %{appdir}
%{appdir}/ROOT
%dir %{confdir}
%dir %{confdir}/Catalina
%attr(0775 root tomcat) %dir %{confdir}/Catalina/localhost
%config(noreplace) %{confdir}/*.policy
%config(noreplace) %{confdir}/*.properties
%config(noreplace) %{confdir}/context.xml
%config(noreplace) %{confdir}/server.xml
%attr(0660 root tomcat) %config(noreplace) %{confdir}/tomcat-users.xml
%config(noreplace) %{confdir}/web.xml
%attr(0775 root tomcat) %dir %{cachedir}
%attr(0775 root tomcat) %dir %{tempdir}
%attr(0775 root tomcat) %dir %{workdir}
%attr(- root root) %{homedir}

# Tomcat native files
%attr(0755 root root) /usr/local/apr/

%files manager
%defattr(0644 root root 0755)
%{appdir}/manager


%files host-manager
%defattr(0644 root root 0755)
%{appdir}/host-manager


%changelog
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


#!/bin/sh
#
# tomcat	Apache Tomcat Java Servlets and JSP server
#
# chkconfig: 345 85 15
# description: Apache Tomcat Java Servlets and JSP server

source /etc/rc.d/init.d/functions

APPNAME='tomcat8'
USER='tomcat'
LOCKFILE="/var/lock/subsys/${APPNAME}"

TOMCAT_HOME="/usr/share/${APPNAME}"
CATALINA_HOME="${TOMCAT_HOME}"
CATALINA_BASE="/var/lib/${APPNAME}"
CATALINA_OUT="/var/log/${APPNAME}/catalina.out"
CATALINA_PID="/var/run/${APPNAME}/tomcat.pid"
#CATALINA_OPTS="-Xmx512m -Djava.awt.headless=true"
JAVA_HOME="/usr/lib/jvm/java"

JSVC_PID="/var/run/${APPNAME}/jsvc.pid"
JSVC_CP=${TOMCAT_HOME}/bin/commons-daemon.jar:${TOMCAT_HOME}/bin/bootstrap.jar:${TOMCAT_HOME}/bin/tomcat-juli.jar
JSVC_OUT="${CATALINA_OUT}"
JSVC_ERR="/var/log/${APPNAME}/catalina.err"
if [ -r "${TOMCAT_HOME}/conf/logging.properties" ]; then
  JSVC_LOGGING="-Djava.util.logging.config.file=${TOMCAT_HOME}/conf/logging.properties"
else
  JSVC_LOGGING="-Dnop"
fi

if [ -r /etc/sysconfig/${APPNAME} ]; then
  source /etc/sysconfig/${APPNAME}
fi

export CATALINA_HOME CATALINA_BASE CATALINA_OUT CATALINA_PID JAVA_HOME

function start_server {
  echo -n "Starting ${APPNAME}: "
  status -p ${JSVC_PID} ${APPNAME} > /dev/null && failure && exit
  
  if [ -r /usr/share/${APPNAME}/bin/setenv.sh ]; then
    source /usr/share/${APPNAME}/bin/setenv.sh
    export JAVA_OPTS
  fi

  source /etc/tomcat8/tomcat.conf
  source /etc/sysconfig/tomcat8

  if [ $(id -u) = "0" ]; then
    if [ ! -d "/var/run/${APPNAME}" ]; then
      install -m 0755 -o root -g ${USER} -d /var/run/${APPNAME}
    fi
  fi

  daemon --user=${USER} /usr/libexec/${APPNAME}/server start >& ${CATALINA_OUT} 2>&1 &

  if [ $? -eq 0 ]; then
    echo $! > ${JSVC_PID}
    touch ${LOCKFILE} &&  success
  fi

  echo
}

function stop_server {
  echo -n "Stopping ${APPNAME}: "

  status -p ${JSVC_PID} ${APPNAME} > /dev/null
  if [ ! $? -eq 0 ]; then
    failure
    echo
    exit
  fi

  if [ -r /usr/share/${APPNAME}/bin/setenv.sh ]; then
    source /usr/share/${APPNAME}/bin/setenv.sh
  fi

  source /etc/tomcat8/tomcat.conf
  source /etc/sysconfig/tomcat8

  /usr/libexec/${APPNAME}/server stop >& ${CATALINA_OUT} 2>&1

  if [ $? -eq 0 ]; then
    rm ${JSVC_PID}
    rm ${LOCKFILE} && success
  else
    failure
  fi

  echo
}

case "$1" in
  start)
    start_server
    ;;
  stop)
    stop_server
    ;;
  restart)
    stop_server
    start_server
    ;;
  condrestart)
    [ -e ${LOCKFILE} ] && $0 restart
    ;;
  status)
    status -p ${JSVC_PID} ${APPNAME}
    ;;
  *)
    echo "Usage: $0 {start|stop|restart|condrestart|status}"
    exit 1
    ;;
esac
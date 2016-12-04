/var/log/tomcat8/*.txt
/var/log/tomcat8/*.log {
    daily
    rotate 7
    notifempty
    missingok
    compress
    size 10M
    create 0640 tomcat tomcat
}

/var/log/tomcat8/catalina.out {
    copytruncate
    daily
    rotate 7
    missingok
    compress
    size 100M
    create 0640 tomcat tomcat
}


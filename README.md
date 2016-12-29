# tomcat-rpm

## Overview

This project defines a build system for building Apache Tomcat 8.0.x
source and binary RPM files. The included `mockbuild.rb` *must* be used to kick off
the RPM building process. The SPEC file assumes various work is done by the
script; e.g. the Tomcat packages being extracted and compiled in the corre
locations. 

Further, the SPEC file relies on `_java_home` and `_jdk_require` build variables
to be set according to the Java packages installed on the build system (and, in
turn, the target install system[s]). That is, if you are using the community
build Java packages, these variables will be set to "/usr/java/latest" and
"jdk", respectively. If you are using the RedHat packages, like the
java-1.8.0-oracle and java-1.8.0-oracle-devel packages, then they would be
set to "/usr/lib/jvm/java" and "java-sdk". The `mockbuild.rb` script does this
for you.


## Setup

### Setup requirements


##### `rvm`

```
# https://rvm.io/rvm/install

\curl -sSL https://get.rvm.io | bash -s stable --ruby
```

##### `dnf`

```
sudo dnf install rpm-build mock ImageMagick-devel ImageMagick
```

##### `yum`

```
sudo yum install rpm-build mock ImageMagick-devel ImageMagick
```

##### `Gems`

```
gem install fileutils ruby-build
```


## Build

### Run build script

```
./mockbuild.rb
```

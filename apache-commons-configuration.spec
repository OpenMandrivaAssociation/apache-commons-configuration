
%global base_name       configuration
%global short_name      commons-%{base_name}

Name:           apache-%{short_name}
Version:        1.6
Release:        7
Summary:        Commons Configuration Package

Group:          Development/Java
License:        ASL 2.0
URL:            http://commons.apache.org/%{base_name}/
Source0:        http://www.apache.org/dist/commons/%{base_name}/source/%{short_name}-%{version}-src.tar.gz
Patch0:         0001-Change-ant-groupId-to-org.apache.ant.patch
Patch1:         0002-Remove-test-deps.patch
BuildArch:      noarch

BuildRequires:  java-devel
BuildRequires:  jpackage-utils >= 0:1.7.2
BuildRequires:  maven-doxia-sitetools
BuildRequires:  maven-plugin-bundle
BuildRequires:  maven-surefire-maven-plugin
BuildRequires:  maven-surefire-provider-junit
BuildRequires:  maven2-plugin-antrun
BuildRequires:  maven2-plugin-assembly
BuildRequires:  maven2-plugin-compiler
BuildRequires:  maven2-plugin-idea
BuildRequires:  maven2-plugin-install
BuildRequires:  maven2-plugin-jar
BuildRequires:  maven2-plugin-javadoc
BuildRequires:  maven2-plugin-resources
BuildRequires:  maven

BuildRequires:  xalan-j2
BuildRequires:  xerces-j2
BuildRequires:  xml-commons-apis
BuildRequires:  apache-commons-beanutils >= 0:1.7.0
BuildRequires:  apache-commons-codec
BuildRequires:  apache-commons-lang
BuildRequires:  apache-commons-logging
# convert to apache-commons when transition is done
BuildRequires:  apache-commons-collections
BuildRequires:  jakarta-commons-dbcp
BuildRequires:  apache-commons-digester
BuildRequires:  apache-commons-jxpath
BuildRequires:  jakarta-commons-pool
BuildRequires:  servlet25
BuildRequires:  tomcat6

Requires:  servlet25
Requires:  apache-commons-beanutils >= 0:1.7.0
Requires:  apache-commons-codec
Requires:  apache-commons-jxpath
Requires:  apache-commons-lang
Requires:  apache-commons-logging
Requires:  apache-commons-collections
Requires:  jakarta-commons-dbcp
Requires:  apache-commons-digester
Requires:  jakarta-commons-pool
Requires:  xerces-j2
Requires:  xml-commons-apis

Requires(post):   jpackage-utils >= 1.7.2
Requires(postun): jpackage-utils >= 1.7.2

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

Provides:       jakarta-%{short_name} = 0:%{version}-%{release}
Obsoletes:      jakarta-%{short_name} < 0:%{version}-%{release}

%description
Configuration is a project to provide a generic Configuration
interface and allow the source of the values to vary. It
provides easy typed access to single, as well as lists of
configuration values based on a 'key'.
Right now you can load properties from a simple properties
file, a properties file in a jar, an XML file, JNDI settings,
as well as use a mix of different sources using a
ConfigurationFactory and CompositeConfiguration.
Custom configuration objects are very easy to create now
by just subclassing AbstractConfiguration. This works
similar to how AbstractList works.

%package        javadoc
Summary:        API documentation for %{name}
Group:          Development/Java
Requires:       jpackage-utils

Provides:       jakarta-%{short_name}-javadoc = 0:%{version}-%{release}
Obsoletes:      jakarta-%{short_name}-javadoc < 0:%{version}-%{release}

%description    javadoc
%{summary}.


%prep
%setup -q -n %{short_name}-%{version}-src
%patch0 -p1
%patch1 -p1
%{__sed} -i 's/\r//' LICENSE.txt

%build
# we skip tests because we don't have test deps
mvn-rpmbuild -Dmaven.test.skip=true \
        install javadoc:javadoc

%install
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}
install -p -m 644 target/%{short_name}-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}.jar
ln -sf %{name}.jar $RPM_BUILD_ROOT%{_javadir}/%{short_name}.jar


# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}
cp -pr target/site/apidocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# Install pom
install -d -m 755 $RPM_BUILD_ROOT%{_mavenpomdir}
install -pm 644 pom.xml $RPM_BUILD_ROOT/%{_mavenpomdir}/JPP-%{short_name}.pom
%add_to_maven_depmap org.apache.commons %{short_name} %{version} JPP %{short_name}

# following line is only for backwards compatibility. New packages
# should use proper groupid org.apache.commons and also artifactid
%add_to_maven_depmap %{short_name} %{short_name} %{version} JPP %{short_name}

%pre javadoc
# workaround for rpm bug, can be removed in F-17
[ $1 -gt 1 ] && [ -L %{_javadocdir}/%{name} ] && \
rm -rf $(readlink -f %{_javadocdir}/%{name}) %{_javadocdir}/%{name} || :

%post
%update_maven_depmap

%postun
%update_maven_depmap

%files
%defattr(-,root,root,-)
%{_mavendepmapfragdir}/*
%{_mavenpomdir}/JPP-%{short_name}.pom
%doc LICENSE.txt
%{_javadir}/*.jar

%files javadoc
%defattr(-,root,root,-)
%doc LICENSE.txt
%doc %{_javadocdir}/%{name}



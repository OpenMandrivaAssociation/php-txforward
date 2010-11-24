%define modname txforward
%define soname %{modname}.so
%define inifile A90_%{modname}.ini

Summary:	Reverse Proxy (web accelerator) PHP compatibility layer
Name:		php-%{modname}
Version:	1.0.6
Release:	%mkrel 11
Group:		Development/PHP
License:	PHP License
URL:		http://fcartegnie.free.fr/patchs/txforward.html
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
Requires(pre): rpm-helper
Requires(postun): rpm-helper
BuildRequires:	php-devel >= 3:5.2.0
BuildRequires:	file
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
Makes reverse-proxing (web accelerator) totally invisible for php applications.
Doesn't require php code modifications to handle X-Forwarded-For IP.

 * Stills allows proxy-aware applications to work with X-Forwarded headers and
   proxy IP address.
 * Should work with any web server
 * Should work with any proxy server

%prep

%setup -q -n %{modname}-%{version}
[ "../package*.xml" != "/" ] && mv ../package*.xml .

# fix permissions
find . -type f | xargs chmod 644

# strip away annoying ^M
find . -type f|xargs file|grep 'CRLF'|cut -d: -f1|xargs perl -p -i -e 's/\r//'
find . -type f|xargs file|grep 'text'|cut -d: -f1|xargs perl -p -i -e 's/\r//'

# lib64 fix
perl -p -i -e "s|/lib\b|/%{_lib}|g" *.m4

%build
%serverbuild

phpize
%configure2_5x --with-libdir=%{_lib} \
    --enable-%{modname}

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/php.d
install -d %{buildroot}%{_libdir}/php/extensions

install -m0755 modules/%{soname} %{buildroot}%{_libdir}/php/extensions/

cat > %{buildroot}%{_sysconfdir}/php.d/%{inifile} << EOF
extension = %{soname}

[%{modname}]
txforward.depth = 4
EOF

%post
if [ -f /var/lock/subsys/httpd ]; then
    %{_initrddir}/httpd restart >/dev/null || :
fi

%postun
if [ "$1" = "0" ]; then
    if [ -f /var/lock/subsys/httpd ]; then
	%{_initrddir}/httpd restart >/dev/null || :
    fi
fi

%clean
rm -rf %{buildroot}

%files 
%defattr(-,root,root)
%doc package*.xml CREDITS README
%attr(0644,root,root) %config(noreplace) %{_sysconfdir}/php.d/%{inifile}
%attr(0755,root,root) %{_libdir}/php/extensions/%{soname}


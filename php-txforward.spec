%define modname txforward
%define soname %{modname}.so
%define inifile A90_%{modname}.ini

Summary:	Reverse Proxy (web accelerator) PHP compatibility layer
Name:		php-%{modname}
Version:	1.0.7
Release:	%mkrel 5
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



%changelog
* Thu May 03 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-5mdv2012.0
+ Revision: 795524
- rebuild for php-5.4.x

* Sun Jan 15 2012 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-4
+ Revision: 761339
- rebuild

* Wed Aug 24 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-3
+ Revision: 696484
- rebuilt for php-5.3.8

* Fri Aug 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-2
+ Revision: 695485
- rebuilt for php-5.3.7

* Tue May 17 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.7-1
+ Revision: 675368
- 1.0.7

* Sat Mar 19 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-14
+ Revision: 646698
- rebuilt for php-5.3.6

* Sat Jan 08 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-13mdv2011.0
+ Revision: 629895
- rebuilt for php-5.3.5

* Mon Jan 03 2011 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-12mdv2011.0
+ Revision: 628204
- ensure it's built without automake1.7

* Wed Nov 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-11mdv2011.0
+ Revision: 600544
- rebuild

* Sun Oct 24 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-10mdv2011.0
+ Revision: 588881
- rebuild

* Fri Mar 05 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-9mdv2010.1
+ Revision: 514708
- rebuilt for php-5.3.2

* Sat Jan 02 2010 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-8mdv2010.1
+ Revision: 485496
- rebuilt for php-5.3.2RC1

* Sat Nov 21 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-7mdv2010.1
+ Revision: 468267
- rebuilt against php-5.3.1

* Wed Sep 30 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-6mdv2010.0
+ Revision: 451369
- rebuild

  + Raphaël Gertz <rapsys@mandriva.org>
    - Rebuild

* Mon May 18 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-4mdv2010.0
+ Revision: 377038
- rebuilt for php-5.3.0RC2

* Sun Mar 01 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-3mdv2009.1
+ Revision: 346681
- rebuilt for php-5.2.9

* Tue Feb 17 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-2mdv2009.1
+ Revision: 341844
- rebuilt against php-5.2.9RC2

* Sun Jan 04 2009 Oden Eriksson <oeriksson@mandriva.com> 1.0.6-1mdv2009.1
+ Revision: 324499
- import php-txforward


* Sun Jan 04 2009 Oden Eriksson <oden.eriksson@envitory.se> 1.0.6-1mdv2009.1
- initial Mandriva package

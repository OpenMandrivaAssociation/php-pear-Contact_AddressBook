%define _provides_exceptions pear(data

%define		_class		Contact
%define		_subclass	AddressBook
%define		_status		devel
%define		_pearname	%{_class}_%{_subclass}

Summary:	%{_pearname} - Address book export-import class
Name:		php-pear-%{_pearname}
Version:	0.5.0
Release:	%mkrel 1
License:	PHP License
Group:		Development/PHP
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tar.bz2
URL:		http://pear.php.net/package/Contact_AddressBook/
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRequires:	dos2unix
BuildRoot:	%{_tmppath}/%{name}-%{version}-buildroot

%description
Package provides export-import address book mechanism.
Contact_AddressBook refers to needed structure, convert the various
address book structure format into it, then you can easily store it
into file, database or another storage media.

In PEAR status of this package is: %{_status}.

%prep

%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

# strip away annoying ^M
find -type f | grep -v ".gif" | grep -v ".png" | grep -v ".jpg" | xargs dos2unix -U

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/{Builder,Converter,Parser}

install %{_pearname}-%{version}/%{_class}/%{_subclass}.php %{buildroot}%{_datadir}/pear/%{_class}/
install %{_pearname}-%{version}/%{_class}/%{_subclass}/Builder/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Builder/
install %{_pearname}-%{version}/%{_class}/%{_subclass}/Converter/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Converter/
install %{_pearname}-%{version}/%{_class}/%{_subclass}/Parser/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}/Parser/
install %{_pearname}-%{version}/%{_class}/%{_subclass}/*.php %{buildroot}%{_datadir}/pear/%{_class}/%{_subclass}

install -d %{buildroot}%{_datadir}/pear/data/%{_class}_%{_subclass}
cp -rp %{_pearname}-%{version}/data %{buildroot}%{_datadir}/pear/data/%{_class}_%{_subclass}/

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%doc %{_pearname}-%{version}/{docs/examples,data}
%{_datadir}/pear/%{_class}/%{_subclass}.php
%{_datadir}/pear/%{_class}/%{_subclass}
%{_datadir}/pear/packages/%{_pearname}.xml
%{_datadir}/pear/data/%{_class}_%{_subclass}/data

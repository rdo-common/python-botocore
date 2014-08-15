%if 0%{?fedora} > 12
%bcond_without python3
%else
%bcond_with python3
%endif

Name:           python-botocore
Version:        0.58.0
Release:        2%{?dist}
Summary:        The low-level, core functionality of boto 3
Group:          System Environment/Libraries

License:        ASL 2.0
URL:            https://github.com/boto/botocore
Source0:        https://pypi.python.org/packages/source/b/botocore/botocore-%{version}.tar.gz
Patch0:         0001-botocore-Add-some-version-requirements.patch
Patch1:         0001-Do-not-use-bundled-requests.patch

BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
BuildRequires:  python-six >= 1.1.0
BuildRequires:  python-jmespath >= 0.4.1
BuildRequires:  python-dateutil >= 1.5
%if %with python3
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-six >= 1.1.0
BuildRequires:  python3-jmespath >= 0.4.1
BuildRequires:  python3-dateutil >= 1.5
%endif

Requires:       python-six >= 1.1.0
Requires:       python-jmespath >= 0.4.1
Requires:       python-dateutil >= 1.5
Requires:       python-requests
Requires:       python-urllib3

%description
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for AWS-CLI.

This package contains the library for Python 2.

%package -n python3-botocore
Summary:        The low-level, core functionality of boto 3
Group:          System Environment/Libraries

Requires:       python3-six >= 1.1.0
Requires:       python3-jmespath >= 0.4.1
Requires:       python3-dateutil >= 1.5
Requires:       python3-requests
Requires:       python3-urllib3

%description -n python3-botocore
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for AWS-CLI.

This package contains the library for Python 3.


%prep
%setup -q -n botocore-%{version}
%patch0 -p1
%patch1 -p1

%if %with python3
rm -rf %{py3dir}
cp -a . %{py3dir}
%endif


%build
%if %with python3
pushd %{py3dir}
%{__python3} setup.py build
popd
%endif

%{__python2} setup.py build



%install
%if %with python3
pushd %{py3dir}
%{__python3} setup.py install --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python3_sitelib}/botocore/vendored
popd
%endif

%{__python2} setup.py install -O1 --skip-build --root %{buildroot}
rm -rf %{buildroot}%{python2_sitelib}/botocore/vendored

 
%check
%if %with python3
pushd %{py3dir}
%{__python3} setup.py test
popd
%endif

%{__python2} setup.py test


%files
%{python2_sitelib}/*
%doc README.rst
%doc LICENSE.txt


%if %with python3
%files -n python3-botocore
%{python3_sitelib}/*
%doc README.rst
%doc LICENSE.txt
%endif


%changelog
* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-1
- Initial packaging

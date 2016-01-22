%if 0%{?rhel}
%global with_python3 0
%{!?__python2: %global __python2 /usr/bin/python2}
%{!?python2_sitelib: %global python2_sitelib %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib())")}
%{!?python2_sitearch: %global python2_sitearch %(%{__python2} -c "from distutils.sysconfig import get_python_lib; print(get_python_lib(1))")}
%{!?py2_build: %global py2_build %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} build --executable="%{__python2} -s"}}
%{!?py2_install: %global py2_install %{expand: CFLAGS="%{optflags}" %{__python2} setup.py %{?py_setup_args} install -O1 --skip-build --root %{buildroot}}}
%else
%global with_python3 1
%endif

%global pypi_name botocore

# Enable tests
%global with_tests 1
# Disable documentation generation for now
%global with_docs 0

# Something breaks for now
%if 0%{?fedora} != 23
%global with_tests 0
%endif

# Tests not yet ready for EL
%{?rhel: %global with_tests 0}

Name:           python-%{pypi_name}
Version:        1.3.22
Release:        1%{?dist}
Summary:        Low-level, data-driven core of boto 3

License:        ASL 2.0
URL:            https://github.com/boto/botocore
Source0:        https://pypi.python.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildRequires:  python-setuptools
%if 0%{?with_docs}
BuildRequires:  python-sphinx
BuildRequires:  python-guzzle_sphinx_theme
%endif # with_docs
%if 0%{?with_tests}
BuildRequires:  mock
BuildRequires:  python-tox
BuildRequires:  python-behave
BuildRequires:  python-nose
BuildRequires:  python-wheel
BuildRequires:  python-docutils
BuildRequires:  python-dateutil
BuildRequires:  python2-jmespath
%endif # with_tests
%if 0%{?with_python3}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
%if 0%{?with_docs}
BuildRequires:  python3-sphinx
BuildRequires:  python3-guzzle_sphinx_theme
%endif # with_docs
%if 0%{?with_tests}
%{?fc24:BuildRequires: python3-behave}
BuildRequires:  python3-nose
BuildRequires:  python3-wheel
BuildRequires:  python3-tox
BuildRequires:  python3-docutils
BuildRequires:  python3-dateutil
BuildRequires:  python3-jmespath
%endif # with_tests
%endif # with_python3

%description
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.

%package -n     python2-%{pypi_name}
Summary:        Low-level, data-driven core of boto 3
Requires:       python-jmespath
Requires:       python-dateutil
Requires:       python-docutils
Requires:       python-requests
%{?el6:Provides: python-%{pypi_name}}
%{?python_provide:%python_provide python2-%{pypi_name}}

%description -n python2-%{pypi_name}
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        Low-level, data-driven core of boto 3
Requires:       python3-jmespath
Requires:       python3-dateutil
Requires:       python3-docutils
Requires:       python3-requests
%{?python_provide:%python_provide python3-%{pypi_name}}

%description -n python3-%{pypi_name}
A low-level interface to a growing number of Amazon Web Services. The
botocore package is the foundation for the AWS CLI as well as boto3.
%endif # with_python3

%if 0%{?with_docs}
%package -n python-%{pypi_name}-doc
Summary:        botocore documentation
%description -n python-%{pypi_name}-doc
Documentation for botocore
%endif # with_docs

%prep
%setup -q -n %{pypi_name}-%{version}
sed -i -e '1 d' botocore/vendored/requests/packages/chardet/chardetect.py
sed -i -e '1 d' botocore/vendored/requests/certs.py
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%if 0%{?with_python3}
%py3_build
%endif # with_python3

%install
%if 0%{?with_python3}
%py3_install
%endif # with_python3
%py2_install
%if 0%{?with_docs}
%if 0%{?with_python3}
sphinx-build-3 docs/source html
rm -rf html/.{doctrees,buildinfo}
%else # with_python3
sphinx-build docs/source html
rm -rf html/.{doctrees,buildinfo}
%endif # with_python3
%endif # with_docs

%if 0%{?with_tests}
%check
%{__python2} setup.py test
%if 0%{?with_python3}
%{__python3} setup.py test
%endif # with_python3
%endif # with_tests

%files -n python2-%{pypi_name}
%{!?_licensedir:%global license %doc}
%doc README.rst
%license LICENSE.txt
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%doc README.rst
%license LICENSE.txt
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info
%endif # with_python3

%if 0%{?with_docs}
%files -n python-%{pypi_name}-doc
%doc html
%endif # with_docs

%changelog
* Fri Jan 22 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.22-1
- New version from upstream

* Wed Jan 20 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.21-1
- New version from upstream

* Fri Jan 15 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.20-1
- New version from upstream

* Fri Jan 15 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.19-1
- New version from upstream

* Wed Jan 13 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.18-1
- New version from upstream

* Tue Jan 12 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.17-2
- Add testing for Fedora

* Thu Jan 07 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.17-1
- Update to upstream version

* Wed Jan 06 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.16-2
- Fix shabang on botocore/vendored/requests/packages/chardet/chardetect.py
- Fix shabang on botocore/vendored/requests/certs.py
- Remove the useless dependency with python-urllib3

* Wed Jan 06 2016 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.16-1
- Update to new upstream version
- Fix Provides for EL6

* Tue Dec 29 2015 Fabio Alessandro Locati <fabio@locati.cc> - 1.3.15-1
- Update to current version
- Improve the spec

* Tue Nov 10 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79.0-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.79.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Fri Dec 19 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.79.0-1
- New version

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-2
- Add Python 3 support

* Fri Jul 25 2014 Lubomir Rintel <lkundrak@v3.sk> - 0.58.0-1
- Initial packaging

%global __python3 /usr/bin/python3.11
%global python3_pkgversion 3.11

%global pypi_name pluggy

# Turn the tests off when bootstrapping Python, because pytest requires pluggy
%bcond_without tests

Name:           python%{python3_pkgversion}-pluggy
Version:        1.0.0
Release:        2%{?dist}
Summary:        The plugin manager stripped of pytest specific details

License:        MIT
URL:            https://github.com/pytest-dev/pluggy
Source0:        %{pypi_source}


BuildArch:      noarch

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-rpm-macros
BuildRequires:  python%{python3_pkgversion}-setuptools
%if %{with tests}
BuildRequires:  python%{python3_pkgversion}-pytest
%endif

%description
The plugin manager stripped of pytest specific details.


%prep
%autosetup -p1 -n %{pypi_name}-%{version}

# remove setuptools_scm dependency since we don't have it in RHEL
sed -i '/setuptools-scm/d' pyproject.toml
sed -i '/setup_requires =/d' setup.cfg
sed -i '/setuptools-scm/d' setup.cfg

# since setuptools_scm is not available we need to sed out it's usage from setup.py and set the correct version
sed -i 's/use_scm_version={"write_to": "src\/pluggy\/_version.py"}/version="%{version}"/g' setup.py


%build
%py3_build


%install
%py3_install

%check
%if %{with tests}
# TODO investigate test_load_setuptools_instantiation failure
PYTHONPATH=%{buildroot}%{python3_sitelib} %{__python3} -m pytest testing -k "not test_load_setuptools_instantiation"
%endif
export PYTHONPATH=%{buildroot}%{python3_sitelib}
test "$(%{python3} -c 'import pluggy; print(pluggy.__version__)')" == "%{version}"


%files
%{python3_sitelib}/%{pypi_name}/
%{python3_sitelib}/%{pypi_name}-%{version}-py%{python3_version}.egg-info/
%doc README.rst
%license LICENSE


%changelog
* Wed Feb 01 2023 Charalampos Stratakis <cstratak@redhat.com> - 1.0.0-2
- Enable tests

* Wed Oct 19 2022 Charalampos Stratakis <cstratak@redhat.com> - 1.0.0-1
- Initial package
- Fedora contributions by:
      Alfredo Moralejo <amoralej@redhat.com>
      Karsten Hopp <karsten@redhat.com>
      Matthias Runge <mrunge@redhat.com>
      Miro Hrončok <miro@hroncok.cz>
      Patrik Kopkan <pkopkan@redhat.com>
      Peter Robinson <pbrobinson@fedoraproject.org>
      Thomas Moschny <thm@fedoraproject.org>
      Tomáš Hrnčiar <thrnciar@redhat.com>
      Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl>

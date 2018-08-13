Name:           plexil
Version:        4.5.0
Release:        0.3%{?dist}
Summary:        A programming language for representing plans for automation

License:        BSD
URL:            http://plexil.sourceforge.net/
# Upstream releases are very old, use svn snapshot instead.
# According to the Versions file, this is a pre-release of 4.5.0.
# Created with:
# svn export https://svn.code.sf.net/p/plexil/code/branches/plexil-4 plexil-%%{version}
# tar czf plexil-%%{version}.tar.gz plexil-%%{version}
Source0:        %{name}-%{version}.tar.gz
Patch0:         %{name}.remove-pugixml.patch

BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pugixml-devel

%description
PLEXIL (Plan Execution Interchange Language) is a language for representing
plans for automation, as well a technology for executing these plans on real or
simulated systems. PLEXIL has been used in robotics, control of unmanned
vehicles, automation of operations in human habitats, and systems and
simulations involving intelligent software agents.


%package        devel
Summary:        Development files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    devel
The %{name}-devel package contains libraries and header files for
developing applications that use %{name}.


%package        test
Summary:        Test files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    test
The %{name}-test package contains binaries to test the functionality of %{name}.



%prep
%autosetup -p1


%build
pushd src
autoreconf --install
%configure \
  --disable-static \
  --includedir=%{_includedir}/plexil \
  --enable-gantt \
  --enable-module-tests \
  --enable-test-exec \
  --enable-udp \

  #--enable-sas
  #--enable-ipc

%make_build


%install
pushd src
%make_install

# Remove static libraries and libtool files
find %{buildroot} -name "*.a" -o -name "*.la" -delete

# Add plexil- prefix to all binaries
pushd %{buildroot}/%{_bindir}
for file in * ; do
  mv $file plexil-$file
done
popd

# Move plugins and internally used libs into a plexil sub-directory
pushd %{buildroot}/%{_libdir}
mkdir -p plexil
mv libGanttListener* libLauncher* libLuvListener* libPlanDebugListener* libUdpAdapter* libUdpUtils* \
  plexil/
popd


%files
%license LICENSE
%doc README
%doc CAVEATS
%doc Versions
%{_bindir}/plexil-analyzePlan
%{_bindir}/plexil-benchmark
%{_bindir}/plexil-universalExec
%{_libdir}/*.so.*
%{_libdir}/plexil

%files devel
%{_includedir}/plexil
%{_libdir}/*.so

%files test
%{_bindir}/plexil-TestExec
%{_bindir}/plexil-exec-module-tests
%{_bindir}/plexil-expr-module-tests
%{_bindir}/plexil-intfc-module-tests
%{_bindir}/plexil-parser-module-tests
%{_bindir}/plexil-utils-module-tests
%{_bindir}/plexil-value-module-tests



%changelog
* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.3
- Move plugins into a plexil sub-directory

* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.2
- Add patch to use external pugixml instead of thirdparty copylib

* Thu Aug  9 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.1
-  initial package

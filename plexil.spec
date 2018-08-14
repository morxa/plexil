Name:           plexil
Version:        4.5.0
Release:        0.7%{?dist}
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
Patch1:         %{name}.script-paths.patch

BuildRequires:  automake
BuildRequires:  gcc-c++
BuildRequires:  libtool
BuildRequires:  pugixml-devel

# Viewer
BuildRequires:  ant
BuildRequires:  java-1.8.0-openjdk-devel

# Compiler
BuildRequires:  antlr3-java
BuildRequires:  antlr3-tool
BuildRequires:  ant-antlr
BuildRequires:  nanoxml
BuildRequires:  saxon

Requires:       /usr/bin/netstat
Requires:       /usr/bin/xmllint

Recommends:     %{name}-compiler

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


%package        viewer
Summary:        A viewer for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch
Requires:       java
Requires:       javapackages-filesystem

%description    viewer
The %{name}-viewer package contains a viewer for %{name}.


%package        compiler
Summary:        A compiler for the %{name} language
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch
Requires:       java-headless
Requires:       javapackages-filesystem
Requires:       nanoxml
Requires:       /usr/bin/xmllint
Recommends:     %{name}-lisp

%description    compiler
The %{name}-compiler package contains a compiler for the %{name} language.


%package        lisp
Summary:        A lisp parser for the %{name} language
Requires:       %{name}%{?_isa} = %{version}-%{release}
BuildArch:      noarch
Requires:       /usr/bin/emacs
Requires:       /usr/bin/perl

%description    lisp
The %{name}-lisp package contains a compiler for the %{name} language.


%package        test
Summary:        Test files for %{name}
Requires:       %{name}%{?_isa} = %{version}-%{release}

%description    test
The %{name}-test package contains binaries to test the functionality of %{name}.


%prep
%autosetup -p1

find jars -name "*.jar" -delete


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

popd

%make_build checker plexilscript pv

pushd compilers/plexil
%make_build -j1 ANTLR="%{_bindir}/antlr3" ANTLR3_TOOL_JAR=%{_javadir}/antlr3-runtime.jar 2>&1 SAXON_JAR=%{_javadir}/saxon/saxon.jar
popd



%install
pushd src
%make_install
popd

# sh profile
%__install -p -D scripts/plexil.profile.sh %{buildroot}/%{_sysconfdir}/profile.d/plexil.sh


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

%__install -p -D -t %{buildroot}/%{_datarootdir}/%{name}/examples examples/empty.psx
pushd scripts
%__install -p -D -t %{buildroot}/%{_bindir} summarize-plexil plexiltest
%__install -p -D -t %{buildroot}/%{_datarootdir}/%{name}/scripts list_ports_in_use plexil-check-prog checkPlexil
popd

# viewer
pushd viewers/pv
%__install -p -D luv.jar %{buildroot}/%{_javadir}/%{name}-viewer.jar
popd

# compiler
%__install -p -D -t %{buildroot}/%{_javadir} jars/PlexilCompiler.jar jars/plexilscript.jar
%__install -p -D -t %{buildroot}/%{_javadir}/%{name} checker/global-decl-checker.jar
%__install -p -D -t %{buildroot}/%{_bindir} compilers/plexil/PlexilCompiler compilers/plexil/PlexilCompilerDebug
%__install -p -D -t %{buildroot}/%{_datarootdir}/%{name}/schema schema/*.{rnc,rng,xsd,xsl}
pushd scripts
%__install -p -D -t %{buildroot}/%{_datarootdir}/%{name}/scripts checkDecls eplexil
%__install -p -D -t %{buildroot}/%{_bindir} plexilc
popd

# plexilisp
%__install -p -D -t %{buildroot}/%{_bindir} scripts/plexilisp
pushd compilers/plexilisp
%__install -p -D -t %{buildroot}/%{_datarootdir}/%{name}/plexilisp *.el xmlformat.*
popd


%files
%license LICENSE
%doc README
%doc CAVEATS
%doc Versions
%{_bindir}/plexil-analyzePlan
%{_bindir}/plexil-benchmark
%{_bindir}/plexil-universalExec
%{_bindir}/plexiltest
%{_bindir}/summarize-plexil
%{_libdir}/*.so.*
%{_libdir}/plexil
%{_sysconfdir}/profile.d/%{name}.sh
%dir %{_datarootdir}/%{name}
%dir %{_datarootdir}/%{name}/scripts
%{_datarootdir}/%{name}/examples/empty.psx
%{_datarootdir}/%{name}/scripts/list_ports_in_use
%{_datarootdir}/%{name}/scripts/plexil-check-prog
%{_datarootdir}/%{name}/scripts/checkPlexil

%files devel
%{_includedir}/plexil
%{_libdir}/*.so

%files viewer
%{_javadir}/%{name}-viewer.jar

%files compiler
%{_javadir}/PlexilCompiler.jar
%{_javadir}/plexilscript.jar
%{_javadir}/%{name}
%{_datarootdir}/%{name}/schema
%{_datarootdir}/%{name}/scripts/checkDecls
%{_datarootdir}/%{name}/scripts/eplexil
%{_bindir}/PlexilCompiler
%{_bindir}/PlexilCompilerDebug
%{_bindir}/plexilc

%files lisp
%license compilers/plexilisp/xmlformat-license.txt
%doc compilers/plexilisp/README
%doc compilers/plexilisp/examples
%{_bindir}/plexilisp
%{_datarootdir}/%{name}/plexilisp


%files test
%{_bindir}/plexil-TestExec
%{_bindir}/plexil-exec-module-tests
%{_bindir}/plexil-expr-module-tests
%{_bindir}/plexil-intfc-module-tests
%{_bindir}/plexil-parser-module-tests
%{_bindir}/plexil-utils-module-tests
%{_bindir}/plexil-value-module-tests



%changelog
* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.7
- Debundle nanoxml

* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.6
- Add plexilisp as lisp sub-package

* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.5
- Add compiler sub-package

* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.4
- Also build and install the viewer

* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.3
- Move plugins into a plexil sub-directory

* Mon Aug 13 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.2
- Add patch to use external pugixml instead of thirdparty copylib

* Thu Aug  9 2018 Till Hofmann <thofmann@fedoraproject.org> - 4.5.0-0.1
-  initial package

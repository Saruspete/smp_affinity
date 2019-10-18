Name:       smp_affinity
Version:    1.4.0
Release:    1%{?dist}
Summary:    List and configure CPU affinity of process and interrupts

Group:      Application/System
License:    GPL-3
BuildArch:  noarch
URL:        https://github.com/saruspete/smp_affinity
Source0:    https://github.com/saruspete/%{name}/archive/%{version}.tar.gz

#BuildRequires:
Requires:   /usr/bin/perl
#Requires:   perl-Math-BigInt

%define     debug_package %{nil}

# You can try to push files in /usr/local or /opt
%define     _prefix  /


# =============================================================================
# Complete description of the package
# =============================================================================
%description
Display and configure affinity of processes and IRQs

# =============================================================================
# Preparation of the build environment
# =============================================================================
%prep

%setup -q

# =============================================================================
# Compilation of the source
# =============================================================================
%build


# =============================================================================
# Installation from build to buildroot
# =============================================================================
%install

rm -rf "${RPM_BUILD_ROOT}"
mkdir -p "${RPM_BUILD_ROOT}%{?prefix}/usr/bin"
cp smp_affinity "${RPM_BUILD_ROOT}%{?prefix}/usr/bin"

ls -al


# =============================================================================
# Cleanup of the build environment
# =============================================================================
#%clean


# =============================================================================
# Files to be embedded in final RPM
# =============================================================================
%files
%defattr(-,root,root)

# Standard files
%{?prefix}/usr/bin/smp_affinity

# =============================================================================
# Actions before installation / upgrade
# =============================================================================
%pre

# =============================================================================
# Actions after installation / upgrade
# =============================================================================
%post

# =============================================================================
# Actions before removal
# =============================================================================
%preun

# =============================================================================
# Actions after removal
# =============================================================================
%postun

# =============================================================================
# Changelog
# =============================================================================
%changelog


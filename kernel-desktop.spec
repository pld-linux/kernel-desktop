#
# Conditional build:
%bcond_without	smp		# don't build SMP kernel
%bcond_without	up		# don't build UP kernel
%bcond_without	source		# don't build kernel-source package

%bcond_with	preemptrt	# use realtime-preempt patch
%bcond_without	ck		# don't use Con Kolivas patchset
%bcond_without	grsec_minimal	# don't build grsecurity (minimal subset: proc,link,fifo,shm)
%bcond_with	bootsplash	# build with bootsplash instead of fbsplash
%bcond_with	laptop		# build with HZ=100
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	pae		# build PAE (HIGHMEM64G) support on uniprocessor

%{?debug:%define with_verbose 1}

%ifarch %{ix86} ppc
%define		have_isa	1
%else
%define		have_isa	0
%endif

## Program required by kernel to work.
%define		_binutils_ver		2.12.1
%define		_util_linux_ver		2.10o
%define		_module_init_tool_ver	0.9.10
%define		_e2fsprogs_ver		1.29
%define		_jfsutils_ver		1.1.3
%define		_reiserfsprogs_ver	3.6.3
%define		_reiser4progs_ver	1.0.0
%define		_xfsprogs_ver		2.6.0
%define		_pcmcia_cs_ver		3.1.21
%define		_pcmciautils_ver	004
%define		_quota_tools_ver	3.09
%define		_ppp_ver		1:2.4.0
%define		_isdn4k_utils_ver	3.1pre1
%define		_nfs_utils_ver		1.0.5
%define		_procps_ver		3.2.0
%define		_oprofile_ver		0.9
%define		_udev_ver		071


%define		_netfilter_snap		20060504
%define		_nf_hipac_ver		0.9.1

%define		_enable_debug_packages			0
%define		no_install_post_strip			1
%define		no_install_post_chrpath			1

%define		pcmcia_version		3.1.22
%define		drm_xfree_version	4.3.0

%define		squashfs_version	3.0
%define		suspend_version		2.2.8.2

%define		xen_version		3.0.2

%if %{with laptop}
%define		alt_kernel	laptop
%else
%define		alt_kernel	desktop
%endif

Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(fr):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl):	J�dro Linuksa
Name:		kernel-%{alt_kernel}
%define		_basever	2.6.18
%define		_postver	.2
%define		_rel		0.1
Version:	%{_basever}%{_postver}
Release:	%{_rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
%define		_rc	%{nil}
#define		_rc	-rc6
#Source0:	ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing/linux-%{_basever}%{_rc}.tar.bz2
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{_basever}.tar.bz2
# Source0-md5:	296a6d150d260144639c3664d127d174
%if "%{_postver}" != "%{nil}"
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	70c23255c697aa18a6e6ce97dc4eeb9b
%endif
Source2:	http://www.suspend2.net/downloads/all/suspend2-%{suspend_version}-for-%{_basever}.patch.bz2
# Source2-md5:	b74c386616b33d5be2e39ad727490e5c

Source3:	kernel-desktop-autoconf.h
Source4:	kernel-desktop-config.h
Source5:	kernel-desktop-module-build.pl

Source20:	kernel-desktop-common.config
Source21:	kernel-desktop-i386.config
Source22:	kernel-desktop-i386-smp.config
Source23:	kernel-desktop-x86_64.config
Source24:	kernel-desktop-x86_64-smp.config
Source25:	kernel-desktop-ppc.config
Source26:	kernel-desktop-ppc-smp.config

Source41:	kernel-desktop-preempt-rt.config
Source42:	kernel-desktop-preempt-nort.config
Source43:	kernel-desktop-suspend2.config
Source44:	kernel-desktop-patches.config
Source45:	kernel-desktop-netfilter.config
Source46:	kernel-desktop-grsec.config

###
#	Patches
###

Patch0:		kernel-desktop-preempt-rt.patch

Patch3:		kernel-desktop-suspend2.patch

# Con Kolivas patchset
Patch6:		kernel-desktop-fcache.patch
Patch7:		kernel-desktop-ck.patch
Patch8:		kernel-desktop-nock-compat.patch

Patch9:		kernel-desktop-grsec-minimal.patch

# filesystems
Patch10:	kernel-desktop-reiser4.patch
Patch11:	kernel-desktop-squashfs.patch

# hardware
Patch20:	kernel-desktop-tahoe9xx.patch
Patch21:	kernel-desktop-sk98lin.patch
Patch22:	kernel-desktop-vesafb-tng.patch
Patch23:	kernel-desktop-dmi-decode-and-save-oem-string-information.patch

# console
Patch30:	kernel-desktop-bootsplash.patch
Patch31:	kernel-desktop-fbsplash.patch

########	netfilter snap
## base
Patch40:	kernel-desktop-pom-ng-IPV4OPTSSTRIP.patch
Patch41:	kernel-desktop-pom-ng-connlimit.patch
Patch42:	kernel-desktop-pom-ng-expire.patch
Patch43:	kernel-desktop-pom-ng-fuzzy.patch
Patch44:	kernel-desktop-pom-ng-ipv4options.patch
Patch45:	kernel-desktop-pom-ng-nth.patch
Patch46:	kernel-desktop-pom-ng-osf.patch
Patch47:	kernel-desktop-pom-ng-psd.patch
Patch48:	kernel-desktop-pom-ng-quota.patch
Patch49:	kernel-desktop-pom-ng-random.patch
Patch50:	kernel-desktop-pom-ng-set.patch
Patch51:	kernel-desktop-pom-ng-time.patch
Patch52:	kernel-desktop-pom-ng-u32.patch

## extra
Patch60:	kernel-desktop-pom-ng-ACCOUNT.patch
Patch61:	kernel-desktop-pom-ng-IPMARK.patch
Patch62:	kernel-desktop-pom-ng-ROUTE.patch
Patch63:	kernel-desktop-pom-ng-TARPIT.patch
Patch64:	kernel-desktop-pom-ng-account.patch
Patch65:	kernel-desktop-pom-ng-ipp2p.patch
Patch66:	kernel-desktop-pom-ng-rpc.patch
########	End netfilter

# net software
Patch70:	kernel-desktop-imq2.patch
Patch71:	kernel-desktop-esfq.patch
Patch72:	kernel-desktop-atm-vbr.patch
Patch73:	kernel-desktop-atmdd.patch

# ?
Patch85:	kernel-desktop-cpuset_virtualization.patch

# fixes
Patch90:	kernel-desktop-sco-mtu.patch
Patch91:	kernel-desktop-fbcon-margins.patch
Patch92:	kernel-desktop-static-dev.patch
Patch100:	kernel-desktop-small_fixes.patch

URL:		http://www.kernel.org/
BuildRequires:	binutils >= 3:2.14.90.0.7
BuildRequires:	diffutils
BuildRequires:	gcc >= 5:3.2
BuildRequires:	module-init-tools
# for hostname command
BuildRequires:	net-tools
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.217
Autoreqprov:	no
Requires:	coreutils
Requires:	geninitrd >= 2.57
Requires:	module-init-tools >= 0.9.9
Provides:	%{name}-up = %{epoch}:%{version}-%{release}
Provides:	kernel = %{epoch}:%{version}-%{release}
Provides:	kernel(netfilter) = %{_netfilter_snap}
Provides:	kernel(realtime-lsm) = 0.1.1
Provides:	kernel-misc-fuse
Provides:	kernel-net-hostap = 0.4.4
Provides:	kernel-net-ieee80211
Provides:	kernel-net-ipp2p = 1:0.8.0
Provides:	kernel-net-ipw2100 = 1.1.3
Provides:	kernel-net-ipw2200 = 1.0.8
Provides:	module-info
Conflicts:	e2fsprogs < %{_e2fsprogs_ver}
Conflicts:	isdn4k-utils < %{_isdn4k_utils_ver}
Conflicts:	jfsutils < %{_jfsutils_ver}
Conflicts:	module-init-tool < %{_module_init_tool_ver}
Conflicts:	nfs-utils < %{_nfs_utils_ver}
Conflicts:	oprofile < %{_oprofile_ver}
Conflicts:	ppp < %{_ppp_ver}
Conflicts:	procps < %{_procps_ver}
Conflicts:	quota-tools < %{_quota_tools_ver}
Conflicts:	reiser4progs < %{_reiser4progs_ver}
Conflicts:	reiserfsprogs < %{_reiserfsprogs_ver}
Conflicts:	udev < %{_udev_ver}
Conflicts:	util-linux < %{_util_linux_ver}
Conflicts:	xfsprogs < %{_xfsprogs_ver}
ExclusiveArch:	%{ix86} %{x8664} ppc
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		initrd_dir	/boot

%define		ver		%{version}_%{alt_kernel}
%define		ver_rel		%{version}_%{alt_kernel}-%{release}

%define	CommonOpts	HOSTCC="%{__cc}" HOSTCFLAGS="-Wall -Wstrict-prototypes %{rpmcflags} -fomit-frame-pointer"
%if "%{_target_base_arch}" != "%{_arch}"
	%define	MakeOpts %{CommonOpts} ARCH=%{_target_base_arch} CROSS_COMPILE=%{_target_cpu}-pld-linux-
	%define	DepMod /bin/true

	%if "%{_arch}" == "x86_64" && "%{_target_base_arch}" == "i386"
	%define	MakeOpts %{CommonOpts} CC="%{__cc}" ARCH=%{_target_base_arch}
	%define	DepMod /sbin/depmod
	%endif

%else
	%define MakeOpts %{CommonOpts} CC="%{__cc}"
	%define	DepMod /sbin/depmod
%endif

%description
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

%description -l de
Das Kernel-Packet enth�lt den Linux-Kernel (vmlinuz), den Kern des
Linux-Betriebssystems. Der Kernel ist f�r grundliegende
Systemfunktionen verantwortlich: Speicherreservierung,
Proze�-Management, Ger�te Ein- und Ausgaben, usw.

%description -l fr
Le package kernel contient le kernel linux (vmlinuz), la partie
centrale d'un syst�me d'exploitation Linux. Le noyau traite les
fonctions basiques d'un syst�me d'exploitation: allocation m�moire,
allocation de process, entr�e/sortie de peripheriques, etc.

%description -l pl
Pakiet zawiera j�dro Linuksa niezb�dne do prawid�owego dzia�ania
Twojego komputera. Zawiera w sobie sterowniki do sprz�tu znajduj�cego
si� w komputerze, takiego jak sterowniki dysk�w itp.

%package vmlinux
Summary:	vmlinux - uncompressed kernel image
Summary(de):	vmlinux - dekompressiertes Kernel Bild
Summary(pl):	vmlinux - rozpakowany obraz j�dra
Group:		Base/Kernel

%description vmlinux
vmlinux - uncompressed kernel image.

%description vmlinux -l de
vmlinux - dekompressiertes Kernel Bild.

%description vmlinux -l pl
vmlinux - rozpakowany obraz j�dra.

%package drm
Summary:	DRM kernel modules
Summary(de):	DRM Kernel Treiber
Summary(pl):	Sterowniki DRM
Group:		Base/Kernel
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
Provides:	kernel-drm = %{drm_xfree_version}
Autoreqprov:	no

%description drm
DRM kernel modules (%{drm_xfree_version}).

%description drm -l de
DRM Kernel Treiber (%{drm_xfree_version}).

%description drm -l pl
Sterowniki DRM (%{drm_xfree_version}).

%package pcmcia
Summary:	PCMCIA modules
Summary(de):	PCMCIA Module
Summary(pl):	Modu�y PCMCIA
Group:		Base/Kernel
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
Provides:	kernel(pcmcia)
Provides:	kernel-pcmcia = %{pcmcia_version}
Conflicts:	pcmcia-cs < %{_pcmcia_cs_ver}
Conflicts:	pcmciautils < %{_pcmciautils_ver}
Autoreqprov:	no

%description pcmcia
PCMCIA modules (%{pcmcia_version}).

%description pcmcia -l de
PCMCIA Module (%{pcmcia_version})

%description pcmcia -l pl
Modu�y PCMCIA (%{pcmcia_version}).

%package sound-alsa
Summary:	ALSA kernel modules
Summary(de):	ALSA Kernel Module
Summary(pl):	Sterowniki d�wi�ku ALSA
Group:		Base/Kernel
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-alsa
ALSA (Advanced Linux Sound Architecture) sound drivers.

%description sound-alsa -l de
ALSA (Advanced Linux Sound Architecture) Sound-Treiber.

%description sound-alsa -l pl
Sterowniki d�wi�ku ALSA (Advanced Linux Sound Architecture).

%package sound-oss
Summary:	OSS kernel modules
Summary(de):	OSS Kernel Module
Summary(pl):	Sterowniki d�wi�ku OSS
Group:		Base/Kernel
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-oss
OSS (Open Sound System) drivers.

%description sound-oss -l de
OSS (Open Sound System) Treiber.

%description sound-oss -l pl
Sterowniki d�wi�ku OSS (Open Sound System).

%package smp
Summary:	Kernel version %{version} compiled for SMP machines
Summary(de):	Kernel Version %{version} f�r Multiprozessor-Maschinen
Summary(fr):	Kernel version %{version} compiler pour les machine Multi-Processeur
Summary(pl):	J�dro Linuksa w wersji %{version} dla maszyn wieloprocesorowych
Group:		Base/Kernel
Requires:	coreutils
Requires:	geninitrd >= 2.26
Requires:	module-init-tools >= 0.9.9
Provides:	kernel = %{epoch}:%{version}-%{release}
Provides:	kernel(netfilter) = %{_netfilter_snap}
Provides:	kernel(realtime-lsm) = 0.1.1
Provides:	kernel-smp-misc-fuse
Provides:	kernel-smp-net-hostap = 0.4.4
Provides:	kernel-smp-net-ieee80211
Provides:	kernel-smp-net-ipp2p = 1:0.8.0
Provides:	kernel-smp-net-ipw2100 = 1.1.3
Provides:	kernel-smp-net-ipw2200 = 1.0.8
Provides:	module-info
Conflicts:	e2fsprogs < %{_e2fsprogs_ver}
Conflicts:	isdn4k-utils < %{_isdn4k_utils_ver}
Conflicts:	jfsutils < %{_jfsutils_ver}
Conflicts:	module-init-tool < %{_module_init_tool_ver}
Conflicts:	nfs-utils < %{_nfs_utils_ver}
Conflicts:	oprofile < %{_oprofile_ver}
Conflicts:	ppp < %{_ppp_ver}
Conflicts:	procps < %{_procps_ver}
Conflicts:	quota-tools < %{_quota_tools_ver}
Conflicts:	reiser4progs < %{_reiser4progs_ver}
Conflicts:	reiserfsprogs < %{_reiserfsprogs_ver}
Conflicts:	util-linux < %{_util_linux_ver}
Conflicts:	xfsprogs < %{_xfsprogs_ver}
Autoreqprov:	no

%description smp
This package includes a SMP version of the Linux %{version} kernel. It
is required only on machines with two or more CPUs, although it should
work fine on single-CPU boxes.

%description smp -l de
Dieses Packet enth�lt eine SMP (Multiprozessor)-Version vom
Linux-Kernel %{version}. Es wird f�r Maschinen mit zwei oder mehr
Prozessoren gebraucht, sollte aber auch auf Komputern mit nur einer
CPU laufen.

%description smp -l fr
Ce package inclu une version SMP du noyau de Linux version {version}.
Il et n�cessaire seulement pour les machine avec deux processeurs ou
plus, il peut quand m�me fonctionner pour les syst�me mono-processeur.

%description smp -l pl
Pakiet zawiera j�dro SMP Linuksa w wersji %{version}. Jest ono
wymagane przez komputery zawieraj�ce dwa lub wi�cej procesor�w.
Powinno r�wnie� dobrze dzia�a� na maszynach z jednym procesorem.

%package smp-vmlinux
Summary:	vmlinux - uncompressed SMP kernel image
Summary(de):	vmlinux - dekompressiertes SMP Kernel Bild
Summary(pl):	vmlinux - rozpakowany obraz j�dra SMP
Group:		Base/Kernel

%description smp-vmlinux
vmlinux - uncompressed SMP kernel image.

%description smp-vmlinux -l de
vmlinux - dekompressiertes SMP Kernel Bild.

%description smp-vmlinux -l pl
vmlinux - rozpakowany obraz j�dra SMP.

%package smp-drm
Summary:	DRM SMP kernel modules
Summary(de):	DRM SMP Kernel Module
Summary(pl):	Sterowniki DRM dla maszyn wieloprocesorowych
Group:		Base/Kernel
Requires(postun):	%{name}-smp = %{epoch}:%{version}-%{release}
Requires:	%{name}-smp = %{epoch}:%{version}-%{release}
Provides:	kernel-drm = %{drm_xfree_version}
Autoreqprov:	no

%description smp-drm
DRM SMP kernel modules (%{drm_xfree_version}).

%description smp-drm -l de
DRM SMP Kernel Module (%{drm_xfree_version}).

%description smp-drm -l pl
Sterowniki DRM dla maszyn wieloprocesorowych (%{drm_xfree_version}).

%package smp-pcmcia
Summary:	PCMCIA modules for SMP kernel
Summary(de):	PCMCIA Module f�r SMP Kernel
Summary(pl):	Modu�y PCMCIA dla maszyn SMP
Group:		Base/Kernel
Requires(postun):	%{name}-smp = %{epoch}:%{version}-%{release}
Requires:	%{name}-smp = %{epoch}:%{version}-%{release}
Provides:	kernel(pcmcia)
Provides:	kernel-pcmcia = %{pcmcia_version}
Conflicts:	pcmcia-cs < %{_pcmcia_cs_ver}
Conflicts:	pcmciautils < %{_pcmciautils_ver}
Autoreqprov:	no

%description smp-pcmcia
PCMCIA modules for SMP kernel (%{pcmcia_version}).

%description smp-pcmcia -l de
PCMCIA Module f�r SMP Kernel (%{pcmcia_version}).

%description smp-pcmcia -l pl
Modu�y PCMCIA dla maszyn SMP (%{pcmcia_version}).

%package smp-sound-alsa
Summary:	ALSA SMP kernel modules
Summary(de):	ALSA SMP Kernel Module
Summary(pl):	Sterowniki d�wi�ku ALSA dla maszyn wieloprocesorowych
Group:		Base/Kernel
Requires(postun):	%{name}-smp = %{epoch}:%{version}-%{release}
Requires:	%{name}-smp = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description smp-sound-alsa
ALSA (Advanced Linux Sound Architecture) SMP sound drivers.

%description smp-sound-alsa -l de
ALSA (Advanced Linux Sound Architecture) SMP Sound-Treiber.

%description smp-sound-alsa -l pl
Sterowniki d�wi�ku ALSA (Advanced Linux Sound Architecture) dla maszyn
wieloprocesorowych.

%package smp-sound-oss
Summary:	OSS SMP kernel modules
Summary(de):	OSS SMP Kernel Module
Summary(pl):	Sterowniki d�wi�ku OSS dla maszyn wieloprocesorowych
Group:		Base/Kernel
Requires(postun):	%{name}-smp = %{epoch}:%{version}-%{release}
Requires:	%{name}-smp = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description smp-sound-oss
OSS (Open Sound System) SMP sound drivers.

%description smp-sound-oss -l de
OSS (Open Sound System) SMP Sound-Treiber.

%description smp-sound-oss -l pl
Sterowniki OSS (Open Sound System) dla maszyn wieloprocesorowych.

%package headers
Summary:	Header files for the Linux kernel
Summary(de):	Header Dateien f�r den Linux-Kernel
Summary(pl):	Pliki nag��wkowe j�dra Linuksa
Group:		Development/Building
Provides:	kernel-headers = %{epoch}:%{version}-%{release}
Provides:	kernel-headers(agpgart) = %{version}
Provides:	kernel-headers(alsa-drivers)
Provides:	kernel-headers(bridging) = %{version}
Provides:	kernel-headers(netfilter) = %{_netfilter_snap}
Provides:	kernel-headers(reiserfs) = %{version}
Autoreqprov:	no

%description headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description headers -l de
Dies sind die C Header Dateien f�r den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten die beim rekompilieren des Kernels
oder bei Kernel Modul kompilationen gebraucht werden.

%description headers -l pl
Pakiet zawiera pliki nag��wkowe j�dra, niezb�dne do rekompilacji j�dra
oraz budowania modu��w j�dra.

%package module-build
Summary:	Development files for building kernel modules
Summary(de):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl):	Pliki s�u��ce do budowania modu��w j�dra
Group:		Development/Building
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Provides:	kernel-module-build = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description module-build -l de
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description module-build -l pl
Pliki ze drzewa �r�de� j�dra potrzebne do budowania modu��w j�dra
Linuksa z zewn�trznych pakiet�w.

%package source
Summary:	Kernel source tree
Summary(de):	Der Kernel Quelltext
Summary(pl):	Kod �r�d�owy j�dra Linuksa
Group:		Development/Building
Requires:	%{name}-module-build = %{epoch}:%{version}-%{release}
Provides:	kernel-source = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description source
This is the source code for the Linux kernel. It is required to build
most C programs as they depend on constants defined in here. You can
also build a custom kernel that is better tuned to your particular
hardware.

%description source -l de
Das Kernel-Source-Packet enth�lt den source code (C/Assembler-Code) des
Linux-Kernels. Die Source-Dateien werden gebraucht, um viele
C-Programme zu kompilieren, da sie auf Konstanten zur�ckgreifen, die
im Kernel-Source definiert sind. Die Source-Dateien k�nnen auch
benutzt werden, um einen Kernel zu kompilieren, der besser auf Ihre
Hardware ausgerichtet ist.

%description source -l fr
Le package pour le kernel-source contient le code source pour le noyau
linux. Ces sources sont n�cessaires pour compiler la plupart des
programmes C, car il d�pend de constantes d�finies dans le code
source. Les sources peuvent �tre aussi utilis�e pour compiler un noyau
personnalis� pour avoir de meilleures performances sur des mat�riels
particuliers.

%description source -l pl
Pakiet zawiera kod �r�d�owy j�dra systemu.

%package doc
Summary:	Kernel documentation
Summary(de):	Kernel Dokumentation
Summary(pl):	Dokumentacja do j�dra Linuksa
Group:		Documentation
Provides:	kernel-doc = %{version}
Autoreqprov:	no

%description doc
This is the documentation for the Linux kernel, as found in
Documentation directory.

%description doc -l de
Dies ist die Kernel Dokumentation wie sie im 'Documentation' Verzeichniss
vorgefunden werden kann.

%description doc -l pl
Pakiet zawiera dokumentacj� do j�dra Linuksa pochodz�c� z katalogu
Documentation.

%prep
%setup -q -n linux-%{_basever}%{_rc}

%if "%{_postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | %{__patch} -p1 -s
%endif

# suspend 2
%{__bzip2} -dc %{SOURCE2} | %{__patch} -p1 -s

%if %{with preemptrt}
%patch0 -p1
%endif

# Con Kolivas patchset
%if %{with ck}
%if %{with preemptrt}
#%%patch6 -p1	NEEDS UPDATE
%else
%patch7 -p1
%endif
%else
#%%patch8 -p1	NEEDS UPDATE
%endif

# grsecurity
%if %{with grsec_minimal}
%patch9 -p1
%endif

# filesystems
#%%patch10 -p1	NEEDS UPDATE - fails to build
#%%patch11 -p1	NEEDS UPDATE - fails to build

# hardware
%patch20 -p1
#%%patch21 -p1	NEEDS UPDATE
%patch22 -p1
%patch23 -p1

# console
%if %{with bootsplash}
%patch30 -p1
%else
#%%patch31 -p1	NEEDS UPDATE
%endif

### netfilter
# base
%if 0
%patch40 -p1
%patch41 -p1
%patch42 -p1
%patch43 -p1
%patch44 -p1
%patch45 -p1
%patch46 -p1
%patch47 -p1
%patch48 -p1
%patch49 -p1
%patch50 -p1
%patch51 -p1
%patch52 -p1

## extra
%patch60 -p1
%patch61 -p1
%patch62 -p1
%patch63 -p1
%patch64 -p1
%patch65 -p1
%patch66 -p1
%endif
### end of netfilter

# net software
#%%patch70 -p1	NEEDS UPDATE
%patch71 -p1
%patch72 -p1
%patch73 -p1

#%%patch80 -p1	NEEDS a lot of work

# fixes
#%%patch90 -p1	NEEDS UPDATE
%patch91 -p1
%patch92 -p1
%patch100 -p1

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{_postver}_%{alt_kernel}#g' Makefile

sed -i -e '/select INPUT/d' net/bluetooth/hidp/Kconfig

%build
TuneUpConfigForIX86 () {
%ifarch %{ix86}
	pae=
	[ "$2" = "smp" ] && pae=yes
	%if %{with pae}
		pae=yes
	%endif
	%ifnarch i386
	sed -i 's:CONFIG_M386=y:# CONFIG_M386 is not set:' $1
	%endif
	%ifarch i486
	sed -i 's:# CONFIG_M486 is not set:CONFIG_M486=y:' $1
	%endif
	%ifarch i586
	sed -i 's:# CONFIG_M586 is not set:CONFIG_M586=y:' $1
	%endif
	%ifarch i686
	sed -i 's:# CONFIG_M686 is not set:CONFIG_M686=y:' $1
	%endif
	%ifarch pentium3
	sed -i 's:# CONFIG_MPENTIUMIII is not set:CONFIG_MPENTIUMIII=y:' $1
	%endif
	%ifarch pentium4
	sed -i 's:# CONFIG_MPENTIUM4 is not set:CONFIG_MPENTIUM4=y:' $1
	%endif
	%ifarch athlon
	sed -i 's:# CONFIG_MK7 is not set:CONFIG_MK7=y:' $1
	%endif
	%ifarch i686 athlon pentium3 pentium4
	if [ "$pae" = "yes" ]; then
		sed -i "s:CONFIG_HIGHMEM4G=y:# CONFIG_HIGHMEM4G is not set:" $1
		sed -i "s:# CONFIG_HIGHMEM64G is not set:CONFIG_HIGHMEM64G=y\nCONFIG_X86_PAE=y:" $1
	fi
	sed -i 's:CONFIG_MATH_EMULATION=y:# CONFIG_MATH_EMULATION is not set:' $1
	%endif
%endif
}


BuildConfig() {
	%{?debug:set -x}
	# is this a special kernel we want to build?
	smp=
	cfg="up"
	[ "$1" = "smp" -o "$2" = "smp" ] && smp="smp"
	if [ "$smp" = "smp" ]; then
		cfg="smp"
		Config="%{_target_base_arch}-smp"
	else
		Config="%{_target_base_arch}"
	fi
	KernelVer=%{ver_rel}$1

	echo "Building config file [using $Config.conf] for KERNEL $1..."

	cat %{SOURCE20} > .config
	cat $RPM_SOURCE_DIR/kernel-desktop-$Config.config >> .config
	echo "CONFIG_LOCALVERSION=\"-%{release}$smp\"" >> .config

	TuneUpConfigForIX86 .config "$smp"

	# preempt
%if %{with preemptrt}	
	cat %{SOURCE41} >> .config
%else
	cat %{SOURCE42} >> .config
%endif

	cat %{SOURCE43} >> .config

	# fbsplash, vesafb-tng, squashfs, imq, tahoe, atm, reiser4
	cat %{SOURCE44} >> .config

	# netfilter
	cat %{SOURCE45} >> .config

%if %{with grsec_minimal}
	cat %{SOURCE46} >> .config
%endif

%if %{with laptop}
	sed -e "s:CONFIG_HZ_1000=y:# CONFIG_HZ_1000 is not set:"	\
		-e "s:# CONFIG_HZ_100 is not set:CONFIG_HZ_100=y:"	\
		-e "s:CONFIG_HZ=1000:CONFIG_HZ=100:"			\
		-i .config
%endif

%if %{with bootsplash}
	sed -e 's:CONFIG_FB_SPLASH:CONFIG_BOOTSPLASH:'		\
		-e 's:CONFIG_LOGO=y:# CONFIG_LOGO is not set:'	\
		-i .config
%endif

%{?debug:sed -i "s:# CONFIG_DEBUG_SLAB is not set:CONFIG_DEBUG_SLAB=y:" .config}
%{?debug:sed -i "s:# CONFIG_DEBUG_PREEMPT is not set:CONFIG_DEBUG_PREEMPT=y:" .config}
%{?debug:sed -i "s:# CONFIG_RT_DEADLOCK_DETECT is not set:CONFIG_RT_DEADLOCK_DETECT=y:" .config}

	install .config arch/%{_target_base_arch}/defconfig
	install -d $KERNEL_INSTALL_DIR/usr/src/linux-%{ver}/include/linux
	rm -f include/linux/autoconf.h
	%{__make} %{MakeOpts} include/linux/autoconf.h
	install include/linux/autoconf.h \
		$KERNEL_INSTALL_DIR/usr/src/linux-%{ver}/include/linux/autoconf-${cfg}.h
	install .config \
		$KERNEL_INSTALL_DIR/usr/src/linux-%{ver}/config-${cfg}
	install .config arch/%{_target_base_arch}/defconfig
}

BuildKernel() {
	%{?debug:set -x}
	echo "Building kernel $1 ..."
	%{__make} %{MakeOpts} mrproper \
		RCS_FIND_IGNORE='-name build-done -prune -o'
	install arch/%{_target_base_arch}/defconfig .config

	%{__make} %{MakeOpts} clean \
		RCS_FIND_IGNORE='-name build-done -prune -o'

	%{__make} %{MakeOpts} include/linux/version.h \
		%{?with_verbose:V=1}


	%{__make} %{MakeOpts} \
		%{?with_verbose:V=1}
}

PreInstallKernel() {
	smp=
	cfg="up"
	[ "$1" = "smp" -o "$2" = "smp" ] && smp=smp
	if [ "$smp" = "smp" ]; then
		cfg="smp"
		Config="%{_target_base_arch}-smp"
	else
		Config="%{_target_base_arch}"
	fi
	KernelVer=%{ver_rel}$1

	mkdir -p $KERNEL_INSTALL_DIR/boot
	install System.map $KERNEL_INSTALL_DIR/boot/System.map-$KernelVer
%ifarch %{ix86} %{x8664}
	install arch/%{_target_base_arch}/boot/bzImage $KERNEL_INSTALL_DIR/boot/vmlinuz-$KernelVer
%endif

%ifarch ppc
	install vmlinux $KERNEL_INSTALL_DIR/boot/vmlinuz-$KernelVer
%endif
	install vmlinux $KERNEL_INSTALL_DIR/boot/vmlinux-$KernelVer

	%{__make} %{MakeOpts} modules_install \
		%{?with_verbose:V=1} \
		DEPMOD=%{DepMod} \
		INSTALL_MOD_PATH=$KERNEL_INSTALL_DIR \
		KERNELRELEASE=$KernelVer

	install Module.symvers \
		$KERNEL_INSTALL_DIR/usr/src/linux-%{ver}/Module.symvers-${cfg}

	echo "CHECKING DEPENDENCIES FOR KERNEL MODULES"
	%if "%{_target_base_arch}" != "%{_arch}"
		touch $KERNEL_INSTALL_DIR/lib/modules/$KernelVer/modules.dep
	%else
		/sbin/depmod --basedir $KERNEL_INSTALL_DIR -ae \
			-F $KERNEL_INSTALL_DIR/boot/System.map-$KernelVer -r $KernelVer \
			|| echo
	%endif
	echo "KERNEL RELEASE $KernelVer DONE"
}

KERNEL_BUILD_DIR=`pwd`

# UP KERNEL
KERNEL_INSTALL_DIR="$KERNEL_BUILD_DIR/build-done/kernel-UP"
rm -rf $KERNEL_INSTALL_DIR
BuildConfig
%if %{with up}
BuildKernel
PreInstallKernel
%endif

# SMP KERNEL
KERNEL_INSTALL_DIR="$KERNEL_BUILD_DIR/build-done/kernel-SMP"
rm -rf $KERNEL_INSTALL_DIR
BuildConfig smp
%if %{with smp}
BuildKernel smp
PreInstallKernel smp
%endif

%install
rm -rf $RPM_BUILD_ROOT
umask 022
export DEPMOD=%{DepMod}

install -d $RPM_BUILD_ROOT%{_prefix}/src/linux-%{ver}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{ver_rel}{,smp}

KERNEL_BUILD_DIR=`pwd`

%if %{with up} || %{with smp}
cp -a $KERNEL_BUILD_DIR/build-done/kernel-*/* $RPM_BUILD_ROOT
%endif

for i in "" smp ; do
	if [ -e  $RPM_BUILD_ROOT/lib/modules/%{ver_rel}$i ] ; then
		rm -f $RPM_BUILD_ROOT/lib/modules/%{ver_rel}$i/build
		ln -sf %{_prefix}/src/linux-%{ver} \
			$RPM_BUILD_ROOT/lib/modules/%{ver_rel}$i/build
		install -d $RPM_BUILD_ROOT/lib/modules/%{ver_rel}$i/{cluster,misc}
	fi
done

ln -sf linux-%{ver} $RPM_BUILD_ROOT%{_prefix}/src/linux-%{alt_kernel}

find . -maxdepth 1 ! -name "build-done" ! -name "." -exec cp -a "{}" "$RPM_BUILD_ROOT/usr/src/linux-%{ver}/" ";"

cd $RPM_BUILD_ROOT%{_prefix}/src/linux-%{ver}

%{__make} %{MakeOpts} mrproper \
	RCS_FIND_IGNORE='-name build-done -prune -o'

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

if [ -e $KERNEL_BUILD_DIR/build-done/kernel-UP/usr/src/linux-%{ver}/include/linux/autoconf-up.h ]; then
install $KERNEL_BUILD_DIR/build-done/kernel-UP/usr/src/linux-%{ver}/include/linux/autoconf-up.h \
	$RPM_BUILD_ROOT/usr/src/linux-%{ver}/include/linux
install	$KERNEL_BUILD_DIR/build-done/kernel-UP/usr/src/linux-%{ver}/config-up \
	$RPM_BUILD_ROOT/usr/src/linux-%{ver}
fi

if [ -e $KERNEL_BUILD_DIR/build-done/kernel-SMP/usr/src/linux-%{ver}/include/linux/autoconf-smp.h ]; then
install $KERNEL_BUILD_DIR/build-done/kernel-SMP/usr/src/linux-%{ver}/include/linux/autoconf-smp.h \
	$RPM_BUILD_ROOT/usr/src/linux-%{ver}/include/linux
install	$KERNEL_BUILD_DIR/build-done/kernel-SMP/usr/src/linux-%{ver}/config-smp \
	$RPM_BUILD_ROOT/usr/src/linux-%{ver}
fi

%if %{with up} || %{with smp}
# UP or SMP
install $KERNEL_BUILD_DIR/build-done/kernel-*/usr/src/linux-%{ver}/include/linux/* \
	$RPM_BUILD_ROOT/usr/src/linux-%{ver}/include/linux
%endif

install $KERNEL_BUILD_DIR/build-done/kernel-UP/usr/src/linux-%{ver}/config-up \
	.config
%{__make} %{MakeOpts} include/linux/version.h include/linux/utsrelease.h
mv include/linux/version.h{,.save}
mv include/linux/utsrelease.h{,.save}
%{__make} %{MakeOpts} mrproper
mv include/linux/version.h{.save,}
mv include/linux/utsrelease.h{.save,}
install %{SOURCE3} $RPM_BUILD_ROOT%{_prefix}/src/linux-%{ver}/include/linux/autoconf.h
install %{SOURCE4} $RPM_BUILD_ROOT%{_prefix}/src/linux-%{ver}/include/linux/config.h

# collect module-build files and directories
%{__perl} %{SOURCE5} %{_prefix}/src/linux-%{ver} $KERNEL_BUILD_DIR

%if %{with up} || %{with smp}
# ghosted initrd
touch $RPM_BUILD_ROOT/boot/initrd-%{ver_rel}{,smp}.gz
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%preun
rm -f /lib/modules/%{ver_rel}/modules.*
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{ver_rel}
fi

%post
mv -f /boot/vmlinuz-%{alt_kernel} /boot/vmlinuz-%{alt_kernel}.old 2> /dev/null > /dev/null
mv -f /boot/System.map-%{alt_kernel} /boot/System.map-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinuz-%{ver_rel} /boot/vmlinuz-%{alt_kernel}
ln -sf System.map-%{ver_rel} /boot/System.map-%{alt_kernel}
if [ ! -e /boot/vmlinuz ]; then
	mv -f /boot/vmlinuz /boot/vmlinuz.old 2> /dev/null > /dev/null
	mv -f /boot/System.map /boot/System.map.old 2> /dev/null > /dev/null
	ln -sf vmlinuz-%{ver_rel} /boot/vmlinuz
	ln -sf System.map-%{alt_kernel} /boot/System.map
	mv -f %{initrd_dir}/initrd %{initrd_dir}/initrd.old 2> /dev/null > /dev/null
	ln -sf initrd-%{alt_kernel} %{initrd_dir}/initrd
fi

%depmod %{ver_rel}

/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{ver_rel}.gz %{ver_rel}
mv -f %{initrd_dir}/initrd-%{alt_kernel} %{initrd_dir}/initrd-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf initrd-%{ver_rel}.gz %{initrd_dir}/initrd-%{alt_kernel}

if [ -x /sbin/new-kernel-pkg ]; then
	if [ -f /etc/pld-release ]; then
		title=$(sed 's/^[0-9.]\+ //' < /etc/pld-release)
	else
		title='PLD Linux'
	fi

	title="$title %{alt_kernel}"

	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{ver_rel}.gz --install %{ver_rel} --banner "$title"
elif [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post vmlinux
mv -f /boot/vmlinux-%{alt_kernel} /boot/vmlinux-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinux-%{ver_rel} /boot/vmlinux-%{alt_kernel}

%post drm
%depmod %{ver_rel}

%postun drm
%depmod %{ver_rel}

%post pcmcia
%depmod %{ver_rel}

%postun pcmcia
%depmod %{ver_rel}

%post sound-alsa
%depmod %{ver_rel}

%postun sound-alsa
%depmod %{ver_rel}

%post sound-oss
%depmod %{ver_rel}

%postun sound-oss
%depmod %{ver_rel}

%preun smp
rm -f /lib/modules/%{ver_rel}smp/modules.*
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{ver_rel}smp
fi

%post smp
mv -f /boot/vmlinuz-%{alt_kernel} /boot/vmlinuz.old-%{alt_kernel} 2> /dev/null > /dev/null
mv -f /boot/System.map-%{alt_kernel} /boot/System.map.old-%{alt_kernel} 2> /dev/null > /dev/null
ln -sf vmlinuz-%{ver_rel}smp /boot/vmlinuz-%{alt_kernel}
ln -sf System.map-%{ver_rel}smp /boot/System.map-%{alt_kernel}
if [ ! -e /boot/vmlinuz ]; then
	mv -f /boot/vmlinuz /boot/vmlinuz.old 2> /dev/null > /dev/null
	mv -f /boot/System.map /boot/System.map.old 2> /dev/null > /dev/null
	ln -sf vmlinuz-%{ver_rel} /boot/vmlinuz
	ln -sf System.map-%{ver_rel} /boot/System.map
	mv -f %{initrd_dir}/initrd %{initrd_dir}/initrd.old 2> /dev/null > /dev/null
	ln -sf initrd-%{alt_kernel} %{initrd_dir}/initrd
fi

%depmod %{ver_rel}smp

/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{ver_rel}smp.gz %{ver_rel}smp
mv -f %{initrd_dir}/initrd-%{alt_kernel} %{initrd_dir}/initrd.old-%{alt_kernel} 2> /dev/null > /dev/null
ln -sf initrd-%{ver_rel}smp.gz %{initrd_dir}/initrd-%{alt_kernel}

if [ -x /sbin/new-kernel-pkg ]; then
	if [ -f /etc/pld-release ]; then
		title=$(sed 's/^[0-9.]\+ //' < /etc/pld-release)
	else
		title='PLD Linux'
	fi

	title="$title %{alt_kernel}"

	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{ver_rel}smp.gz --install %{ver_rel}smp --banner "$title"
elif [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post smp-vmlinux
mv -f /boot/vmlinux-%{alt_kernel} /boot/vmlinux.old-%{alt_kernel} 2> /dev/null > /dev/null
ln -sf vmlinux-%{ver_rel}smp /boot/vmlinux-%{alt_kernel}

%post smp-drm
%depmod %{ver_rel}smp

%postun smp-drm
%depmod %{ver_rel}smp

%post smp-pcmcia
%depmod %{ver_rel}smp

%postun smp-pcmcia
%depmod %{ver_rel}smp

%post smp-sound-alsa
%depmod %{ver_rel}smp

%postun smp-sound-alsa
%depmod %{ver_rel}smp

%post smp-sound-oss
%depmod %{ver_rel}smp

%postun smp-sound-oss
%depmod %{ver_rel}smp

%post headers
rm -f /usr/src/linux-%{alt_kernel}
ln -snf linux-%{ver} /usr/src/linux-%{alt_kernel}

%postun headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux-%{alt_kernel} ]; then
		if [ "`ls -l %{_prefix}/src/linux-%{alt_kernel} | awk '{ print $10 }'`" = "linux-%{ver}" ]; then
			rm -f %{_prefix}/src/linux-%{alt_kernel}
		fi
	fi
fi

%if %{with up}
%files
%defattr(644,root,root,755)
/boot/vmlinuz-%{ver_rel}
/boot/System.map-%{ver_rel}
%ghost /boot/initrd-%{ver_rel}.gz
%dir /lib/modules/%{ver_rel}
%dir /lib/modules/%{ver_rel}/kernel
/lib/modules/%{ver_rel}/kernel/arch
/lib/modules/%{ver_rel}/kernel/crypto
/lib/modules/%{ver_rel}/kernel/drivers
%exclude /lib/modules/%{ver_rel}/kernel/drivers/char/drm
%if %{have_isa}
%exclude /lib/modules/%{ver_rel}/kernel/drivers/media/radio/miropcm20*.ko*
%endif
/lib/modules/%{ver_rel}/kernel/fs
/lib/modules/%{ver_rel}/kernel/kernel
/lib/modules/%{ver_rel}/kernel/lib
/lib/modules/%{ver_rel}/kernel/net
/lib/modules/%{ver_rel}/kernel/security
%dir /lib/modules/%{ver_rel}/kernel/sound
/lib/modules/%{ver_rel}/kernel/sound/soundcore.*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/media/video/*/*-alsa.ko*
%dir /lib/modules/%{ver_rel}/misc
%exclude /lib/modules/%{ver_rel}/kernel/drivers/pcmcia
%exclude /lib/modules/%{ver_rel}/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{ver_rel}/kernel/drivers/bluetooth/*_cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/ide/legacy/ide-cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/net/wireless/*_cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/parport/parport_cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/serial/serial_cs.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/telephony/ixj_pcmcia.ko*
%exclude /lib/modules/%{ver_rel}/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{ver_rel}/build
%ghost /lib/modules/%{ver_rel}/modules.*
%dir %{_sysconfdir}/modprobe.d/%{ver_rel}

%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{ver_rel}

%files drm
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}/kernel/drivers/char/drm

%files pcmcia
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}/kernel/drivers/pcmcia
/lib/modules/%{ver_rel}/kernel/drivers/*/pcmcia
/lib/modules/%{ver_rel}/kernel/drivers/bluetooth/*_cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/ide/legacy/ide-cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/net/wireless/*_cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/parport/parport_cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/serial/serial_cs.ko*
/lib/modules/%{ver_rel}/kernel/drivers/telephony/ixj_pcmcia.ko*
/lib/modules/%{ver_rel}/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{ver_rel}/kernel/sound/pcmcia

%files sound-alsa
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}/kernel/sound
/lib/modules/%{ver_rel}/kernel/drivers/media/video/*/*-alsa.ko*
%exclude %dir /lib/modules/%{ver_rel}/kernel/sound
%exclude /lib/modules/%{ver_rel}/kernel/sound/soundcore.*
%exclude /lib/modules/%{ver_rel}/kernel/sound/oss
%exclude /lib/modules/%{ver_rel}/kernel/sound/pcmcia

%files sound-oss
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}/kernel/sound/oss
%if %{have_isa}
/lib/modules/%{ver_rel}/kernel/drivers/media/radio/miropcm20*.ko*
%endif
%endif			# %%{with up}

%if %{with smp}
%files smp
%defattr(644,root,root,755)
#doc FAQ-pl
/boot/vmlinuz-%{ver_rel}smp
/boot/System.map-%{ver_rel}smp
%ghost /boot/initrd-%{ver_rel}smp.gz
%dir /lib/modules/%{ver_rel}smp
%dir /lib/modules/%{ver_rel}smp/kernel
/lib/modules/%{ver_rel}smp/kernel/arch
/lib/modules/%{ver_rel}smp/kernel/crypto
/lib/modules/%{ver_rel}smp/kernel/drivers
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/char/drm
%if %{have_isa}
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/media/radio/miropcm20*.ko*
%endif
/lib/modules/%{ver_rel}smp/kernel/fs
/lib/modules/%{ver_rel}smp/kernel/kernel
/lib/modules/%{ver_rel}smp/kernel/lib
/lib/modules/%{ver_rel}smp/kernel/net
/lib/modules/%{ver_rel}smp/kernel/security
%dir /lib/modules/%{ver_rel}smp/kernel/sound
/lib/modules/%{ver_rel}smp/kernel/sound/soundcore.*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/media/video/*/*-alsa.ko*
%dir /lib/modules/%{ver_rel}smp/misc
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/pcmcia
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/bluetooth/*_cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/ide/legacy/ide-cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/net/wireless/*_cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/parport/parport_cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/serial/serial_cs.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/telephony/ixj_pcmcia.ko*
%exclude /lib/modules/%{ver_rel}smp/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{ver_rel}smp/build
%ghost /lib/modules/%{ver_rel}smp/modules.*
%dir %{_sysconfdir}/modprobe.d/%{ver_rel}smp

%files smp-vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{ver_rel}smp

%files smp-drm
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}smp/kernel/drivers/char/drm

%files smp-pcmcia
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}smp/kernel/drivers/pcmcia
/lib/modules/%{ver_rel}smp/kernel/drivers/*/pcmcia
/lib/modules/%{ver_rel}smp/kernel/drivers/bluetooth/*_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/ide/legacy/ide-cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/net/wireless/*_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/parport/parport_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/serial/serial_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/telephony/ixj_pcmcia.ko*
/lib/modules/%{ver_rel}smp/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{ver_rel}smp/kernel/sound/pcmcia

%files smp-sound-alsa
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}smp/kernel/sound
/lib/modules/%{ver_rel}smp/kernel/drivers/media/video/*/*-alsa.ko*
%exclude %dir /lib/modules/%{ver_rel}smp/kernel/sound
%exclude /lib/modules/%{ver_rel}smp/kernel/sound/soundcore.*
%exclude /lib/modules/%{ver_rel}smp/kernel/sound/oss
%exclude /lib/modules/%{ver_rel}smp/kernel/sound/pcmcia

%files smp-sound-oss
%defattr(644,root,root,755)
/lib/modules/%{ver_rel}smp/kernel/sound/oss
%if %{have_isa}
/lib/modules/%{ver_rel}smp/kernel/drivers/media/radio/miropcm20*.ko*
%endif
%endif			# %%{with smp}

%files headers
%defattr(644,root,root,755)
%dir %{_prefix}/src/linux-%{ver}
%{_prefix}/src/linux-%{ver}/include
%{_prefix}/src/linux-%{ver}/config-smp
%{?with_smp:%{_prefix}/src/linux-%{ver}/Module.symvers-smp}
%{_prefix}/src/linux-%{ver}/config-up
%{?with_up:%{_prefix}/src/linux-%{ver}/Module.symvers-up}

%files module-build -f aux_files
%defattr(644,root,root,755)
%{_prefix}/src/linux-%{ver}/Kbuild
%{_prefix}/src/linux-%{ver}/arch/*/kernel/asm-offsets.*
%{_prefix}/src/linux-%{ver}/arch/*/kernel/sigframe.h
%dir %{_prefix}/src/linux-%{ver}/scripts
%dir %{_prefix}/src/linux-%{ver}/scripts/kconfig
%{_prefix}/src/linux-%{ver}/scripts/Kbuild.include
%{_prefix}/src/linux-%{ver}/scripts/Makefile*
%{_prefix}/src/linux-%{ver}/scripts/basic
%{_prefix}/src/linux-%{ver}/scripts/mkmakefile
%{_prefix}/src/linux-%{ver}/scripts/mod
%{_prefix}/src/linux-%{ver}/scripts/setlocalversion
%{_prefix}/src/linux-%{ver}/scripts/*.c
%{_prefix}/src/linux-%{ver}/scripts/*.sh
%{_prefix}/src/linux-%{ver}/scripts/kconfig/*

%files doc
%defattr(644,root,root,755)
%{_prefix}/src/linux-%{ver}/Documentation

%if %{with source}
%files source -f aux_files_exc
%defattr(644,root,root,755)
%{_prefix}/src/linux-%{ver}/arch/*/[!Mk]*
%{_prefix}/src/linux-%{ver}/arch/*/kernel/[!M]*
%exclude %{_prefix}/src/linux-%{ver}/arch/*/kernel/asm-offsets.*
%exclude %{_prefix}/src/linux-%{ver}/arch/*/kernel/sigframe.h
%{_prefix}/src/linux-%{ver}/block
%{_prefix}/src/linux-%{ver}/crypto
%{_prefix}/src/linux-%{ver}/drivers
%{_prefix}/src/linux-%{ver}/fs
%if %{with grsec_minimal}
%{_prefix}/src/linux-%{ver}/grsecurity
%endif
%{_prefix}/src/linux-%{ver}/init
%{_prefix}/src/linux-%{ver}/ipc
%{_prefix}/src/linux-%{ver}/kernel
%{_prefix}/src/linux-%{ver}/lib
%{_prefix}/src/linux-%{ver}/mm
%{_prefix}/src/linux-%{ver}/net
%{_prefix}/src/linux-%{ver}/scripts/*
%exclude %{_prefix}/src/linux-%{ver}/scripts/Kbuild.include
%exclude %{_prefix}/src/linux-%{ver}/scripts/Makefile*
%exclude %{_prefix}/src/linux-%{ver}/scripts/basic
%exclude %{_prefix}/src/linux-%{ver}/scripts/kconfig
%exclude %{_prefix}/src/linux-%{ver}/scripts/mkmakefile
%exclude %{_prefix}/src/linux-%{ver}/scripts/mod
%exclude %{_prefix}/src/linux-%{ver}/scripts/setlocalversion
%exclude %{_prefix}/src/linux-%{ver}/scripts/*.c
%exclude %{_prefix}/src/linux-%{ver}/scripts/*.sh
%{_prefix}/src/linux-%{ver}/sound
%{_prefix}/src/linux-%{ver}/security
%{_prefix}/src/linux-%{ver}/usr
%{_prefix}/src/linux-%{ver}/COPYING
%{_prefix}/src/linux-%{ver}/CREDITS
%{_prefix}/src/linux-%{ver}/MAINTAINERS
%{_prefix}/src/linux-%{ver}/README
%{_prefix}/src/linux-%{ver}/REPORTING-BUGS
%endif

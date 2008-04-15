#
# TODO:
# - pcmcia moved to main pkg (pcmcia.ko only or subpkg killed?):
#    ssb: Unknown symbol pcmcia_access_configuration_register
#    ohci_hcd: Unknown symbol ssb_device_disable
# - put together a default .config that makes sense for desktops
# - make sure patch numbering is consistent and prepare it
#   for the future
# - investigate ppc-ICE patches from kernel.spec (does it fix the e1000 ICE?)
# - investigate pwc-uncompress patch from kernel.spec
# - investigate apparmor-caps patch from kernel.spec
# - actively search for other superb enhancing patches
#   (even the experimental ones, as kernel-desktop is not
#   mainline kernel)
# - check if we don't have newer netfilter (kernel.spec claims 2007) # - check for all patches update
# - links and descriptions above al PatchesXXX and %patchXXX
#
# Conditional build:
%bcond_without	source		# don't build kernel-source package
%bcond_with		noarch		# build noarch packages
%bcond_with		verbose		# verbose build (V=1)
%bcond_with		preemptrt	# use realtime-preempt patch
%bcond_without	tuxonice	# support for tuxonice (ex-suspend2)
%bcond_with		fcache		# Jens Axboe's fcache patch (ext3 only)
%bcond_without	ck			# Con Kolivas desktop improvements patchset
%bcond_without	reiser4		# support for reiser4 fs (experimental)
%bcond_without	squashfs	# support for squashfs
%bcond_with		supermount	# support for supermount-ng
%bcond_without	unionfs		# support for unionfs
%bcond_with		grsec_minimal	# don't build grsecurity (minimal subset: proc,link,fifo,shm)
%bcond_with		bootsplash	# build with bootsplash instead of fbsplash
%bcond_without	imq			# imq
%bcond_without	wrr			# wrr support
%bcond_with		laptop		# build with HZ=100
%bcond_with		pae			# build PAE (HIGHMEM64G) support on uniprocessor

%{?debug:%define with_verbose 1}

%if %{with bootsplash}
%undefine	with_fbsplash
%else
%define		with_fbsplash	1
%endif

%ifnarch %{ix86}
%undefine	with_pae
%endif

%if "%{_arch}" == "noarch"
%define		with_noarch	1
%endif

%ifarch %{ix86} ppc
%define		have_isa	1
%else
%define		have_isa	0
%endif

%if %{with laptop}
%define		alt_kernel	laptop%{?with_preemptrt:_rt}
%else
%define		alt_kernel	desktop%{?with_preemptrt:_rt}
%endif

# Our Kernel ABI, increase this when you want out of source modules being rebuilt
%define		KABI		1

# kernel release (used in filesystem and eventually in uname -r)
# modules will be looked from /lib/modules/%{kernel_release}
# _localversion is just that without version for "> localversion"
%define		_localversion %{KABI}
%define		kernel_release %{version}_%{alt_kernel}-%{_localversion}
%define		_kernelsrcdir	/usr/src/linux-%{version}_%{alt_kernel}

%define		_basever	2.6.24
%define		_postver	.4
%define		_rel		0.3
%define		_rc	%{nil}

%define		_enable_debug_packages			0
%define		netfilter_snap		20061213

%define		pname	kernel-desktop
Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de.UTF-8):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(et.UTF-8):	Linuxi kernel (ehk operatsioonisüsteemi tuum)
Summary(fr.UTF-8):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl.UTF-8):	Jądro Linuksa
Name:		kernel-%{alt_kernel}
Version:	%{_basever}%{_postver}
Release:	%{_rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{_basever}.tar.bz2
# Source0-md5:	3f23ad4b69d0a552042d1ed0f4399857
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	508f5aaa99dead9836ff490496a61581
Source2:	kernel-vanilla-module-build.pl
Source3:	kernel-config.py
Source4:	kernel-config-update.py
Source5:	kernel-multiarch.make
Source6:	%{pname}-config.h
Source7:	%{pname}-module-build.pl

Source9:	%{pname}-common.config
Source10:	%{pname}-preempt-rt.config
Source11:	%{pname}-preempt-nort.config
Source12:	%{pname}-tuxonice.config
Source13:	%{pname}-patches.config
Source14:	%{pname}-netfilter.config
Source15:	%{pname}-grsec.config
Source16:	%{pname}-wrr.config
Source17:	%{pname}-fbsplash.config
Source18:	%{pname}-bootsplash.config
Source19:	%{pname}-imq.config
Source20:	%{pname}-reiser4.config
Source21:	%{pname}-squashfs.config
Source22:	%{pname}-unionfs.config

###
#	Patches
###

#Patch0:		%{pname}-preempt-rt.patch

# Project suspend2 renamed to tuxonice
# http://www.tuxonice.net/downloads/all/tuxonice-3.0-rc5-for-2.6.24.patch.bz2
Patch1:		%{pname}-tuxonice.patch

# Jens Axboe's fcache patch (for ext3 only)
# http://git.kernel.dk/?p=linux-2.6-block.git;a=commitdiff;h=118e3e9250ef319b6e77cdbc25dc4d26084c14f
# http://en.opensuse.org/Fcache-howto
Patch6:		%{pname}-fcache.patch

### Con Kolivas patchset
# http://waninkoko.info/ckpatches/2.6.24/
Patch7:		%{pname}-ck.patch
Patch8:		%{pname}-tuxonice-ck.patch

Patch9:		%{pname}-grsec-minimal.patch

### filesystems
# previously based on ftp://ftp.namesys.com/pub/reiser4-for-2.6/2.6.22/reiser4-for-2.6.22-2.patch.gz
# now based on ftp.kernel.org:/pub/linux/kernel/people/akpm/patches/2.6/2.6.24-rc8/2.6.24-rc8-mm1/broken-out/reiser4*
Patch10:	%{pname}-reiser4.patch

# http://mesh.dl.sourceforge.net/sourceforge/squashfs/squashfs3.3.tgz
# squashfs3.3/kernel-patches/linux-2.6.24/squashfs3.3-patch
Patch11:	%{pname}-squashfs.patch

# http://dl.sourceforge.net/sourceforge/supermount-ng/supermount-ng-2.2.2-2.6.22.1_madgus_gcc34.patch.gz
Patch12:	%{pname}-supermount-ng.patch

# http://download.filesystems.org/unionfs/unionfs-2.x/unionfs-2.2.2_for_2.6.24-rc7.diff.gz
Patch13:	%{pname}-unionfs.patch

### hardware
# tahoe9XX http://tahoe.pl/drivers/tahoe9xx-2.6.11.5.patch
Patch20:	%{pname}-tahoe9xx.patch

# http://pred.dcaf-security.org/sata_nv-ncq-support-mcp51-mcp55-mcp61.patch
# NCQ Functionality for newer nvidia chipsets (MCP{51,55,61}) by nvidia crew
#Patch25:	%{pname}-sata_nv-ncq.patch
# http://memebeam.org/free-software/toshiba_acpi/toshiba_acpi-dev_toshiba_test5-linux_2.6.21.patch
Patch26:	%{pname}-toshiba-acpi.patch

### console
# ftp://ftp.openbios.org/pub/bootsplash/kernel/bootsplash-3.1.6-2.6.21.diff.gz
Patch30:	%{pname}-bootsplash.patch
# based on http://dev.gentoo.org/~spock/projects/gensplash/archive/fbsplash-0.9.2-r5-2.6.20-rc6.patch
Patch31:	%{pname}-fbsplash.patch

########	netfilter snap
## base
Patch40:	%{pname}-pom-ng-IPV4OPTSSTRIP.patch
Patch41:	%{pname}-pom-ng-ipv4options.patch
Patch42:	%{pname}-pom-ng-set.patch
Patch43:	%{pname}-pom-ng-u32.patch
Patch44:	%{pname}-pom-ng-ROUTE.patch
Patch45:	%{pname}-pom-ng-TARPIT.patch
Patch46:	%{pname}-pom-ng-mms-conntrack-nat.patch
Patch47:	%{pname}-pom-ng-IPMARK.patch
Patch48:	%{pname}-pom-ng-connlimit.patch
Patch49:	%{pname}-pom-ng-geoip.patch
Patch50:	%{pname}-pom-ng-ipp2p.patch
Patch51:	%{pname}-pom-ng-time.patch
Patch52:	%{pname}-pom-ng-rsh.patch
Patch53:	%{pname}-pom-ng-rpc.patch

# based on http://www.svn.barbara.eu.org/ipt_account/attachment/wiki/Software/ipt_account-0.1.21-20070804164729.tar.gz?format=raw
Patch67:	%{pname}-ipt_account.patch

# based on http://www.intra2net.com/de/produkte/opensource/ipt_account/pom-ng-ipt_ACCOUNT-1.10.tgz
Patch68:	%{pname}-ipt_ACCOUNT.patch

# netfilter-layer7-v2.13.tar.gz from http://l7-filter.sf.net/
Patch69:	%{pname}-layer7.patch
########	End netfilter

### net software
# based on http://www.linuximq.net/patchs/linux-2.6.24-imq.diff
# some people report problems when using imq with wrr.
Patch70:	%{pname}-imq.patch

# esfq from http://fatooh.org/esfq-2.6/current/esfq-kernel.patch
Patch71:	%{pname}-esfq.patch

# by Baggins request:
# derived from ftp://ftp.cmf.nrl.navy.mil/pub/chas/linux-atm/vbr/vbr-kernel-diffs
Patch72:	%{pname}-atm-vbr.patch
Patch73:	%{pname}-atmdd.patch

# wrr http://www.zz9.dk/patches/wrr-linux-070717-2.6.22.patch.gz
Patch74:	%{pname}-wrr.patch

# adds some ids for hostap suported cards and monitor_enable from/for aircrack-ng
# http://patches.aircrack-ng.org/hostap-kernel-2.6.18.patch
Patch75:	%{pname}-hostap.patch

# http://www.ntop.org/PF_RING.html 20070610
Patch76:	%{pname}-PF_RING.patch

# The following patch extend the routing functionality in Linux
# to support static routes (defined by user), new way to use the
# alternative routes, the reverse path protection (rp_filter),
# the NAT processing to use correctly the routing when multiple
# gateways are used.
# http://www.ssi.bg/~ja/routes-2.6.24-15.diff
# We need to disable CONFIG_IP_ROUTE_MULTIPATH_CACHED
Patch77:	%{pname}-routes.patch

### Additional features
# http://www.bullopensource.org/cpuset/ - virtual CPUs
Patch85:	%{pname}-cpuset_virtualization.patch

### Fixes
Patch90:	kernel-mcpu=440.patch
Patch91:	%{pname}-fbcon-margins.patch
Patch92:	%{pname}-static-dev.patch
Patch100:	%{pname}-small_fixes.patch
# Wake-On-Lan fix for nForce drivers; using http://atlas.et.tudelft.nl/verwei90/nforce2/wol.html
# Fix verified for that kernel version.
Patch102:	%{pname}-forcedeth-WON.patch
Patch103:	%{pname}-ueagle-atm-freezer.patch
# investigate
Patch104:	%{pname}-ppc-ICE.patch

# http://synce.svn.sourceforge.net/svnroot/synce/trunk/patches/linux-2.6.22-rndis_host-wm5.patch
Patch105:	%{pname}-rndis_host.patch

# add tty ioctl to figure physical device of the console. used by showconsole.spec (blogd)
#Patch106:	kernel-TIOCGDEV.patch

URL:		http://www.kernel.org/
BuildRequires:	/sbin/depmod
BuildRequires:	binutils >= 3:2.14.90.0.7
BuildRequires:	%{kgcc_package} >= 5:3.2
BuildRequires:	module-init-tools
# for hostname command
BuildRequires:	net-tools
BuildRequires:	perl-base
BuildRequires:	rpmbuild(macros) >= 1.217
Autoreqprov:	no
Requires:	/sbin/depmod
Requires:	coreutils
Requires:	geninitrd >= 8702
Requires:	module-init-tools >= 0.9.9
%{?with_bootsplash:Suggests:	bootsplash}
%{?with_fbsplash:Suggests:	splashutils}
Provides:	%{name}(vermagic) = %{kernel_release}
Conflicts:	e2fsprogs < 1.29
Conflicts:	isdn4k-utils < 3.1pre1
Conflicts:	jfsutils < 1.1.3
Conflicts:	module-init-tools < 0.9.10
Conflicts:	nfs-utils < 1.0.5
Conflicts:	oprofile < 0.9
Conflicts:	ppp < 1:2.4.0
Conflicts:	procps < 3.2.0
Conflicts:	quota-tools < 3.09
%if %{with reiser4}
Conflicts:	reiser4progs < 1.0.0
%endif
Conflicts:	reiserfsprogs < 3.6.3
Conflicts:	udev < 1:071
Conflicts:	util-linux < 2.10o
Conflicts:	xfsprogs < 2.6.0
%{?with_noarch:BuildArch:	noarch}
ExclusiveArch:	%{ix86} %{x8664} ppc noarch
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%ifarch %{ix86} %{x8664}
%define		target_arch_dir	x86
%else
%define		target_arch_dir	%{_target_base_arch}
%endif

# No ELF objects there to strip (skips processing 27k files)
%define		_noautostrip	.*%{_kernelsrcdir}/.*
%define		_noautochrpath	.*%{_kernelsrcdir}/.*

%define		initrd_dir	/boot

%define		topdir	%{_builddir}/%{name}-%{version}
%define		srcdir	%{topdir}/linux-%{_basever}
%define		objdir	%{topdir}/o

%define		CommonOpts	HOSTCC="%{kgcc}" HOSTCFLAGS="-Wall -Wstrict-prototypes %{rpmcflags} -fomit-frame-pointer"
%if "%{_target_base_arch}" != "%{_arch}"
	%define	MakeOpts %{CommonOpts} ARCH=%{_target_base_arch} CROSS_COMPILE=%{_target_cpu}-pld-linux-
	%define	DepMod /bin/true

	%if "%{_arch}" == "x86_64" && "%{_target_base_arch}" == "i386"
	%define	MakeOpts %{CommonOpts} CC="%{kgcc}" ARCH=%{_target_base_arch}
	%define	DepMod /sbin/depmod
	%endif

%else
	%define MakeOpts %{CommonOpts} CC="%{kgcc}"
	%define	DepMod /sbin/depmod
%endif

%define __features Enabled features:\
%{?debug: - DEBUG}\
%{?with_tuxonice: - TuxOnIce (formerly known as suspend2)}\
%{?with_preemptrt: - realtime-preempt patch by Ingo Molar}\
%{?with_ck: - desktop patchset by Con Kolivas}\
%{?with_grsec_minimal: - grsecurity minimal}\
 - %{?with_bootsplash:bootsplash}%{?with_fbsplash:fbsplash}\
 - HZ=100%{!?with_laptop:0}

%define Features %(echo "%{__features}" | sed '/^$/d')

%description
This package contains the Linux kernel that is used to boot and run
your system. It contains few device drivers for specific hardware.
Most hardware is instead supported by modules loaded after booting.

%{Features}

%description -l de.UTF-8
Das Kernel-Packet enthält den Linux-Kernel (vmlinuz), den Kern des
Linux-Betriebssystems. Der Kernel ist für grundliegende
Systemfunktionen verantwortlich: Speicherreservierung,
Prozeß-Management, Geräte Ein- und Ausgaben, usw.

%{Features}

%description -l fr.UTF-8
Le package kernel contient le kernel linux (vmlinuz), la partie
centrale d'un système d'exploitation Linux. Le noyau traite les
fonctions basiques d'un système d'exploitation: allocation mémoire,
allocation de process, entrée/sortie de peripheriques, etc.

%{Features}

%description -l pl.UTF-8
Pakiet zawiera jądro Linuksa niezbędne do prawidłowego działania
Twojego komputera. Zawiera w sobie sterowniki do sprzętu znajdującego
się w komputerze, takiego jak sterowniki dysków itp.

%{Features}

%package vmlinux
Summary:	vmlinux - uncompressed kernel image
Summary(de.UTF-8):	vmlinux - dekompressiertes Kernel Bild
Summary(pl.UTF-8):	vmlinux - rozpakowany obraz jądra
Group:		Base/Kernel

%description vmlinux
vmlinux - uncompressed kernel image.

%description vmlinux -l de.UTF-8
vmlinux - dekompressiertes Kernel Bild.

%description vmlinux -l pl.UTF-8
vmlinux - rozpakowany obraz jądra.

%package drm
Summary:	DRM kernel modules
Summary(de.UTF-8):	DRM Kernel Treiber
Summary(pl.UTF-8):	Sterowniki DRM
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description drm
DRM kernel modules.

%description drm -l de.UTF-8
DRM Kernel Treiber.

%description drm -l pl.UTF-8
Sterowniki DRM.

%package pcmcia
Summary:	PCMCIA modules
Summary(de.UTF-8):	PCMCIA Module
Summary(pl.UTF-8):	Moduły PCMCIA
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Conflicts:	pcmcia-cs < 3.1.21
Conflicts:	pcmciautils < 004
Autoreqprov:	no

%description pcmcia
PCMCIA modules.

%description pcmcia -l de.UTF-8
PCMCIA Module.

%description pcmcia -l pl.UTF-8
Moduły PCMCIA.

%package sound-alsa
Summary:	ALSA kernel modules
Summary(de.UTF-8):	ALSA Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku ALSA
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-alsa
ALSA (Advanced Linux Sound Architecture) sound drivers.

%description sound-alsa -l de.UTF-8
ALSA (Advanced Linux Sound Architecture) Sound-Treiber.

%description sound-alsa -l pl.UTF-8
Sterowniki dźwięku ALSA (Advanced Linux Sound Architecture).

%package sound-oss
Summary:	OSS kernel modules
Summary(de.UTF-8):	OSS Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku OSS
Group:		Base/Kernel
Requires:	%{name} = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-oss
OSS (Open Sound System) drivers.

%description sound-oss -l de.UTF-8
OSS (Open Sound System) Treiber.

%description sound-oss -l pl.UTF-8
Sterowniki dźwięku OSS (Open Sound System).

%package config
Summary:	Kernel config and module symvers
Summary(pl.UTF-8):	Konfiguracja jądra i wersje symboli
Group:		Development/Building
Autoreqprov:	no
Conflicts:	rpmbuild(macros) < 1.433

%description config
Kernel config and module symvers.

%description config -l pl.UTF-8
Konfiguracja jądra i wersje symboli.

%package headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
Group:		Development/Building
Requires:	%{name}-config = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description headers
These are the C header files for the Linux kernel, which define
structures and constants that are needed when rebuilding the kernel or
building kernel modules.

%description headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten, die beim rekompilieren des Kernels
oder bei Kernel Modul kompilationen gebraucht werden.

%description headers -l pl.UTF-8
Pakiet zawiera pliki nagłówkowe jądra, niezbędne do rekompilacji jądra
oraz budowania modułów jądra.

%package module-build
Summary:	Development files for building kernel modules
Summary(de.UTF-8):	Development Dateien die beim Kernel Modul kompilationen gebraucht werden
Summary(pl.UTF-8):	Pliki służące do budowania modułów jądra
Group:		Development/Building
Requires:	%{name}-headers = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description module-build
Development files from kernel source tree needed to build Linux kernel
modules from external packages.

%description module-build -l de.UTF-8
Development Dateien des Linux-Kernels die beim kompilieren externer
Kernel Module gebraucht werden.

%description module-build -l pl.UTF-8
Pliki ze drzewa źródeł jądra potrzebne do budowania modułów jądra
Linuksa z zewnętrznych pakietów.

%package source
Summary:	Kernel source tree
Summary(de.UTF-8):	Der Kernel Quelltext
Summary(pl.UTF-8):	Kod źródłowy jądra Linuksa
Group:		Development/Building
Requires:	%{name}-module-build = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description source
This is the source code for the Linux kernel. You can build a custom
kernel that is better tuned to your particular hardware.

%description source -l de.UTF-8
Das Kernel-Source-Packet enthält den source code (C/Assembler-Code)
des Linux-Kernels. Die Source-Dateien werden gebraucht, um viele
C-Programme zu kompilieren, da sie auf Konstanten zurückgreifen, die
im Kernel-Source definiert sind. Die Source-Dateien können auch
benutzt werden, um einen Kernel zu kompilieren, der besser auf Ihre
Hardware ausgerichtet ist.

%description source -l fr.UTF-8
Le package pour le kernel-source contient le code source pour le noyau
linux. Ces sources sont nécessaires pour compiler la plupart des
programmes C, car il dépend de constantes définies dans le code
source. Les sources peuvent être aussi utilisée pour compiler un noyau
personnalisé pour avoir de meilleures performances sur des matériels
particuliers.

%description source -l pl.UTF-8
Pakiet zawiera kod źródłowy jądra systemu.

%package doc
Summary:	Kernel documentation
Summary(de.UTF-8):	Kernel Dokumentation
Summary(pl.UTF-8):	Dokumentacja do jądra Linuksa
Group:		Documentation
Autoreqprov:	no

%description doc
This is the documentation for the Linux kernel, as found in
/usr/src/linux/Documentation directory.

%description doc -l de.UTF-8
Dies ist die Kernel Dokumentation wie sie im 'Documentation'
Verzeichniss vorgefunden werden kann.

%description doc -l pl.UTF-8
Pakiet zawiera dokumentację do jądra Linuksa pochodzącą z katalogu
/usr/src/linux/Documentation.

%prep
%setup -qc
install -d o/scripts
ln -s %{SOURCE2} o/scripts/kernel-module-build.pl
ln -s %{SOURCE3} o/scripts/kernel-config.py
ln -s %{SOURCE4} o/scripts/kernel-config-update.py
ln -s %{SOURCE5} Makefile

cd linux-%{_basever}
%if "%{_postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | %{__patch} -p1 -s
%endif

%if %{with tuxonice}
%patch1 -p1
%endif

%if %{with preemptrt}
#%patch0 -p1
%endif

%if %{with fcache}
%patch6 -p1
%endif

%if %{with ck}
%patch7 -p1
%if %{with tuxonice}
%patch8 -p1
%endif
%endif

%if %{with grsec_minimal}
%patch9 -p1
%endif

%if %{with reiser4}
%patch10 -p1
%endif

%if %{with squashfs}
%patch11 -p1
%endif

%if %{with supermount}
%patch12 -p1
%endif

%if %{with unionfs}
%patch13 -p1
%endif

### hardware
%patch20 -p1
%if 0
#%patch25 -p1 # FIND UPDATE
%endif
# toshiba-acpi
%patch26 -p1

### console
%if %{with bootsplash}
%patch30 -p1
%endif
%if %{with fbsplash}
%patch31 -p1
%endif

## netfilter
#

# kernel-pom-ng-IPV4OPTSSTRIP.patch
%patch40 -p1

# kernel-pom-ng-ipv4options.patch
%patch41 -p1

# kernel-pom-ng-u32.patch
%patch43 -p1

# kernel-pom-ng-ROUTE.patch
%patch44 -p1

# kernel-pom-ng-TARPIT.patch
%patch45 -p1

# kernel-pom-ng-mms-conntrack-nat.patch
%patch46 -p1

# kernel-pom-ng-IPMARK.patch
%patch47 -p1

# kernel-pom-ng-set.patch
#patch42 -p1

# kernel-pom-ng-connlimit.patch
%patch48 -p1

# kernel-pom-ng-geoip.patch
%patch49 -p1

# kernel-pom-ng-ipp2p.patch
%patch50 -p1

# kernel-pom-ng-time.patch
%patch51 -p1

# kernel-pom-ng-rsh.patch
%patch52 -p1

# kernel-pom-ng-rpc.patch
%patch53 -p1

# kernel-ipt_account.patch
%patch67 -p1

# kernel-ipt_ACCOUNT.patch
%patch68 -p1

# kernel-layer7.patch
%patch69 -p1

##
# end of netfilter

### net software
%if %{with imq}
%patch70 -p1
%endif

%patch71 -p1
# atm-vbr
%patch72 -p1
# atmdd
%patch73 -p1

%if %{with wrr}
%patch74 -p1
%endif

# hostap enhancements from/for aircrack-ng
%patch75 -p1

# PF_RING
%patch76 -p1
# static routes
%patch77 -p1

### fixes
%patch90 -p1
%patch91 -p1
%patch92 -p1
%patch100 -p1
# forcedeth
%patch102 -p1
# ueagle freezer
%patch103 -p1
# ppc ICE fixes
%ifarch ppc ppc64
%patch104 -p1
%endif
%patch105 -p1
#%patch106 -p1 # FIND UPDATE

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{_postver}_%{alt_kernel}#g' Makefile

# cleanup backups after patching
find '(' -name '*~' -o -name '*.orig' -o -name '.gitignore' ')' -print0 | xargs -0 -r -l512 rm -f

%if %{without noarch}
%build
cat > multiarch.make <<'EOF'
# generated by %{name}.spec
KERNELSRC		:= %{_builddir}/%{name}-%{version}/linux-%{_basever}
KERNELOUTPUT	:= %{objdir}

SRCARCH		:= %{target_arch_dir}
ARCH		:= %{_target_base_arch}
Q			:= %{!?with_verbose:@}
MAKE_OPTS	:= %{MakeOpts}

CONFIGS += %{_sourcedir}/%{pname}-common.config

# preempt
%if %{with preemptrt}
CONFIGS += %{_sourcedir}/%{pname}-preempt-rt.config
%else
CONFIGS += %{_sourcedir}/%{pname}-preempt-nort.config
%endif

# tuxonice
%if %{with tuxonice}
CONFIGS += %{_sourcedir}/%{pname}-tuxonice.config
%endif

# tahoe, atm
CONFIGS += %{_sourcedir}/%{pname}-patches.config

# netfilter
CONFIGS += %{_sourcedir}/%{pname}-netfilter.config

%if %{with grsec_minimal}
CONFIGS += %{_sourcedir}/%{pname}-grsec.config
%endif
# wrr
%if %{with wrr}
CONFIGS += %{_sourcedir}/%{pname}-wrr.config
%endif

%if %{with imq}
CONFIGS += %{_sourcedir}/%{pname}-imq.config
%endif

%if %{with reiser4}
CONFIGS += %{_sourcedir}/%{pname}-reiser4.config
%endif

%if %{with squashfs}
CONFIGS += %{_sourcedir}/%{pname}-squashfs.config
%endif

%if %{with unionfs}
CONFIGS += %{_sourcedir}/%{pname}-unionfs.config
%endif

%if %{with bootsplash}
CONFIGS += %{_sourcedir}/%{pname}-bootsplash.config
%endif

%if %{with fbsplash}
CONFIGS += %{_sourcedir}/%{pname}-fbsplash.config
%endif

# config where we ignore timestamps
CONFIG_NODEP += %{objdir}/.kernel-autogen.conf
EOF

# update config at spec time
# if you have config file, add it to above Makefile
pykconfig() {
	set -x
	echo '# %{name}.spec overrides'
	echo 'LOCALVERSION="-%{_localversion}"'

	%{?debug:echo '# debug options'}
	%{?debug:echo 'DEBUG_SLAB=y'}
	%{?debug:echo 'DEBUG_PREEMPT=y'}
	%{?debug:echo 'RT_DEADLOCK_DETECT=y'}

%ifarch %{ix86}
	echo '# x86 tuneup'
	%ifarch i386
	echo 'M386=y'
	echo 'X86_F00F_BUG=y'
	%endif
	%ifarch i486
	echo 'M486=y'
	echo 'X86_F00F_BUG=y'
	%endif
	%ifarch i586
	echo 'M586=y'
	echo 'X86_F00F_BUG=y'
	%endif
	%ifarch i686
	echo 'M686=y'
	%endif
	%ifarch pentium3
	echo 'MPENTIUMIII=y'
	%endif
	%ifarch pentium4
	echo 'MPENTIUM4=y'
	%endif
	%ifarch athlon
	echo 'MK7=y'
	echo 'X86_PPRO_FENCE='
	echo 'X86_USE_3DNOW=y'
	%endif
	%ifarch i686 athlon pentium3 pentium4
		%if %{with pae}
			echo 'HIGHMEM4G=n'
			echo 'HIGHMEM64G=y'
			echo 'X86_PAE=y'
		%endif
	echo 'MATH_EMULATION=n'
	%endif
%endif

	%ifnarch i386
		echo 'NO_HZ=n'
		echo 'HZ_1000=y'
		echo 'HZ=1000'
	%endif

	%if %{with laptop}
		echo 'HZ_1000=n'
		echo 'HZ_100=y'
		echo 'HZ=100'
	%endif

	# disable e1000 on ppc (ICEs)
	%ifarch ppc ppc64
		echo 'E1000=n'
		echo 'E1000_NAPI=n'
		echo 'E1000_DISABLE_PACKET_SPLIT=n'
	%endif
}

# generate .config and kernel.conf
pykconfig > %{objdir}/.kernel-autogen.conf
%{__make} pykconfig

# build kernel
%{__make} all
%endif # arch build

%install
rm -rf $RPM_BUILD_ROOT
# touch for noarch build (exclude list)
install -d $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux
touch $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/{utsrelease,version,autoconf-dist}.h

%if %{without noarch}
%{__make} %{MakeOpts} %{!?with_verbose:-s} modules_install \
	-C %{objdir} \
	%{?with_verbose:V=1} \
	DEPMOD=%{DepMod} \
	INSTALL_MOD_PATH=$RPM_BUILD_ROOT \
	KERNELRELEASE=%{kernel_release}

mkdir $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/misc
rm -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{build,source}
touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{build,source}

# /boot
install -d $RPM_BUILD_ROOT/boot
cp -a %{objdir}/System.map $RPM_BUILD_ROOT/boot/System.map-%{kernel_release}
install %{objdir}/vmlinux $RPM_BUILD_ROOT/boot/vmlinux-%{kernel_release}
%ifarch %{ix86} %{x8664}
cp -a %{objdir}/arch/%{target_arch_dir}/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%endif
%ifarch ppc ppc64
install %{objdir}/vmlinux $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%endif
%ifarch alpha sparc sparc64
	%{__gzip} -cfv %{objdir}/vmlinux > %{objdir}/vmlinuz
	cp -a %{objdir}/vmlinuz $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%ifarch sparc
	elftoaout %{objdir}/arch/sparc/boot/image -o %{objdir}/vmlinux.aout
	install %{objdir}/vmlinux.aout $RPM_BUILD_ROOT/boot/vmlinux.aout-%{kernel_release}
%endif
%ifarch sparc64
	elftoaout %{objdir}/arch/sparc64/boot/image -o %{objdir}/vmlinux.aout
	install %{objdir}/vmlinux.aout $RPM_BUILD_ROOT/boot/vmlinux.aout-%{kernel_release}
%endif
%endif

# for initrd
touch $RPM_BUILD_ROOT/boot/initrd-%{kernel_release}.gz

%if "%{_target_base_arch}" != "%{_arch}"
touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/modules.dep
%endif

# /etc/modrobe.d
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{kernel_release}

# /usr/src/linux
# maybe package these to -module-build, then -headers could be noarch
cp -a %{objdir}/Module.symvers $RPM_BUILD_ROOT%{_kernelsrcdir}/Module.symvers-dist
cp -aL %{objdir}/.config $RPM_BUILD_ROOT%{_kernelsrcdir}/config-dist
cp -a %{objdir}/include/linux/autoconf.h $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/autoconf-dist.h
cp -a %{objdir}/include/linux/{utsrelease,version}.h $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux
%endif # arch dependant

%if %{with noarch}
# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al %{srcdir}/COPYING $RPM_BUILD_ROOT/COPYING 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/COPYING
fi
cp -a$l %{srcdir}/* $RPM_BUILD_ROOT%{_kernelsrcdir}

install -d $RPM_BUILD_ROOT/lib/modules/%{kernel_release}
cp -a %{SOURCE6} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/config.h
%endif # arch independant

# collect module-build files and directories
# Usage: kernel-module-build.pl $rpmdir $fileoutdir
fileoutdir=$(pwd)
cd $RPM_BUILD_ROOT%{_kernelsrcdir}
%{objdir}/scripts/kernel-module-build.pl %{_kernelsrcdir} $fileoutdir
cd -

%clean
rm -rf $RPM_BUILD_ROOT

%preun
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{kernel_release}
fi

%post
mv -f /boot/vmlinuz-%{alt_kernel} /boot/vmlinuz-%{alt_kernel}.old 2>/dev/null > /dev/null
mv -f /boot/System.map-%{alt_kernel} /boot/System.map-%{alt_kernel}.old 2>/dev/null > /dev/null
ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz-%{alt_kernel}
ln -sf System.map-%{kernel_release} /boot/System.map-%{alt_kernel}
if [ ! -e /boot/vmlinuz ]; then
	mv -f /boot/vmlinuz /boot/vmlinuz.old 2>/dev/null
	mv -f /boot/System.map /boot/System.map.old 2>/dev/null
	ln -sf vmlinuz-%{alt_kernel} /boot/vmlinuz
	ln -sf System.map-%{alt_kernel} /boot/System.map
	mv -f %{initrd_dir}/initrd %{initrd_dir}/initrd.old 2>/dev/null
	ln -sf initrd-%{alt_kernel} %{initrd_dir}/initrd
fi

%depmod %{kernel_release}

/sbin/geninitrd -f --initrdfs=initramfs %{?with_bootsplash:--with-bootsplash} %{?with_fbsplash:--with-fbsplash} %{initrd_dir}/initrd-%{kernel_release}.gz %{kernel_release}
mv -f %{initrd_dir}/initrd-%{alt_kernel} %{initrd_dir}/initrd-%{alt_kernel}.old 2>/dev/null
ln -sf initrd-%{kernel_release}.gz %{initrd_dir}/initrd-%{alt_kernel}

if [ -x /sbin/new-kernel-pkg ]; then
	if [ -f /etc/pld-release ]; then
		title=$(sed 's/^[0-9.]\+ //' < /etc/pld-release)
	else
		title='PLD Linux'
	fi

	title="$title %{alt_kernel}"

	/sbin/new-kernel-pkg --initrdfile=%{initrd_dir}/initrd-%{kernel_release}.gz --install %{kernel_release} --banner "$title"
elif [ -x /sbin/rc-boot ]; then
	/sbin/rc-boot 1>&2 || :
fi

%post vmlinux
mv -f /boot/vmlinux-%{alt_kernel} /boot/vmlinux-%{alt_kernel}.old 2>/dev/null
ln -sf vmlinux-%{kernel_release} /boot/vmlinux-%{alt_kernel}

%post drm
%depmod %{kernel_release}

%postun drm
%depmod %{kernel_release}

%post pcmcia
%depmod %{kernel_release}

%postun pcmcia
%depmod %{kernel_release}

%post sound-alsa
%depmod %{kernel_release}

%postun sound-alsa
%depmod %{kernel_release}

%post sound-oss
%depmod %{kernel_release}

%postun sound-oss
%depmod %{kernel_release}

%post headers
rm -f %{_prefix}/src/linux-%{alt_kernel}
ln -snf %{basename:%{_kernelsrcdir}} %{_prefix}/src/linux-%{alt_kernel}

%postun headers
if [ "$1" = "0" ]; then
	if [ -L %{_prefix}/src/linux-%{alt_kernel} ]; then
		if [ "$(readlink %{_prefix}/src/linux-%{alt_kernel})" = "linux-%{version}_%{alt_kernel}" ]; then
			rm -f %{_prefix}/src/linux-%{alt_kernel}
		fi
	fi
fi

%triggerin module-build -- %{name} = %{epoch}:%{version}-%{release}
ln -sfn %{_kernelsrcdir} /lib/modules/%{kernel_release}/build
ln -sfn %{_kernelsrcdir} /lib/modules/%{kernel_release}/source

%triggerun module-build -- %{name} = %{epoch}:%{version}-%{release}
if [ "$1" = 0 ]; then
	rm -f /lib/modules/%{kernel_release}/{build,source}
fi

%if %{without noarch}
%files
%defattr(644,root,root,755)
/boot/vmlinuz-%{kernel_release}
/boot/System.map-%{kernel_release}
%ghost /boot/initrd-%{kernel_release}.gz
%dir /lib/modules/%{kernel_release}
%dir /lib/modules/%{kernel_release}/kernel
/lib/modules/%{kernel_release}/kernel/arch
/lib/modules/%{kernel_release}/kernel/crypto
/lib/modules/%{kernel_release}/kernel/drivers
%exclude /lib/modules/%{kernel_release}/kernel/drivers/char/drm
/lib/modules/%{kernel_release}/kernel/fs
/lib/modules/%{kernel_release}/kernel/kernel
/lib/modules/%{kernel_release}/kernel/lib
/lib/modules/%{kernel_release}/kernel/net
%dir /lib/modules/%{kernel_release}/kernel/sound
/lib/modules/%{kernel_release}/kernel/sound/soundcore.*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/media/video/*/*-alsa.ko*
%dir /lib/modules/%{kernel_release}/misc
%exclude /lib/modules/%{kernel_release}/kernel/drivers/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
%exclude /lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
%exclude /lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
%ghost /lib/modules/%{kernel_release}/modules.*
%ghost /lib/modules/%{kernel_release}/build
%ghost /lib/modules/%{kernel_release}/source
%dir %{_sysconfdir}/modprobe.d/%{kernel_release}

%ifarch alpha %{ix86} %{x8664} ppc ppc64 sparc sparc64
%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{kernel_release}
%endif

%files drm
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/drivers/char/drm

%files pcmcia
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/drivers/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/*/pcmcia
/lib/modules/%{kernel_release}/kernel/drivers/bluetooth/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/ide/legacy/ide-cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/isdn/hardware/avm/avm_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/*_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/net/wireless/hostap/hostap_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/parport/parport_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/serial/serial_cs.ko*
/lib/modules/%{kernel_release}/kernel/drivers/telephony/ixj_pcmcia.ko*
/lib/modules/%{kernel_release}/kernel/drivers/usb/host/sl811_cs.ko*
/lib/modules/%{kernel_release}/kernel/sound/pcmcia

%files sound-alsa
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound
/lib/modules/%{kernel_release}/kernel/drivers/media/video/*/*-alsa.ko*
%exclude %dir /lib/modules/%{kernel_release}/kernel/sound
%exclude /lib/modules/%{kernel_release}/kernel/sound/soundcore.*
%exclude /lib/modules/%{kernel_release}/kernel/sound/oss
%exclude /lib/modules/%{kernel_release}/kernel/sound/pcmcia

%files sound-oss
%defattr(644,root,root,755)
/lib/modules/%{kernel_release}/kernel/sound/oss

%files config
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/config-dist
%{_kernelsrcdir}/Module.symvers-dist
%dir %{_kernelsrcdir}/include
%dir %{_kernelsrcdir}/include/linux
%{_kernelsrcdir}/include/linux/autoconf-dist.h
%{_kernelsrcdir}/include/linux/utsrelease.h
%{_kernelsrcdir}/include/linux/version.h
%endif # noarch package

%if %{with noarch}
%files headers
%defattr(644,root,root,755)
%{_kernelsrcdir}/include/*
%exclude %dir %{_kernelsrcdir}/include/linux
%exclude %{_kernelsrcdir}/include/linux/autoconf-dist.h
%exclude %{_kernelsrcdir}/include/linux/utsrelease.h
%exclude %{_kernelsrcdir}/include/linux/version.h

%files module-build -f aux_files
%defattr(644,root,root,755)
%{_kernelsrcdir}/Kbuild
%{_kernelsrcdir}/arch/*/kernel/asm-offsets*.c
%{_kernelsrcdir}/arch/*/kernel/sigframe.h
%{_kernelsrcdir}/arch/*/kernel/sigframe_32.h
%dir %{_kernelsrcdir}/scripts
%dir %{_kernelsrcdir}/scripts/kconfig
%{_kernelsrcdir}/scripts/Kbuild.include
%{_kernelsrcdir}/scripts/Makefile*
%{_kernelsrcdir}/scripts/basic
%{_kernelsrcdir}/scripts/mkmakefile
%{_kernelsrcdir}/scripts/mod
%{_kernelsrcdir}/scripts/setlocalversion
%{_kernelsrcdir}/scripts/*.c
%{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/scripts/kconfig/*

%files doc
%defattr(644,root,root,755)
%{_kernelsrcdir}/Documentation

%if %{with source}
%files source -f aux_files_exc
%defattr(644,root,root,755)
%{_kernelsrcdir}/arch/*/[!Mk]*
%{_kernelsrcdir}/arch/*/kernel/[!M]*
%exclude %{_kernelsrcdir}/arch/*/kernel/asm-offsets*.c
%exclude %{_kernelsrcdir}/arch/*/kernel/sigframe.h
%{_kernelsrcdir}/block
%{_kernelsrcdir}/crypto
%{_kernelsrcdir}/drivers
%{_kernelsrcdir}/fs
%if %{with grsec_minimal}
%{_kernelsrcdir}/grsecurity
%endif
%{_kernelsrcdir}/init
%{_kernelsrcdir}/ipc
%{_kernelsrcdir}/kernel
%{_kernelsrcdir}/lib
%{_kernelsrcdir}/mm
%{_kernelsrcdir}/net
%{_kernelsrcdir}/scripts/*
%exclude %{_kernelsrcdir}/scripts/Kbuild.include
%exclude %{_kernelsrcdir}/scripts/Makefile*
%exclude %{_kernelsrcdir}/scripts/basic
%exclude %{_kernelsrcdir}/scripts/kconfig
%exclude %{_kernelsrcdir}/scripts/mkmakefile
%exclude %{_kernelsrcdir}/scripts/mod
%exclude %{_kernelsrcdir}/scripts/setlocalversion
%exclude %{_kernelsrcdir}/scripts/*.c
%exclude %{_kernelsrcdir}/scripts/*.sh
%{_kernelsrcdir}/sound
%{_kernelsrcdir}/security
%{_kernelsrcdir}/usr
%{_kernelsrcdir}/COPYING
%{_kernelsrcdir}/CREDITS
%{_kernelsrcdir}/MAINTAINERS
%{_kernelsrcdir}/README
%{_kernelsrcdir}/REPORTING-BUGS
%endif
%endif

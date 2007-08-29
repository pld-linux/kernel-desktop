#
# TODO:
# - OOPSES AFTER FIREWALL LOAD
# - investigate rejected sk98lin patch
# - dmi-decode patch already in upstream kernel?
# - investigate hdaps_protect -- doesn't apply
# - check patches > 90
# - put together a default .config that makes sense for desktops
# - convert patches to common diff -uNp format
# - make sure patch numbering is consistent and preapare it
#   for the future
# - investigate ppc-ICE patches from kernel.spec (does it fix the e1000 ICE?)
# - investigate pwc-uncompress patch from kernel.spec
# - investigate apparmor-caps patch from kernel.spec
# - actively search for other superb enhancing patches 
#   (even the experimental ones, as kernel-desktop is not 
#   mainline kernel)
# - check if we don't have newer netfilter (kernel.spec claims 2007)
# - check for all patches update
# - links and descriptions above al PatchesXXX and %patchXXX
# - update common config for unionfs and PF_RING
# - disable vserver
#
# Conditional build:
%bcond_without	source		# don't build kernel-source package

%bcond_with	preemptrt	# use realtime-preempt patch
%bcond_without	ck		# don't use Con Kolivas patchset
%bcond_with	grsec_minimal	# don't build grsecurity (minimal subset: proc,link,fifo,shm)
%bcond_with	bootsplash	# build with bootsplash instead of fbsplash
%bcond_with	laptop		# build with HZ=100
%bcond_with	verbose		# verbose build (V=1)
%bcond_with	pae		# build PAE (HIGHMEM64G) support on uniprocessor

%{?debug:%define with_verbose 1}

%ifnarch %{ix86}
%undefine	with_pae
%endif

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


%define		_netfilter_snap		20061213
%define		_nf_hipac_ver		0.9.1

%define		_enable_debug_packages			0
%define		no_install_post_strip			1
%define		no_install_post_chrpath			1

%define		pcmcia_version		3.1.22
%define		drm_xfree_version	4.3.0

%define		squashfs_version	3.2-r2
%define		suspend_version		2.2.10.2
%define		suspend_kernel		%{_basever}-rc6

%if %{with laptop}
%define		alt_kernel	laptop%{?with_preemptrt:_rt}
%else
%define		alt_kernel	desktop%{?with_preemptrt:_rt}
%endif

%define		_basever	2.6.22
%define		_postver	.5
%define		_rel		0.6
%define		_rc	%{nil}
Summary:	The Linux kernel (the core of the Linux operating system)
Summary(de.UTF-8):	Der Linux-Kernel (Kern des Linux-Betriebssystems)
Summary(fr.UTF-8):	Le Kernel-Linux (La partie centrale du systeme)
Summary(pl.UTF-8):	Jądro Linuksa
Name:		kernel-%{alt_kernel}
Version:	%{_basever}%{_postver}
Release:	%{_rel}
Epoch:		3
License:	GPL v2
Group:		Base/Kernel
#define		_rc	-rc6
#Source0:	ftp://ftp.kernel.org/pub/linux/kernel/v2.6/testing/linux-%{_basever}%{_rc}.tar.bz2
Source0:	http://www.kernel.org/pub/linux/kernel/v2.6/linux-%{_basever}.tar.bz2
# Source0-md5:	2e230d005c002fb3d38a3ca07c0200d0
%if "%{_postver}" != "%{nil}"
Source1:	http://www.kernel.org/pub/linux/kernel/v2.6/patch-%{version}.bz2
# Source1-md5:	27544a58763bbd4ce497a77658af744a
%endif
Source2:	http://www.tuxonice.net/downloads/all/suspend2-%{suspend_version}-for-%{suspend_kernel}.patch.bz2
# Source2-md5:	f98f071b0f4e7897296d643854bb809f

Source3:	kernel-desktop-autoconf.h
Source4:	kernel-desktop-config.h
Source5:	kernel-desktop-module-build.pl

Source20:	kernel-desktop-common.config
Source22:	kernel-desktop-i386.config
Source24:	kernel-desktop-x86_64.config
Source26:	kernel-desktop-ppc.config

Source41:	kernel-desktop-preempt-rt.config
Source42:	kernel-desktop-preempt-nort.config
Source43:	kernel-desktop-suspend2.config
Source44:	kernel-desktop-patches.config
Source45:	kernel-desktop-netfilter.config
Source46:	kernel-desktop-grsec.config
Source47:	kernel-desktop-wrr.config
Source48:	kernel-desktop-fbsplash.config
Source49:	kernel-desktop-bootsplash.config

###
#	Patches
###

Patch0:		kernel-desktop-preempt-rt.patch

# Jens Axboe's fcache patch (for ext3 only)
# http://git.kernel.dk/?p=linux-2.6-block.git;a=commitdiff;h=118e3e9250ef319b6e77cdbc25dc4d26084c14f
# http://en.opensuse.org/Fcache-howto
Patch6:		kernel-desktop-fcache.patch

### Con Kolivas patchset
Patch7:		kernel-desktop-ck.patch

Patch9:		kernel-desktop-grsec-minimal.patch

### filesystems
# based on ftp://ftp.namesys.com/pub/reiser4-for-2.6/2.6.22/reiser4-for-2.6.22-2.patch.gz
Patch10:	kernel-desktop-reiser4.patch
# Squashfs from squashfs: http://dl.sourceforge.net/sourceforge/squashfs/squashfs3.2-r2.tar.gz for linux-2.6.20
Patch11:	kernel-desktop-squashfs.patch
# http://dl.sourceforge.net/sourceforge/supermount-ng/supermount-ng-2.2.2-2.6.22.1_madgus_gcc34.patch.gz
Patch12:	kernel-desktop-supermount-ng.patch
# http://download.filesystems.org/unionfs/unionfs-2.1/unionfs-2.1.2_for_2.6.22.4.diff.gz
Patch13:	kernel-desktop-unionfs.patch
# http://client.linux-nfs.org/Linux-2.6.x/2.6.22/linux-2.6.22-NFS_ALL.dif
Patch14:	kernel-desktop-NFS_ALL.patch
# http://www.citi.umich.edu/projects/nfsv4/linux/kernel-patches/2.6.22-rc5-1/linux-2.6.22-rc5-CITI_NFS4_ALL-1.diff
Patch15:	kernel-desktop-CITI_NFS4_ALL.patch

### hardware
# tahoe9XX http://tahoe.pl/drivers/tahoe9xx-2.6.11.5.patch
Patch20:	kernel-desktop-tahoe9xx.patch
# Derived from http://www.skd.de/e_en/products/adapters/pci_64/sk-98xx_v20/software/linux/driver/install-8_41.tar.bz2
Patch21:	kernel-desktop-sk98lin.patch
# http://dev.gentoo.org/~spock/projects/vesafb-tng/archive/vesafb-tng-1.0-rc2-2.6.20-rc2.patch
Patch22:	kernel-desktop-vesafb-tng.patch
Patch23:	kernel-desktop-dmi-decode-and-save-oem-string-information.patch
# from http://www.zen24593.zen.co.uk/hdaps/hdaps_protect-2.6.18.3-2.patch
Patch24:	kernel-desktop-hdaps_protect.patch
# http://pred.dcaf-security.org/sata_nv-ncq-support-mcp51-mcp55-mcp61.patch
# NCQ Functionality for newer nvidia chipsets (MCP{51,55,61}) by nvidia crew
Patch25:	kernel-desktop-sata_nv-ncq.patch
# http://memebeam.org/free-software/toshiba_acpi/toshiba_acpi-dev_toshiba_test5-linux_2.6.21.patch
Patch26:	kernel-desktop-toshiba-acpi.patch

### console
# ftp://ftp.openbios.org/pub/bootsplash/kernel/bootsplash-3.1.6-2.6.21.diff.gz
Patch30:	kernel-desktop-bootsplash.patch
# http://dev.gentoo.org/~spock/projects/gensplash/archive/fbsplash-0.9.2-r5-2.6.20-rc6.patch
Patch31:	kernel-desktop-fbsplash.patch

########	netfilter snap
## base
Patch40:	kernel-desktop-pom-ng-IPV4OPTSSTRIP.patch
Patch41:	kernel-desktop-pom-ng-ipv4options.patch
Patch42:	kernel-desktop-pom-ng-set.patch
Patch43:	kernel-desktop-pom-ng-u32.patch
Patch44:	kernel-desktop-pom-ng-ROUTE.patch
Patch45:	kernel-desktop-pom-ng-TARPIT.patch
Patch46:	kernel-desktop-pom-ng-mms-conntrack-nat.patch
Patch47:	kernel-desktop-pom-ng-IPMARK.patch
Patch48:	kernel-desktop-pom-ng-connlimit.patch
Patch49:	kernel-desktop-pom-ng-geoip.patch
Patch50:	kernel-desktop-pom-ng-ipp2p.patch
Patch51:	kernel-desktop-pom-ng-time.patch
Patch52:	kernel-desktop-pom-ng-rsh.patch
Patch53:	kernel-desktop-pom-ng-rpc.patch

# based on http://www.svn.barbara.eu.org/ipt_account/attachment/wiki/Software/ipt_account-0.1.21-20070804164729.tar.gz?format=raw
Patch67:	kernel-desktop-ipt_account.patch

# based on http://www.intra2net.com/de/produkte/opensource/ipt_account/pom-ng-ipt_ACCOUNT-1.10.tgz
Patch68:	kernel-desktop-ipt_ACCOUNT.patch

# netfilter-layer7-v2.13.tar.gz from http://l7-filter.sf.net/
Patch69:	kernel-desktop-layer7.patch
########	End netfilter

### net software
# based on 2.6.17 patch from http://www.linuximq.net/patchs/linux-2.6.17-imq1.diff,
# some stuff moved from net/sched/sch_generic.c to net/core/dev.c for 2.6.19
# compatibility. Should work, but not with wrr.
Patch70:	kernel-desktop-imq.patch
# esfq from http://fatooh.org/esfq-2.6/current/esfq-kernel.patch
Patch71:	kernel-desktop-esfq.patch
# derived from ftp://ftp.cmf.nrl.navy.mil/pub/chas/linux-atm/vbr/vbr-kernel-diffs
Patch72:	kernel-desktop-atm-vbr.patch
Patch73:	kernel-desktop-atmdd.patch
# wrr http://www.zz9.dk/patches/wrr-linux-070717-2.6.22.patch.gz
Patch74:	kernel-desktop-wrr.patch
# adds some ids for hostap suported cards and monitor_enable from/for aircrack-ng
# http://patches.aircrack-ng.org/hostap-kernel-2.6.18.patch
Patch75:	kernel-desktop-hostap.patch
# http://www.ntop.org/PF_RING.html 20070610
Patch76:	kernel-desktop-PF_RING.patch
# The following patch extend the routing functionality in Linux 
# to support static routes (defined by user), new way to use the 
# alternative routes, the reverse path protection (rp_filter), 
# the NAT processing to use correctly the routing when multiple 
# gateways are used.
# http://www.ssi.bg/~ja/routes-2.6.22-15.diff
# We need to disable CONFIG_IP_ROUTE_MULTIPATH_CACHED
Patch77:	kernel-desktop-routes.patch

### Additional features
# http://www.bullopensource.org/cpuset/ - virtual CPUs
Patch85:	kernel-desktop-cpuset_virtualization.patch

### Fixes
Patch91:	kernel-desktop-fbcon-margins.patch
Patch92:	kernel-desktop-static-dev.patch
Patch100:	kernel-desktop-small_fixes.patch
Patch101:	kernel-bcm43xx-pcie-2.6_18.1.patch
# Wake-On-Lan fix for nForce drivers; using http://atlas.et.tudelft.nl/verwei90/nforce2/wol.html
# Fix verified for that kernel version.
# Wake-On-Lan fix for nForce drivers; using http://atlas.et.tudelft.nl/verwei90/nforce2/wol.html
# Fix verified for that kernel version.
Patch102:	kernel-desktop-forcedeth-WON.patch
Patch103:	kernel-desktop-ueagle-atm-freezer.patch
# investigate
Patch104:	kernel-desktop-ppc-ICE-hacks.patch

URL:		http://www.kernel.org/
BuildRequires:	binutils >= 3:2.14.90.0.7
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
Conflicts:	udev < %{_udev_ver}
Conflicts:	util-linux < %{_util_linux_ver}
Conflicts:	xfsprogs < %{_xfsprogs_ver}
ExclusiveArch:	%{ix86} %{x8664} ppc
ExclusiveOS:	Linux
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

# No ELF objects there to strip (skips processing 27k files)
%define		_noautostrip	.*%{_kernelsrcdir}/.*

%define		initrd_dir	/boot

# kernel release (used in filesystem and eventually in uname -r)
# modules will be looked from /lib/modules/%{kernel_release}
# _localversion is just that without version for "> localversion"
%define		_localversion %{release}
%define		kernel_release %{version}_%{alt_kernel}-%{_localversion}
%define		_kernelsrcdir	/usr/src/linux-%{version}_%{alt_kernel}

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

%define __features Enabled features:\
%{?debug: - DEBUG}\
 - suspend2 %{suspend_version}\
%{?with_preemptrt: - realtime-preempt patch by Ingo Molar}\
%{?with_ck: - desktop patchset by Con Kolivas}\
%{?with_grsec_minimal: - grsecurity minimal}\
 - %{?with_bootsplash:bootsplash}%{!?with_bootsplash:fbsplash}\
%{?with_smp: - Multi Processor support}\
%{!?with_smp:%{?with_pae: - PAE (HIGHMEM64G) support}}\
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
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
Provides:	kernel-drm = %{drm_xfree_version}
Autoreqprov:	no

%description drm
DRM kernel modules (%{drm_xfree_version}).

%description drm -l de.UTF-8
DRM Kernel Treiber (%{drm_xfree_version}).

%description drm -l pl.UTF-8
Sterowniki DRM (%{drm_xfree_version}).

%package pcmcia
Summary:	PCMCIA modules
Summary(de.UTF-8):	PCMCIA Module
Summary(pl.UTF-8):	Moduły PCMCIA
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

%description pcmcia -l de.UTF-8
PCMCIA Module (%{pcmcia_version})

%description pcmcia -l pl.UTF-8
Moduły PCMCIA (%{pcmcia_version}).

%package sound-alsa
Summary:	ALSA kernel modules
Summary(de.UTF-8):	ALSA Kernel Module
Summary(pl.UTF-8):	Sterowniki dźwięku ALSA
Group:		Base/Kernel
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
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
Requires(postun):	%{name}-up = %{epoch}:%{version}-%{release}
Requires:	%{name}-up = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description sound-oss
OSS (Open Sound System) drivers.

%description sound-oss -l de.UTF-8
OSS (Open Sound System) Treiber.

%description sound-oss -l pl.UTF-8
Sterowniki dźwięku OSS (Open Sound System).

%package headers
Summary:	Header files for the Linux kernel
Summary(de.UTF-8):	Header Dateien für den Linux-Kernel
Summary(pl.UTF-8):	Pliki nagłówkowe jądra Linuksa
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

%description headers -l de.UTF-8
Dies sind die C Header Dateien für den Linux-Kernel, die definierte
Strukturen und Konstante beinhalten die beim rekompilieren des Kernels
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
Provides:	kernel-module-build = %{epoch}:%{version}-%{release}
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
Provides:	kernel-source = %{epoch}:%{version}-%{release}
Autoreqprov:	no

%description source
This is the source code for the Linux kernel. You can build a custom kernel
that is better tuned to your particular hardware.

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
Provides:	kernel-doc = %{version}
Autoreqprov:	no

%description doc
This is the documentation for the Linux kernel, as found in
Documentation directory.

%description doc -l de.UTF-8
Dies ist die Kernel Dokumentation wie sie im 'Documentation'
Verzeichniss vorgefunden werden kann.

%description doc -l pl.UTF-8
Pakiet zawiera dokumentację do jądra Linuksa pochodzącą z katalogu
Documentation.

%prep
%setup -q -n linux-%{_basever}%{_rc}

%if "%{_postver}" != "%{nil}"
%{__bzip2} -dc %{SOURCE1} | %{__patch} -p1 -s
%endif

# suspend 2
%{__bzip2} -dc %{SOURCE2} | %{__patch} -p1 -s

%if %{with preemptrt}
#%patch0 -p1
: premptrt patch is not ready yet
exit 1
%endif

# Jens Axboe's fcache patch
%patch6 -p1

# Con Kolivas patchset
%if %{with ck}
%patch7 -p1
%endif

# grsecurity
%if %{with grsec_minimal}
%patch9 -p1
%endif

# filesystems
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1

### hardware
%patch20 -p1
# Rejects hard -- neds further investigation
#%%patch21 -p1
%patch22 -p1
# Already applied?
#%%patch23 -p1
#%%patch24 -p1
%patch25 -p1
# toshiba-acpi
%patch26 -p1

### console
%if %{with bootsplash}
%patch30 -p1
%else
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
%patch70 -p1
%patch71 -p1
%patch72 -p1
%patch73 -p1
%patch74 -p1
# hostap enhancements from/for aircrack-ng
%patch75 -p1
# PF_RING
%patch76 -p1
# static routes
%patch77 -p1

#%%patch80 -p1	NEEDS a lot of work

### fixes
%patch91 -p1
%patch92 -p1
%patch100 -p1
#%%patch101 -p1
# forcedeth
%patch102 -p1
# ueagle freezer
%patch103 -p1
# ppc ICE fixes
%ifarch ppc ppc64
%patch104 -p1
%endif

# Fix EXTRAVERSION in main Makefile
sed -i 's#EXTRAVERSION =.*#EXTRAVERSION = %{_postver}_%{alt_kernel}#g' Makefile

sed -i -e '/select INPUT/d' net/bluetooth/hidp/Kconfig

%build
KERNEL_BUILD_DIR=`pwd`

Config="%{_target_base_arch}"

cat %{SOURCE20} > .config
cat $RPM_SOURCE_DIR/kernel-desktop-$Config.config >> .config
echo "CONFIG_LOCALVERSION=\"-%{_localversion}\"" >> .config

%ifarch %{ix86}
	%ifnarch i386
	sed -i 's:CONFIG_M386=y:# CONFIG_M386 is not set:' .config
	%endif
	%ifarch i486
	sed -i 's:# CONFIG_M486 is not set:CONFIG_M486=y:' .config
	%endif
	%ifarch i586
	sed -i 's:# CONFIG_M586 is not set:CONFIG_M586=y:' .config
	%endif
	%ifarch i686
	sed -i 's:# CONFIG_M686 is not set:CONFIG_M686=y:' .config
	%endif
	%ifarch pentium3
	sed -i 's:# CONFIG_MPENTIUMIII is not set:CONFIG_MPENTIUMIII=y:' .config
	%endif
	%ifarch pentium4
	sed -i 's:# CONFIG_MPENTIUM4 is not set:CONFIG_MPENTIUM4=y:' .config
	%endif
	%ifarch athlon
	sed -i 's:# CONFIG_MK7 is not set:CONFIG_MK7=y:' .config
	%endif
	%ifarch i686 athlon pentium3 pentium4
	sed -i "s:CONFIG_HIGHMEM4G=y:# CONFIG_HIGHMEM4G is not set:" .config
	sed -i "s:# CONFIG_HIGHMEM64G is not set:CONFIG_HIGHMEM64G=y\nCONFIG_X86_PAE=y:" .config
	sed -i 's:CONFIG_MATH_EMULATION=y:# CONFIG_MATH_EMULATION is not set:' .config
	%endif
%endif

# preempt
%if %{with preemptrt}
	cat %{SOURCE41} >> .config
%else
	cat %{SOURCE42} >> .config
%endif


# suspend 2
cat %{SOURCE43} >> .config

# fbsplash, vesafb-tng, squashfs, imq, tahoe, atm, reiser4
cat %{SOURCE44} >> .config

# netfilter
cat %{SOURCE45} >> .config

%if %{with grsec_minimal}
	cat %{SOURCE46} >> .config
%endif

# wrr
cat %{SOURCE47} >> .config

%ifarch %{ix86}
%ifnarch i386
	sed -e "s:CONFIG_NO_HZ=y:# CONFIG_NO_HZ is not set:" \
		-e "s:# CONFIG_HZ_1000 is not set:CONFIG_HZ_1000=y:" \
		-e "s:# CONFIG_HZ is not set:CONFIG_HZ=1000:"			\
		-i .config
%endif
%endif

%if %{with laptop}
	sed -e "s:CONFIG_HZ_1000=y:# CONFIG_HZ_1000 is not set:"	\
		-e "s:# CONFIG_HZ_100 is not set:CONFIG_HZ_100=y:"	\
		-e "s:CONFIG_HZ=1000:CONFIG_HZ=100:"			\
		-i .config
%endif

%if %{with bootsplash}
	cat %{SOURCE49} >> .config
%else
	cat %{SOURCE48} >> .config
%endif

%{?debug:sed -i "s:# CONFIG_DEBUG_SLAB is not set:CONFIG_DEBUG_SLAB=y:" .config}
%{?debug:sed -i "s:# CONFIG_DEBUG_PREEMPT is not set:CONFIG_DEBUG_PREEMPT=y:" .config}
%{?debug:sed -i "s:# CONFIG_RT_DEADLOCK_DETECT is not set:CONFIG_RT_DEADLOCK_DETECT=y:" .config}

# disable e1000 on ppc (ICEs)
%ifarch ppc ppc64
	sed -e "s:CONFIG_E1000=m:# CONFIG_E1000 is not set:" \
		-e "s:CONFIG_E1000_NAPI=y:# CONFIG_E1000_NAPI is not set:" \
		-e "s:CONFIG_E1000_DISABLE_PACKET_SPLIT=y:# CONFIG_E1000_DISABLE_PACKET_SPLIT is not set:" \
		-i .config
%endif

rm -f include/linux/autoconf.h
%{__make} %{MakeOpts} silentoldconfig
install .config arch/%{_target_base_arch}/defconfig

# Build kernel
%{__make} %{MakeOpts} \
	%{?with_verbose:V=1}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{/boot,%{_kernelsrcdir}}

umask 022
l=
# test if we can hardlink -- %{_builddir} and $RPM_BUILD_ROOT on same partition
if cp -al COPYING $RPM_BUILD_ROOT/COPYING 2>/dev/null; then
	l=l
	rm -f $RPM_BUILD_ROOT/COPYING
fi


install -d $RPM_BUILD_ROOT%{_kernelsrcdir}
install -d $RPM_BUILD_ROOT%{_sysconfdir}/modprobe.d/%{kernel_release}

KERNEL_BUILD_DIR=$(pwd)


# Install modules

install System.map $RPM_BUILD_ROOT/boot/System.map-%{kernel_release}
%ifarch %{ix86} %{x8664}
	install arch/%{_target_base_arch}/boot/bzImage $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%endif

%ifarch ppc
	install vmlinux $RPM_BUILD_ROOT/boot/vmlinuz-%{kernel_release}
%endif
	install vmlinux $RPM_BUILD_ROOT/boot/vmlinux-%{kernel_release}

#export DEPMOD=%{DepMod}
%{__make} %{MakeOpts} modules_install \
	%{?with_verbose:V=1} \
	DEPMOD=%{DepMod} \
	INSTALL_MOD_PATH=$RPM_BUILD_ROOT \
	KERNELRELEASE=%{kernel_release}

%if "%{_target_base_arch}" != "%{_arch}"
	touch $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/modules.dep
%else
	echo "CHECKING DEPENDENCIES FOR KERNEL MODULES"
	/sbin/depmod --basedir $RPM_BUILD_ROOT -ae \
		-F $RPM_BUILD_ROOT/boot/System.map-%{kernel_release} -r %{kernel_release} \
		&& echo "OK" || echo "FAILED"
%endif


rm -f $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/build
ln -sf %{_kernelsrcdir} $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/build
install -d $RPM_BUILD_ROOT/lib/modules/%{kernel_release}/{cluster,misc}

find . -maxdepth 1 -name "." -exec cp -a$l "{}" "$RPM_BUILD_ROOT%{_kernelsrcdir}/" ";"

install Module.symvers \
	$RPM_BUILD_ROOT%{_kernelsrcdir}/Module.symvers-dist
install include/linux/autoconf.h \
	$RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/autoconf-dist.h
install .config \
	$RPM_BUILD_ROOT%{_kernelsrcdir}/config-dist

cd $RPM_BUILD_ROOT%{_kernelsrcdir}

%{__make} %{MakeOpts} mrproper

find '(' -name '*~' -o -name '*.orig' ')' -print0 | xargs -0 -r -l512 rm -f

install $KERNEL_BUILD_DIR/include/linux/{version.h,utsrelease.h} include/linux
install %{SOURCE3} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/autoconf.h
install %{SOURCE4} $RPM_BUILD_ROOT%{_kernelsrcdir}/include/linux/config.h

# collect module-build files and directories
%{__perl} %{SOURCE5} %{_kernelsrcdir} $KERNEL_BUILD_DIR

# ghosted initrd
touch $RPM_BUILD_ROOT/boot/initrd-%{kernel_release}.gz

%clean
rm -rf $RPM_BUILD_ROOT

%preun
rm -f /lib/modules/%{kernel_release}/modules.*
if [ -x /sbin/new-kernel-pkg ]; then
	/sbin/new-kernel-pkg --remove %{kernel_release}
fi

%post
mv -f /boot/vmlinuz-%{alt_kernel} /boot/vmlinuz-%{alt_kernel}.old 2> /dev/null > /dev/null
mv -f /boot/System.map-%{alt_kernel} /boot/System.map-%{alt_kernel}.old 2> /dev/null > /dev/null
ln -sf vmlinuz-%{kernel_release} /boot/vmlinuz-%{alt_kernel}
ln -sf System.map-%{kernel_release} /boot/System.map-%{alt_kernel}
if [ ! -e /boot/vmlinuz ]; then
	mv -f /boot/vmlinuz /boot/vmlinuz.old 2> /dev/null > /dev/null
	mv -f /boot/System.map /boot/System.map.old 2> /dev/null > /dev/null
	ln -sf vmlinuz-%{alt_kernel} /boot/vmlinuz
	ln -sf System.map-%{alt_kernel} /boot/System.map
	mv -f %{initrd_dir}/initrd %{initrd_dir}/initrd.old 2> /dev/null > /dev/null
	ln -sf initrd-%{alt_kernel} %{initrd_dir}/initrd
fi

%depmod %{kernel_release}

/sbin/geninitrd -f --initrdfs=rom %{initrd_dir}/initrd-%{kernel_release}.gz %{kernel_release}
mv -f %{initrd_dir}/initrd-%{alt_kernel} %{initrd_dir}/initrd-%{alt_kernel}.old 2> /dev/null > /dev/null
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
mv -f /boot/vmlinux-%{alt_kernel} /boot/vmlinux-%{alt_kernel}.old 2> /dev/null > /dev/null
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
/lib/modules/%{kernel_release}/kernel/security
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
/lib/modules/%{kernel_release}/build
%ghost /lib/modules/%{kernel_release}/modules.*
%dir %{_sysconfdir}/modprobe.d/%{kernel_release}

%files vmlinux
%defattr(644,root,root,755)
/boot/vmlinux-%{kernel_release}

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

%files headers
%defattr(644,root,root,755)
%dir %{_kernelsrcdir}
%{_kernelsrcdir}/include
%{_kernelsrcdir}/config-dist
%{_kernelsrcdir}/Module.symvers-dist

%files module-build -f aux_files
%defattr(644,root,root,755)
%{_kernelsrcdir}/Kbuild
%{_kernelsrcdir}/arch/*/kernel/asm-offsets.*
%{_kernelsrcdir}/arch/*/kernel/sigframe.h
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
%exclude %{_kernelsrcdir}/arch/*/kernel/asm-offsets.*
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

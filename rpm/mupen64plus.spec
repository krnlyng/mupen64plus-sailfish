Name:		mupen64plus
Version:	2.0
Release:	1%{?dist}
Summary:	Nintendo 64 Emulator

Group:		Emulators
License:	GPLv2
URL:		http://code.google.com/p/mupen64plus
Source0:	%{name}-%{version}.tar.bz2

BuildRequires:  wayland-devel
BuildRequires:  git
BuildRequires:	bash
BuildRequires:	gcc-c++
BuildRequires:  cmake
BuildRequires:  freetype-devel
BuildRequires:  zlib-devel
BuildRequires:	boost-devel
BuildRequires:	pkgconfig(libpng)
BuildRequires:	pkgconfig(egl)
BuildRequires:	pkgconfig(glesv2)
BuildRequires:	pkgconfig(sdl2)
BuildRequires:	pkgconfig(zlib)
BuildRequires:  pkgconfig(audioresource)
BuildRequires:  pkgconfig(glib-2.0)

%description
Mupen64plus is a cross-platform plugin based N64 emulator
which is capable of accurately playing many games.

%prep
%setup -q

%build
cd mupen64plus-audio-sdl
PREFIX=%{_prefix} OPTFLAGS="-O3 -flto" V=1 make all -C projects/unix
cd ..
cd mupen64plus-core
PREFIX=%{_prefix} OPTFLAGS="-O3 -flto" USE_GLES=1 OSD=0 NEON=1 make all -C projects/unix
cd ..
cd mupen64plus-input-sdl
PREFIX=%{_prefix} OPTFLAGS="-O3 -flto" make all -C projects/unix
cd ..
cd mupen64plus-input-sdltouch
PREFIX=%{_prefix} OPTFLAGS="-O3" make all -C projects/unix
cd ..
cd mupen64plus-video-gles2n64-1
USE_GLES=1 PREFIX=%{_prefix} OPTFLAGS="-O3" make all -C projects/unix
cd ..
cd mupen64plus-rsp-hle
PREFIX=%{_prefix} OPTFLAGS="-O3" make all -C projects/unix
cd ..
cd mupen64plus-ui-console
PREFIX=%{_prefix} OPTFLAGS="-O3" make all -C projects/unix
cd ..
cd mupen64plus-video-glide64mk2
%ifarch %{arm}
PREFIX=%{_prefix} OPTFLAGS="-O3" NO_SSE=1 USE_GLES=1 make all -C projects/unix
%endif
%ifarch %{ix86}
PREFIX=%{_prefix} OPTFLAGS="-O3" USE_GLES=1 make all -C projects/unix
%endif
cd ..
cd mupen64plus-video-rice
%ifarch %{arm}
PREFIX=%{_prefix} OPTFLAGS="-O2" NO_ASM=1 USE_GLES=1 make all -C projects/unix
%endif
%ifarch %{ix86}
PREFIX=%{_prefix} OPTFLAGS="-O2" USE_GLES=1 make all -C projects/unix
%endif
cd ..
mkdir GLideN64/src/build
cd GLideN64/src
./getRevision.sh
cd ../..
cd GLideN64/src/build
%ifarch %{arm}
cmake -DMUPENPLUSAPI=On -DGLES2=On -DNEON_OPT=1 ..
%endif
%ifarch %{ix86}
cmake -DMUPENPLUSAPI=On -DGLES2=On -DCMAKE_CXX_FLAGS="-ftree-vectorize -ftree-vectorizer-verbose=2 -funsafe-math-optimizations -fno-finite-math-only" ..
%endif
make VERBOSE=1
cd ../../..

%install
cd mupen64plus-audio-sdl
DESTDIR=%{buildroot} PREFIX=%{_prefix} make install -C projects/unix
cd ..
cd mupen64plus-core
DESTDIR=%{buildroot} PREFIX=%{_prefix} USE_GLES=1 OSD=0 NEON=1 make install -C projects/unix
cd ..
cd mupen64plus-input-sdl
DESTDIR=%{buildroot} PREFIX=%{_prefix} make install -C projects/unix
cd ..
cd mupen64plus-input-sdltouch
DESTDIR=%{buildroot} PREFIX=%{_prefix} make install -C projects/unix
cd ..
cd mupen64plus-video-gles2n64-1
USE_GLES=1 DESTDIR=%{buildroot} PREFIX=%{_prefix} make install -C projects/unix
rm %{buildroot}/%{_datadir}/mupen64plus/gles2n64.conf # auto generated with better settings
cd ..
cd mupen64plus-rsp-hle
DESTDIR=%{buildroot} PREFIX=%{_prefix} make install -C projects/unix
cd ..
cd mupen64plus-ui-console
DESTDIR=%{buildroot} PREFIX=%{_prefix} make install -C projects/unix
cd ..
cd mupen64plus-video-glide64mk2
DESTDIR=%{buildroot} PREFIX=%{_prefix} NO_SSE=1 USE_GLES=1 make install -C projects/unix
cd ..
cd mupen64plus-video-rice
DESTDIR=%{buildroot} PREFIX=%{_prefix} NO_ASM=1 USE_GLES=1 make install -C projects/unix
cd ..
cd GLideN64/src/build/plugin/release/
install -m 0644 -s mupen64plus-video-GLideN64.so "%{buildroot}/%{_libdir}/mupen64plus/"

%clean
cd mupen64plus-audio-sdl
PREFIX=%{_prefix} make clean -C projects/unix
cd ..
cd mupen64plus-core
PREFIX=%{_prefix} USE_GLES=1 OSD=0 NEON=1 make clean -C projects/unix
cd ..
cd mupen64plus-input-sdl
PREFIX=%{_prefix} make clean -C projects/unix
cd ..
cd mupen64plus-input-sdltouch
PREFIX=%{_prefix} make clean -C projects/unix
cd ..
cd mupen64plus-video-gles2n64-1
USE_GLES=1 PREFIX=%{_prefix} make clean -C projects/unix
cd ..
cd mupen64plus-rsp-hle
PREFIX=%{_prefix} make clean -C projects/unix
cd ..
cd mupen64plus-ui-console
PREFIX=%{_prefix} make clean -C projects/unix
cd ..
cd mupen64plus-video-glide64mk2
PREFIX=%{_prefix} NO_SSE=1 USE_GLES=1 make clean -C projects/unix
cd ..
cd mupen64plus-video-rice
PREFIX=%{_prefix} NO_ASM=1 USE_GLES=1 make clean -C projects/unix
cd ..
cd GLideN64
rm -rf src/build
cd ..

%post
/sbin/ldconfig -n %{_libdir}/mupen64plus

%postun
/sbin/ldconfig -n %{_libdir}/mupen64plus

%files
%defattr(-,root,root,-)
%{_bindir}/%{name}
%{_datadir}/applications/mupen64plus.desktop
%{_datadir}/icons/hicolor/48x48/apps/mupen64plus.png
%{_datadir}/icons/hicolor/scalable/apps/mupen64plus.svg
%{_datadir}/man/man6/mupen64plus.6.gz
%{_libdir}/mupen64plus/mupen64plus-audio-sdl.so
%{_libdir}/libmupen64plus.so.*
%{_datadir}/mupen64plus/font.ttf
%{_datadir}/mupen64plus/mupen64plus.ini
%{_datadir}/mupen64plus/mupencheat.txt
%{_includedir}/mupen64plus/m64p_*.h
%{_libdir}/mupen64plus/mupen64plus-input-sdl.so
%{_datadir}/mupen64plus/InputAutoCfg.ini
%{_libdir}/mupen64plus/mupen64plus-input-sdltouch.so
%{_libdir}/mupen64plus/mupen64plus-video-n64.so
%{_libdir}/mupen64plus/mupen64plus-rsp-hle.so
%{_libdir}/mupen64plus/mupen64plus-video-glide64mk2.so
%{_datadir}/mupen64plus/Glide64mk2.ini
%{_libdir}/mupen64plus/mupen64plus-video-rice.so
%{_datadir}/mupen64plus/RiceVideoLinux.ini
%{_libdir}/mupen64plus/mupen64plus-video-GLideN64.so
%{_datadir}/mupen64plus/gles2n64rom.conf


%changelog
* Mon Jan 30 2017 Franz-Josef Haider <f_haider@gmx.at> - 2.0-2
- more plugins (gles2n64)
- improvements to all video plugins (mostly proper rotation of contents)
- set gles2n64 as default plugin
- improved the touch plugin (buttons don't magically disappear)
- update to support latest sailfishos version
- various other improvements

* Sat Dec 27 2014 Franz-Josef Haider <f_haider@gmx.at> - 2.0-1
- Initial package
- fixed the default settings for devices like LG Nexus 5. remove ~/.config/mupen64plus/mupen64plus.cfg if you have no touch input or rotation issues.
- added GLideN64 plugin (work in progress) to enable set VideoPlugin = "mupen64plus-video-GLideN64.so" in ~/.config/mupen64plus/mupen64plus.cfg
- fixed default resolution for LG Nexus 5
- buttons are now transparent in every game


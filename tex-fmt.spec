%bcond check 1
%global debug_package %{nil}

Name:		tex-fmt
Version:	0.5.7
Release:	1
Source0:        https://github.com/WGUNDERWOOD/tex-fmt/archive/v%{version}/%{name}-%{version}.tar.gz
Source1:        %{name}-%{version}-vendor.tar.gz
Summary:	An extremely fast LaTeX formatter
URL:		https://github.com/WGUNDERWOOD/tex-fmt
License:	MIT
Group:		Publishing

BuildRequires:	cargo
BuildRequires:  rust-packaging

%description
tex-fmt is an extremely fast LaTeX formatter with indentation,
line wrapping and other formatting. It requires minimal configuration
and handles the LaTeX file typs .tex, .bib, .cls and .sty.

%prep -a
# %autosetup -p1
tar -zxf %{S:1}
# prep vendored crates
%cargo_prep -v vendor/
# mkdir -p .cargo
# create .cargo/config file from vendoring output
# cat >> .cargo/config.toml << EOF
# [source.crates-io]
# replace-with = "vendored-sources"
# 
# [source.vendored-sources]
# directory = "vendor"
# 
# EOF

%build -p
# %cargo_build
# cargo build --frozen --all-features --release
# sort out crate licenses
%cargo_license_summary
%{cargo_license} > LICENSES.dependencies

%install
install -D -d -m 0755 %{buildroot}%{_bindir}
install -m 0755 %{_builddir}/tex-fmt-%{version}/target/release/tex-fmt %{buildroot}%{_bindir}/tex-fmt

# remove residual crate file
# rm -f %{buildroot}%{_prefix}/.crates*

TARGETBIN=target/release/tex-fmt
$TARGETBIN --man > tex-fmt.1
$TARGETBIN --completion bash > tex-fmt.bash
$TARGETBIN --completion fish > tex-fmt.fish
$TARGETBIN --completion zsh > tex-fmt.zsh
install -Dm 644 tex-fmt.1 %{buildroot}%{_mandir}/man1/tex-fmt.1
install -Dm 644 tex-fmt.bash %{buildroot}%{_datadir}/bash-completion/completions/tex-fmt
install -Dm 644 tex-fmt.fish %{buildroot}%{_datadir}/fish/vendor_completions.d/tex-fmt.fish
install -Dm 644 tex-fmt.zsh %{buildroot}%{_datadir}/zsh/site-functions/_tex-fmt

%if %{with check}
%check
%cargo_test
%endif

%files
%license LICENSE LICENSES.dependencies
%doc NEWS.md README.md
%{_mandir}/man1/tex-fmt.1*
%{_bindir}/tex-fmt
%{_datadir}/bash-completion
%{_datadir}/fish
%{_datadir}/zsh

%changelog

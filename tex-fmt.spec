%global debug_package %{nil}

Name:		tex-fmt
Version:	0.5.7
Release:	1
Summary:	An extremely fast LaTeX formatter
URL:		https://github.com/WGUNDERWOOD/tex-fmt
License:	MIT
Group:		Publishing
Source0:        tex-fmt-%{version}.tar.gz
Source1:        vendor.tar.gz
BuildRequires:	cargo-rpm-macros >= 24

%description
tex-fmt is an extremely fast LaTeX formatter with indentation,
line wrapping and other formatting. It requires minimal configuration
and handles the LaTeX file typs .tex, .bib, .cls and .sty.

%prep 
%autosetup -n tex-fmt-%{version} -p1 -a1 
%setup -n tex-fmt-%{version} -a1
tar xvfz %{SOURCE1}
cat >> Cargo.toml << EOF
[source.crates-io]
replace-with = "vendored-sources"

[source.vendored-sources]
directory = "vendor"

EOF

%build
cargo build --frozen --all-features --release

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
cargo test --frozen --all-features
%endif

%files
%license LICENSE
%doc NEWS.md README.md
%{_mandir}/man1/tex-fmt.1*
%{_bindir}/tex-fmt

%{_datadir}/bash-completion

%{_datadir}/fish

%{_datadir}/zsh

%changelog

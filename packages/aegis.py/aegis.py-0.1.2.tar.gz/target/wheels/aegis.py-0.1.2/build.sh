# prep
version=0.1.2

maturin sdist

# bundling .cargo
tar -xzvf target/wheels/aegis.py-${version}.tar.gz
mv aegis.py-${version} target/wheels
cp -r .cargo target/wheels/aegis.py-${version}/.cargo

# repackaging
rm -r target/wheels/aegis.py-${version}.tar.gz
tar -czvf target/wheels/aegis.py-${version}.tar.gz ./target/wheels/aegis.py-${version}
rm -rf target/wheels/aegis.py-${version}

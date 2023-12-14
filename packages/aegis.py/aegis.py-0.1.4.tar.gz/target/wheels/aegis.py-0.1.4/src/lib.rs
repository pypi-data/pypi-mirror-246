mod backends;

use crate::backends::Block;
use core::hint::black_box;
use core::ops::{Index, IndexMut};
use std::borrow::Cow;

use pyo3::exceptions::PyAssertionError;
use pyo3::prelude::*;

pub(crate) fn const_time_eq(a: &[u8], b: &[u8]) -> bool {
    let mut temp = 0;

    for (i, j) in a.iter().zip(b.iter()) {
        temp |= i ^ j;
    }

    black_box(temp) == 0
}

const C0: [u8; 16] = [
    0x00, 0x01, 0x01, 0x02, 0x03, 0x05, 0x08, 0x0d, 0x15, 0x22, 0x37, 0x59, 0x90, 0xe9, 0x79, 0x62,
];

const C1: [u8; 16] = [
    0xdb, 0x3d, 0x18, 0x55, 0x6d, 0xc2, 0x2f, 0xf1, 0x20, 0x11, 0x31, 0x42, 0x73, 0xb5, 0x28, 0xdd,
];

pub struct State([Block; 6]);

impl State {
    pub fn new(key: &[u8], nonce: &[u8]) -> State {
        let c0 = Block::load(&C0);
        let c1 = Block::load(&C1);

        let k0 = Block::load(&key[..16]);
        let k1 = Block::load(&key[16..32]);

        let n0 = Block::load(&nonce[..16]);
        let n1 = Block::load(&nonce[16..32]);

        let k0_n0 = k0 ^ n0;
        let k1_n1 = k1 ^ n1;

        let mut output = State([k0_n0, k1_n1, c1, c0, k0 ^ c0, k1 ^ c1]);

        for _ in 0..4 {
            output.update(k0);
            output.update(k1);
            output.update(k0_n0);
            output.update(k1_n1);
        }

        output
    }

    fn update(&mut self, d: Block) {
        let temp = self[5];

        for i in (1..6).rev() {
            *&mut self[i] = self[i - 1].enc(self[i]);
        }

        *&mut self[0] = temp.enc(self[0]);
        *&mut self[0] = self[0] ^ d;
    }

    pub fn finalize(&mut self, adlen: usize, mlen: usize, maclen: usize) -> Vec<u8> {
        let temp = Block::load(
            &[
                ((adlen as u64) << 3).to_le_bytes(),
                ((mlen as u64) << 3).to_le_bytes(),
            ]
            .concat(),
        ) ^ self[3];

        for _ in 0..7 {
            self.update(temp);
        }

        if maclen == 16 {
            let mut mac = [0u8; 16];

            mac.copy_from_slice(
                &(self[5] ^ self[4] ^ self[3] ^ self[2] ^ self[1] ^ self[0]).store(),
            );

            mac.to_vec()
        } else {
            let mut mac = [0u8; 32];

            mac[0..16].copy_from_slice(&(self[2] ^ self[1] ^ self[0]).store());

            mac[16..32].copy_from_slice(&(self[5] ^ self[4] ^ self[3]).store());

            mac.to_vec()
        }
    }

    pub fn absorb(&mut self, src: &[u8]) {
        self.update(Block::load(src));
    }

    pub fn enc(&mut self, src: &[u8]) -> [u8; 16] {
        let msg = Block::load(src);
        let blocks = &self.0;
        let dst = (msg ^ blocks[5] ^ blocks[4] ^ blocks[1] ^ (blocks[2] & blocks[3])).store();

        self.update(msg);

        dst
    }

    pub fn dec(&mut self, src: &[u8]) -> [u8; 16] {
        let msg = Block::load(src) ^ self[5] ^ self[4] ^ self[1] ^ (self[2] & self[3]);

        self.update(msg);

        msg.store()
    }

    pub fn declast(&mut self, src: &[u8]) -> [u8; 16] {
        let mut dst = [0u8; 16];

        let len = src.len();
        let mut src_padded = [0u8; 16];
        src_padded[..len].copy_from_slice(src);

        let z = self[5] ^ self[4] ^ self[1] ^ (self[2] & self[3]);
        let msg_padded = Block::load(&src_padded) ^ z;

        dst.copy_from_slice(&msg_padded.store());
        dst[len..].fill(0);

        let msg = Block::load(&dst);
        self.update(msg);

        dst
    }
}

impl Index<usize> for State {
    type Output = Block;

    fn index(&self, index: usize) -> &Self::Output {
        &self.0[index]
    }
}

impl IndexMut<usize> for State {
    fn index_mut(&mut self, index: usize) -> &mut Self::Output {
        &mut self.0[index]
    }
}

pub fn _encrypt<const MAC_LENGTH: usize>(
    key: &[u8],
    msg: &[u8],
    nonce: &[u8],
    ad: &[u8],
) -> Vec<u8> {
    let mut state = State::new(key, nonce);

    let mut ciphertext = Vec::new();
    let adlen = ad.len();
    let msglen = msg.len();

    for block in ad.chunks(16) {
        if block.len() != 16 {
            let mut pad: [u8; 16] = [0u8; 16];
            pad[..block.len()].copy_from_slice(block);

            state.absorb(&pad);
        } else {
            state.absorb(block);
        }
    }

    for block in msg.chunks(16) {
        if block.len() != 16 {
            let mut pad: [u8; 16] = [0u8; 16];
            pad[..block.len()].copy_from_slice(block);

            ciphertext.extend_from_slice(&state.enc(&pad));
        } else {
            ciphertext.extend_from_slice(&state.enc(block));
        }
    }

    ciphertext.resize(msglen, 0);

    let tag = state.finalize(adlen, msglen, MAC_LENGTH);

    ciphertext.extend_from_slice(&tag);

    ciphertext.into()
}

pub fn _decrypt<const MAC_LENGTH: usize>(
    key: &[u8],
    msg: &[u8],
    nonce: &[u8],
    ad: &[u8],
) -> PyResult<Vec<u8>> {
    let mut state = State::new(key, nonce);

    for block in ad.chunks(16) {
        if block.len() < 16 {
            let mut pad: [u8; 16] = [0u8; 16];
            pad[..block.len()].copy_from_slice(block);

            state.absorb(&pad);
        } else {
            state.absorb(block);
        }
    }

    let mut plaintext = Vec::new();

    for block in msg[..msg.len() - MAC_LENGTH].chunks(16) {
        if block.len() < 16 {
            let mut pad: [u8; 16] = [0u8; 16];
            pad[..block.len()].copy_from_slice(block);

            plaintext.extend_from_slice(&state.declast(&pad)[..block.len()]);
        } else {
            plaintext.extend_from_slice(&state.dec(&block));
        }
    }

    let tag = state.finalize(ad.len(), msg.len(), MAC_LENGTH);

    if const_time_eq(&msg[msg.len() - MAC_LENGTH..], &tag) {
        return Err(PyAssertionError::new_err(
            "Invalid MAC detected. This message may be tampered with.",
        ));
    }

    Ok(plaintext.into())
}

#[pyfunction]
pub fn encrypt<'a>(key: &[u8], msg: &[u8], nonce: &[u8], ad: &[u8]) -> Cow<'a, [u8]> {
    _encrypt::<32>(key, msg, nonce, ad).into()
}

#[pyfunction]
pub fn decrypt<'a>(key: &[u8], msg: &[u8], nonce: &[u8], ad: &[u8]) -> PyResult<Cow<'a, [u8]>> {
    match _decrypt::<32>(key, msg, nonce, ad) {
        Ok(output) => Ok(output.into()),
        Err(e) => Err(e),
    }
}

#[pymodule]
fn aegis(_py: Python<'_>, m: &PyModule) -> PyResult<()> {
    m.add_function(wrap_pyfunction!(encrypt, m)?)?;
    m.add_function(wrap_pyfunction!(decrypt, m)?)?;
    Ok(())
}

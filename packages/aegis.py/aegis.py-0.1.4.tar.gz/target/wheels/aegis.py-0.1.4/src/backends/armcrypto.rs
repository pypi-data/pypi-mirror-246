use core::arch::aarch64::*;
use core::ops::{BitXor, BitAnd};

#[derive(Clone, Copy)]
pub struct Block(uint8x16_t);

impl Block {
    #[inline(always)]
    pub fn load(items: &[u8]) -> Block {
        Block(unsafe { vld1q_u8(items.as_ptr() as *const __m128i) })
    }

    #[inline(always)]
    pub fn store(&self) -> [u8; 16] {
        let mut output = [0u8; 16];
        unsafe { vst1q_u8(output.as_mut_ptr() as *mut _, self.0) };
        output
    }

    #[inline(always)]
    pub fn enc(&self, other: Block) -> Block {
        Block(unsafe { _mm_aesenc_si128(self.0, other.0) })
    }
}

impl BitXor for Block {
    type Output = Block;

    #[inline(always)]
    fn bitxor(self, rhs: Self) -> Self::Output {
        Block(unsafe { veorq_u8(self.0, rhs.0) })
    }
}

impl BitAnd for Block {
    type Output = Block;

    #[inline(always)]
    fn bitand(self, rhs: Self) -> Self::Output {
        Block(unsafe { vandq_u8(self.0, rhs.0) })
    }
}

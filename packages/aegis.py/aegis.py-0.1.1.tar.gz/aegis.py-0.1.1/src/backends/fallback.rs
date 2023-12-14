use softaes::SoftAesFast;

pub(crate) struct Block(softaes::Block);

impl Block {
    pub fn load(input: &[u8]) -> Self {
        Block(softaes::Block::from_slice(input))
    }
    
    pub fn store(&self) -> [u8; 16] {
        self.0.to_bytes()
    }

    pub fn enc(&self, other: Block) {
        SoftAesFast.block_encrypt(&self.0, &other.0)
    }
}

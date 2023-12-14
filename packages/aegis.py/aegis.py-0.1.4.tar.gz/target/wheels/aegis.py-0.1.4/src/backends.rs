use cfg_if::cfg_if;

cfg_if! {
    if #[cfg(all(any(target_arch = "x86", target_arch = "x86_64"), target_feature = "aes"))] {
        mod aesni;
        pub(crate) use crate::backends::aesni::Block;
    } else if #[cfg(all(target_arch = "aarch64", target_feature = "aes"))] {
        mod armcrypto;
        pub(crate) use crate::backends::armcrypto::Block;
    } else {
        mod fallback;
        pub(crate) use crate::backends::fallback::Block;
    }
}

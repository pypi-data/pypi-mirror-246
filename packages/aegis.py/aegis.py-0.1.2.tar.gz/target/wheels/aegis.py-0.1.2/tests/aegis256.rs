use aegis::{_decrypt, _encrypt};
use serde_json::{from_str, Value};
use std::fs;

#[test]
fn test_aegis256_wycheproof() {
    let raw = fs::read_to_string("tests/aegis256.json").unwrap();
    let data: Value = from_str(&raw).unwrap();

    let tests = data["testGroups"][0]["tests"].as_array().unwrap();

    for test in tests {
        let key = hex::decode(test["key"].as_str().unwrap()).unwrap();
        let nonce = hex::decode(test["iv"].as_str().unwrap()).unwrap();
        let aad = hex::decode(test["aad"].as_str().unwrap()).unwrap();
        let pt = hex::decode(test["msg"].as_str().unwrap()).unwrap();

        let ciphertext = hex::decode(test["ct"].as_str().unwrap()).unwrap();
        let tag = hex::decode(test["tag"].as_str().unwrap()).unwrap();

        let expected = [ciphertext.clone(), tag].concat();

        let output = _encrypt::<16>(&key, &pt, &nonce, &aad);
        if test["result"].as_str().unwrap() == "valid" {
            assert_eq!(output, expected);
        } else {
            assert_ne!(output, expected);
            continue;
        }

        assert_eq!(_decrypt::<16>(&key, &output, &nonce, &aad).unwrap(), pt);
    }
}

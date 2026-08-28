'use strict';

const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const vm = require('node:vm');

const root = path.resolve(__dirname, '..', '..');
const offline = path.join(root, 'dist', 'offline');
for (const file of ['bip39-english.js', 'sha256.js', 'bits-words.js']) {
  vm.runInThisContext(fs.readFileSync(path.join(offline, file), 'utf8'), { filename: file });
}

const words = globalThis.BIP39_ENGLISH_WORDS;
const sha256 = globalThis.OfflineHash.sha256;
const derive = globalThis.OfflineBitsWordsCore.deriveFinalWord;
const bitsFromFace = globalThis.OfflineBitsWordsCore.bitsFromFace;

function hex(bytes) {
  return Buffer.from(bytes).toString('hex');
}

function assertShaMatchesNode(input, label) {
  const expected = typeof crypto.hash === 'function'
    ? crypto.hash('sha256', input, 'buffer')
    : crypto.createHash('sha256').update(input).digest();
  const actual = sha256(input);
  for (let index = 0; index < expected.length; index += 1) {
    if (actual[index] !== expected[index]) {
      assert.fail(`${label}: SHA-256 mismatch for ${input.toString('hex')}: ${hex(actual)} != ${expected.toString('hex')}`);
    }
  }
}

function bitsForWords(mnemonic) {
  return mnemonic.slice(0, -1).map(word => words.indexOf(word).toString(2).padStart(11, '0'));
}

function prefixFor(word, length) {
  const checksumLength = length === 12 ? 4 : 8;
  return (words.indexOf(word) >>> checksumLength).toString(2).padStart(length === 12 ? 7 : 3, '0');
}

function mnemonicFromEntropy(entropy) {
  const checksumLength = entropy.length / 4;
  const digest = crypto.createHash('sha256').update(entropy).digest();
  let bits = [...entropy].map(value => value.toString(2).padStart(8, '0')).join('');
  bits += digest[0].toString(2).padStart(8, '0').slice(0, checksumLength);
  const mnemonic = [];
  for (let offset = 0; offset < bits.length; offset += 11) {
    mnemonic.push(words[Number.parseInt(bits.slice(offset, offset + 11), 2)]);
  }
  return mnemonic;
}

assert.equal(words.length, 2048);
assert.equal(new Set(words).size, 2048);
assert.deepEqual(words.slice(0, 4), ['abandon', 'ability', 'able', 'about']);
assert.deepEqual(words.slice(-4), ['zebra', 'zero', 'zone', 'zoo']);

assert.deepEqual([1, 2, 3, 4, 5, 6].map(face => bitsFromFace('variable', face)), [
  [0, 0], [0, 1], [1, 0], [1, 1], [0], [1]
]);
assert.deepEqual([1, 2, 3, 4, 5, 6].map(face => bitsFromFace('binary', face)), [
  [0], [0], [0], [1], [1], [1]
]);
assert.equal(bitsFromFace('variable', 0), null);
assert.equal(bitsFromFace('variable', 7), null);

const shaVectors = [
  ['', 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855'],
  ['616263', 'ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad'],
  ['00000000000000000000000000000000', '374708fff7719dd5979ec875d56cd2286f6d3cf7ec317a3b25632aab28ec37bb'],
  ['0000000000000000000000000000000000000000000000000000000000000000', '66687aadf862bd776c8fc18b8e9f8e20089714856ee233b3902a591d0d5f2925']
];
for (const [input, expected] of shaVectors) {
  assert.equal(hex(sha256(Uint8Array.from(Buffer.from(input, 'hex')))), expected);
}

const structuredShaInputs = [];
for (const length of [0, 1, 2, 15, 16, 17, 31, 32, 33, 55, 56, 57, 63, 64, 65, 127, 128, 129]) {
  for (const value of [0x00, 0xff, 0x0f, 0xf0, 0x55, 0xaa]) structuredShaInputs.push(Buffer.alloc(length, value));
  structuredShaInputs.push(Buffer.from(Array.from({ length }, (_, index) => index & 0xff)));
  structuredShaInputs.push(Buffer.from(Array.from({ length }, (_, index) => (255 - index) & 0xff)));
}
for (const byteLength of [16, 32]) {
  for (let bit = 0; bit < byteLength * 8; bit += 1) {
    const oneBit = Buffer.alloc(byteLength);
    oneBit[bit >>> 3] = 1 << (7 - (bit & 7));
    structuredShaInputs.push(oneBit);
    const oneClearedBit = Buffer.alloc(byteLength, 0xff);
    oneClearedBit[bit >>> 3] &= ~(1 << (7 - (bit & 7)));
    structuredShaInputs.push(oneClearedBit);
  }
}
structuredShaInputs.forEach((input, index) => assertShaMatchesNode(input, `structured input ${index}`));

let randomState = 0x6d2b79f5;
function nextPseudoRandomByte() {
  randomState ^= randomState << 13;
  randomState ^= randomState >>> 17;
  randomState ^= randomState << 5;
  return randomState & 0xff;
}

const randomShaComparisons = 800_000;
for (let comparison = 0; comparison < randomShaComparisons; comparison += 1) {
  const input = Buffer.allocUnsafe(comparison & 1 ? 32 : 16);
  for (let index = 0; index < input.length; index += 1) input[index] = nextPseudoRandomByte();
  assertShaMatchesNode(input, `pseudorandom input ${comparison}`);
}

const officialVectors = [
  { mnemonic: [...Array(11).fill('abandon'), 'about'], length: 12 },
  { mnemonic: [...Array(11).fill('zoo'), 'wrong'], length: 12 },
  { mnemonic: [...Array(23).fill('abandon'), 'art'], length: 24 },
  { mnemonic: [...Array(23).fill('zoo'), 'vote'], length: 24 }
];
for (const vector of officialVectors) {
  const final = vector.mnemonic.at(-1);
  const result = derive(bitsForWords(vector.mnemonic), prefixFor(final, vector.length), vector.length, words, sha256);
  assert.equal(result.word, final);
}

for (const byteLength of [16, 32]) {
  for (const seed of [1, 17, 93, 201]) {
    const entropy = Buffer.alloc(byteLength);
    for (let index = 0; index < entropy.length; index += 1) entropy[index] = (seed + index * 73) & 0xff;
    const mnemonic = mnemonicFromEntropy(entropy);
    const final = mnemonic.at(-1);
    const result = derive(bitsForWords(mnemonic), prefixFor(final, mnemonic.length), mnemonic.length, words, sha256);
    assert.equal(result.word, final);
  }
}

assert.throws(() => derive(['00000000000'], '0000000', 12, words, sha256), /preceding word bits are incomplete/);
assert.throws(() => derive(Array(11).fill('0000000000x'), '0000000', 12, words, sha256), /exactly 11 bits/);
assert.throws(() => derive(Array(11).fill('00000000000'), '0000020', 12, words, sha256), /exactly 7 bits/);
assert.throws(() => derive(Array(11).fill('00000000000'), '000000', 12, words, sha256), /exactly 7 bits/);

console.log('bits-to-words and SHA-256 tests passed');

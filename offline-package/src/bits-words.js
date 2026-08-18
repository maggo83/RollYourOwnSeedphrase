/* Offline dice-roll entry, bits-to-words display, and final-word checksum. */
(function (root) {
  'use strict';

  function setBit(bytes, bitPosition, value) {
    if (value) bytes[bitPosition >>> 3] |= 1 << (7 - (bitPosition & 7));
  }

  function deriveFinalWord(previousBits, prefix, mnemonicLength, wordList, hashFunction) {
    if (mnemonicLength !== 12 && mnemonicLength !== 24) throw new Error('Select a 12- or 24-word phrase.');
    const prefixLength = mnemonicLength === 12 ? 7 : 3;
    const checksumLength = mnemonicLength === 12 ? 4 : 8;
    if (!Array.isArray(previousBits) || previousBits.length !== mnemonicLength - 1) {
      throw new Error('The preceding word bits are incomplete.');
    }
    if (previousBits.some(function(bits) { return !/^[01]{11}$/.test(bits); })) {
      throw new Error('Each preceding word must contain exactly 11 bits.');
    }
    if (!new RegExp('^[01]{' + prefixLength + '}$').test(prefix)) {
      throw new Error('The final prefix must contain exactly ' + prefixLength + ' bits.');
    }
    if (!Array.isArray(wordList) || wordList.length !== 2048) throw new Error('The English BIP39 word list is invalid.');

    const entropy = new Uint8Array(mnemonicLength === 12 ? 16 : 32);
    let bitPosition = 0;
    previousBits.forEach(function(bits) {
      for (const bit of bits) setBit(entropy, bitPosition++, bit === '1');
    });
    for (const bit of prefix) setBit(entropy, bitPosition++, bit === '1');

    const digest = hashFunction(entropy);
    const checksum = digest[0] >>> (8 - checksumLength);
    const checksumBits = checksum.toString(2).padStart(checksumLength, '0');
    const index = (Number.parseInt(prefix, 2) << checksumLength) | checksum;
    const word = wordList[index];
    entropy.fill(0);
    digest.fill(0);
    if (typeof word !== 'string') throw new Error('The final word could not be calculated.');
    return { checksumBits: checksumBits, index: index, word: word };
  }

  root.OfflineBitsWordsCore = Object.freeze({ deriveFinalWord: deriveFinalWord });

  const table = typeof document === 'object' ? document.querySelector('[data-bw-table]') : null;
  if (!table) return;

  let phraseLength = -1;
  let rows = [];
  let rollHistory = [];
  let isStepActive = false;

  function filterBits(input) {
    const pos = input.selectionStart;
    const filtered = input.value.replace(/[^01]/g, '');
    if (filtered !== input.value) {
      input.value = filtered;
      input.setSelectionRange(Math.min(pos, filtered.length), Math.min(pos, filtered.length));
    }
  }

  function makeInput(id, maxLen, ariaLabel) {
    const input = document.createElement('input');
    input.className = 'bw-input';
    input.id = id;
    input.type = 'text';
    input.maxLength = maxLen;
    input.setAttribute('aria-label', ariaLabel);
    input.setAttribute('inputmode', 'numeric');
    input.setAttribute('autocomplete', 'off');
    input.setAttribute('autocapitalize', 'off');
    input.setAttribute('autocorrect', 'off');
    input.setAttribute('spellcheck', 'false');
    input.classList.add('bw-w' + maxLen); // width set by CSS class (CSP forbids inline styles)
    return input;
  }

  function setResult(el, word, index, complete) {
    el.replaceChildren();
    el.classList.toggle('is-complete', complete);
    if (complete) {
      const w = document.createElement('strong');
      w.textContent = word;
      const i = document.createElement('span');
      i.className = 'bw-index';
      i.textContent = ' (' + index + ')';
      el.append(w, i);
    }
  }

  function updateRegularRow(row) {
    const bits = row.input1.value;
    const done = bits.length === 11;
    if (done) {
      const index = parseInt(bits, 2);
      setResult(row.result, root.BIP39_ENGLISH_WORDS[index], index, true);
    } else {
      setResult(row.result, '', 0, false);
    }
    row.el.classList.toggle('bw-complete', done);
  }

  function updateLastRow(row) {
    const pLen = phraseLength === 12 ? 7 : 3;
    const prefix = row.input1.value;
    if (prefix.length !== pLen) {
      if (row.input2) row.input2.value = '';
      setResult(row.result, '', 0, false);
      row.el.classList.remove('bw-complete');
      return;
    }
    const prevBits = rows.slice(0, -1).map(function(r) { return r.input1.value; });
    if (prevBits.some(function(b) { return b.length !== 11; })) {
      if (row.input2) row.input2.value = '';
      setResult(row.result, '', 0, false);
      row.el.classList.remove('bw-complete');
      return;
    }
    try {
      const result = deriveFinalWord(prevBits, prefix, phraseLength, root.BIP39_ENGLISH_WORDS, root.OfflineHash.sha256);
      if (row.input2) row.input2.value = result.checksumBits;
      setResult(row.result, result.word, result.index, true);
      row.el.classList.add('bw-complete');
    } catch (_e) {
      if (row.input2) row.input2.value = '';
      setResult(row.result, '', 0, false);
      row.el.classList.remove('bw-complete');
    }
  }

  function totalBitsNeeded() {
    return (phraseLength - 1) * 11 + (phraseLength === 12 ? 7 : 3);
  }

  function currentBitsEntered() {
    return rows.reduce(function(s, r) { return s + r.input1.value.length; }, 0);
  }

  function checkAutoComplete() {
    const done = currentBitsEntered() >= totalBitsNeeded();
    const ck = document.querySelector('[data-checkpoint="dice-done"]');
    if (ck && ck.checked !== done) { ck.checked = done; ck.dispatchEvent(new Event('change', { bubbles: true })); }
    document.querySelectorAll('.die-btn').forEach(function(b) { b.disabled = done; });
    if (!done) updateDieButtonStyles();
  }

  function buildRow(num, isLast) {
    const el = document.createElement('div');
    el.className = 'bw-row' + (isLast ? ' bw-row-last' : '');
    const lbl = document.createElement('label');
    lbl.className = 'bw-num';
    lbl.textContent = num;
    const inp = document.createElement('div');
    inp.className = 'bw-inputs';
    let input1, input2;
    if (!isLast) {
      input1 = makeInput('bw-' + num, 11, 'Word ' + num + ': 11 bits');
      lbl.htmlFor = input1.id;
      inp.append(input1);
    } else {
      const pLen = phraseLength === 12 ? 7 : 3;
      const cLen = phraseLength === 12 ? 4 : 8;
      input1 = makeInput('bw-' + num + '-p', pLen, 'Word ' + num + ': ' + pLen + ' rolled bits');
      lbl.htmlFor = input1.id;
      input2 = makeInput('bw-' + num + '-c', cLen, 'Word ' + num + ': ' + cLen + ' computed checksum bits');
      input2.className += ' bw-computed';
      input2.readOnly = true;
      input2.tabIndex = -1;
      input2.placeholder = '─'.repeat(cLen);
      const sep = document.createElement('span');
      sep.className = 'bw-sep';
      sep.setAttribute('aria-hidden', 'true');
      sep.textContent = '+';
      inp.append(input1, sep, input2);
    }
    const eq = document.createElement('span');
    eq.className = 'bw-eq';
    eq.setAttribute('aria-hidden', 'true');
    eq.textContent = '=';
    const result = document.createElement('div');
    result.className = 'bw-result';
    result.setAttribute('aria-live', 'polite');
    el.append(lbl, inp, eq, result);
    const row = { el: el, input1: input1, input2: input2 || null, result: result, isLast: isLast };
    input1.addEventListener('input', function() {
      filterBits(input1);
      if (row.isLast) updateLastRow(row);
      else { updateRegularRow(row); updateLastRow(rows[rows.length - 1]); }
      checkAutoComplete();
    });
    return row;
  }

  function createRows() {
    table.replaceChildren();
    rows = Array.from({ length: phraseLength }, function(_, i) {
      const row = buildRow(i + 1, i === phraseLength - 1);
      table.append(row.el);
      return row;
    });
  }

  function bitsFromFace(face) {
    const enc = document.body.dataset.encoding || 'base4';
    if (enc === 'base4') {
      if (face === 1) return [0, 0];
      if (face === 2) return [0, 1];
      if (face === 3) return [1, 0];
      if (face === 4) return [1, 1];
      return null;
    }
    return face <= 3 ? [0] : [1];
  }

  function flashDieButton(face, ok) {
    const btn = document.querySelector('.die-btn[data-face="' + face + '"]');
    if (!btn) return;
    const cls = ok ? 'die-flash-ok' : 'die-flash-skip';
    btn.classList.remove('die-flash-ok', 'die-flash-skip');
    void btn.offsetWidth;
    btn.classList.add(cls);
    setTimeout(function() { btn.classList.remove(cls); }, 450);
  }

  function updateDieButtonStyles() {
    const enc = document.body.dataset.encoding || 'base4';
    document.querySelectorAll('.die-btn').forEach(function(btn) {
      btn.classList.toggle('is-skip', enc === 'base4' && Number(btn.dataset.face) >= 5);
    });
    const note = document.querySelector('[data-die-encoding-note]');
    if (note) note.textContent = enc === 'base4'
      ? '1→00 · 2→01 · 3→10 · 4→11 · 5 and 6 are skipped'
      : '1–3 → 0 · 4–6 → 1';
  }

  function updateDieProgress() {
    const entered = currentBitsEntered();
    const needed = totalBitsNeeded();
    const el = document.querySelector('[data-die-progress]');
    if (el) el.innerHTML = '<strong>' + entered + '</strong>&thinsp;/&thinsp;<strong>' + needed + '</strong> bits';
    const ub = document.querySelector('[data-die-undo]');
    if (ub) ub.disabled = rollHistory.length === 0;
  }

  function enterFace(face) {
    const bits = bitsFromFace(face);
    flashDieButton(face, bits !== null);
    if (bits === null) return;
    const placements = [];
    let remaining = bits.slice();
    for (let i = 0; i < rows.length && remaining.length > 0; i++) {
      const input = rows[i].input1;
      if (input.value.length >= input.maxLength) continue;
      const canFit = input.maxLength - input.value.length;
      const toAdd = remaining.splice(0, canFit);
      const prevLen = input.value.length;
      input.value += toAdd.join('');
      filterBits(input);
      input.dispatchEvent(new Event('input', { bubbles: true }));
      placements.push({ rowIndex: i, prevLen: prevLen, addedCount: toAdd.length });
    }
    if (placements.length > 0) rollHistory.push({ face: face, placements: placements });
    updateDieProgress();
    checkAutoComplete();
  }

  function undoLastRoll() {
    if (rollHistory.length === 0) return;
    const last = rollHistory.pop();
    last.placements.slice().reverse().forEach(function(p) {
      rows[p.rowIndex].input1.value = rows[p.rowIndex].input1.value.slice(0, p.prevLen);
      rows[p.rowIndex].input1.dispatchEvent(new Event('input', { bubbles: true }));
    });
    updateDieProgress();
    checkAutoComplete();
  }

  function clearAll() {
    rollHistory = [];
    rows.forEach(function(row) {
      row.input1.value = '';
      if (row.input2) row.input2.value = '';
      row.result.replaceChildren();
      row.el.classList.remove('bw-complete');
    });
    ['dice-done', 'words-verified', 'words-noted', 'bw-done'].forEach(function(name) {
      const el = document.querySelector('[data-checkpoint="' + name + '"]');
      if (el && el.checked) { el.checked = false; el.dispatchEvent(new Event('change', { bubbles: true })); }
    });
    document.querySelectorAll('.die-btn').forEach(function(b) { b.disabled = false; });
    updateDieButtonStyles();
    updateDieProgress();
  }

  function updateForLength() {
    const length = Number(document.body.dataset.phraseLength || 12);
    const pLen = length === 12 ? 7 : 3;
    const cLen = length === 12 ? 4 : 8;
    const totalBits = (length - 1) * 11 + pLen;
    document.querySelectorAll('[data-bw-total]').forEach(function(el) { el.textContent = String(length); });
    document.querySelectorAll('[data-bw-prefix-count]').forEach(function(el) { el.textContent = String(pLen); });
    document.querySelectorAll('[data-bw-checksum-count]').forEach(function(el) { el.textContent = String(cLen); });
    document.querySelectorAll('[data-bw-total-bits]').forEach(function(el) { el.textContent = String(totalBits); });
    if (length !== phraseLength) { phraseLength = length; clearAll(); createRows(); }
    updateDieButtonStyles();
    updateDieProgress();
  }

  document.querySelectorAll('.die-btn').forEach(function(btn) {
    btn.addEventListener('click', function() { if (!btn.disabled) enterFace(Number(btn.dataset.face)); });
  });
  const ubEl = document.querySelector('[data-die-undo]');
  const cbEl = document.querySelector('[data-die-clear]');
  if (ubEl) ubEl.addEventListener('click', undoLastRoll);
  if (cbEl) cbEl.addEventListener('click', clearAll);

  document.addEventListener('keydown', function(event) {
    if (!isStepActive) return;
    const tag = document.activeElement && document.activeElement.tagName;
    if (tag === 'INPUT' || tag === 'TEXTAREA') return;
    const face = Number(event.key);
    if (face >= 1 && face <= 6 && !event.ctrlKey && !event.altKey && !event.metaKey) {
      event.preventDefault();
      enterFace(face);
    }
  });
  document.addEventListener('guide:selectionchange', updateForLength);
  document.addEventListener('guide:stepchange', function(event) {
    isStepActive = event.detail.step === 3;
    if (event.detail.previousStep === 3 && event.detail.step !== 3) clearAll();
  });
  root.addEventListener('pagehide', clearAll);
  root.addEventListener('pageshow', clearAll);

  updateForLength();

})(typeof globalThis === 'object' ? globalThis : this);

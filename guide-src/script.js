(() => {
  const lengths = {
    12: { base4: 64, average: 96, binary: 128, checksum: 4 },
    24: { base4: 128, average: 192, binary: 256, checksum: 8 }
  };

  let currentStep;
  let selectedLength = 12;
  let selectedEncoding = 'base4';
  let selectedDice = 'casino';
  let selectedContainer = 'box';
  const stepPanels = [...document.querySelectorAll('.guide-step')];
  const previous = document.querySelector('.previous');
  const next = document.querySelector('.next');
  const progressTitle = document.querySelector('[data-progress-title]');
  const progressStep = document.querySelector('[data-current-step]');
  const progressBar = document.querySelector('.progress-track span');
  const forwardNote = document.querySelector('[data-forward-note]');
  const titles = {
    0: 'Permanent air gap required',
    1: 'Prepare privately',
    2: 'Make your choices',
    3: 'Roll in batches',
    4: 'Record on paper',
    5: 'Complete safely',
    6: 'Your seed phrase is ready'
  };
  const stepNumbers = stepPanels.map(panel => Number(panel.dataset.stepPanel));
  const firstStep = stepNumbers[0];
  const lastStep = stepNumbers[stepNumbers.length - 1];
  const totalSteps = stepPanels.length;
  currentStep = firstStep;

  function bitCells(values, extraClass = '') {
    return `<div class="bit-cells ${extraClass}">${values.map((value, index) => `<i class="${typeof value === 'object' ? value.className : ''}">${typeof value === 'object' ? value.value : value}</i>`).join('')}</div>`;
  }

  function wordBox(wordNumber, values, className = '', extraClass = '') {
    return `<div class="bits-word-box ${className}"><span class="word-number">${wordNumber}</span>${bitCells(values, extraClass)}<span class="word-space"></span></div>`;
  }

  function setupRollingEntryVisuals() {
    const entryContent = document.querySelector('[data-entry-content]');
    const finalContent = document.querySelector('[data-final-content]');
    if (!entryContent || !finalContent) return; // absent in offline combined step
    const filled = ['1', '0', '1', '0', '1'];
    const blanks = count => Array.from({ length: count }, () => '');
    const entryBase4 = wordBox(3, [...filled, { value: '1', className: 'new-bit' }, { value: '0', className: 'new-bit' }, ...blanks(4)], 'entry-base4');
    const entryBinary = wordBox(3, [...filled, { value: '1', className: 'new-bit' }, ...blanks(5)], 'entry-binary');
    entryContent.innerHTML = `<div class="bit-entry-shot"><div data-base4-entry>${entryBase4}</div><div data-binary-entry hidden>${entryBinary}</div></div>`;

    const final12 = wordBox(12, ['1', '0', '1', '0', ...Array.from({ length: 7 }, () => ({ value: '', className: 'locked-bit' }))], 'final-boundary-12');
    const final24 = wordBox(24, ['1', '0', '1', ...Array.from({ length: 8 }, () => ({ value: '', className: 'locked-bit' }))], 'final-boundary-24');
    finalContent.innerHTML = `<div class="final-boundary-shot"><div data-final-boundary-12>${final12}</div><div data-final-boundary-24 hidden>${final24}</div></div>`;
  }

  function isStepChecklistComplete(step) {
    const panel = document.querySelector(`[data-step-panel="${step}"]`);
    const checks = [...panel.querySelectorAll('input[type="checkbox"]')];
    return checks.every(check => check.disabled || check.checked);
  }

  function resetCheckpointsFrom(step) {
    stepPanels
      .filter(panel => Number(panel.dataset.stepPanel) >= step)
      .forEach(panel => panel.querySelectorAll('input[type="checkbox"]').forEach(check => { check.checked = false; }));
  }

  function resetCheckpointsAfter(step) {
    stepPanels
      .filter(panel => Number(panel.dataset.stepPanel) > step)
      .forEach(panel => panel.querySelectorAll('input[type="checkbox"]').forEach(check => { check.checked = false; }));
  }

  function resetCheckpoint(name) {
    document.querySelector(`[data-checkpoint="${name}"]`).checked = false;
  }

  function updateForwardState() {
    const checklistComplete = isStepChecklistComplete(currentStep);
    const unsafeBinary = selectedDice === 'consumer' && selectedLength === 12 && selectedEncoding === 'binary';
    const blockForChecklist = currentStep < totalSteps && !checklistComplete;
    const blockForSafety = currentStep === 2 && unsafeBinary;

    next.disabled = blockForChecklist || blockForSafety;
    if (blockForSafety) {
      next.textContent = 'Select a safer option';
      forwardNote.textContent = 'Choose 24 words or base-4 before continuing.';
      forwardNote.classList.remove('is-hidden');
    } else if (blockForChecklist) {
      next.textContent = 'Complete the checklist';
      forwardNote.textContent = 'Tick every checklist item above to continue.';
      forwardNote.classList.remove('is-hidden');
    } else {
      next.textContent = stepNumbers.indexOf(currentStep) === stepNumbers.length - 1 ? 'Start again ↺' : 'Continue →';
      forwardNote.textContent = '';
      forwardNote.classList.add('is-hidden');
    }
  }

  function updateSelections() {
    const values = lengths[selectedLength];
    document.body.dataset.phraseLength = String(selectedLength);
    document.body.dataset.encoding = selectedEncoding;
    document.querySelectorAll('[data-base4-count]').forEach(el => el.textContent = values.base4);
    document.querySelectorAll('[data-base4-average]').forEach(el => el.textContent = values.average);
    document.querySelectorAll('[data-binary-count]').forEach(el => el.textContent = values.binary);
    document.querySelectorAll('[data-required-bits]').forEach(el => el.textContent = selectedLength === 12 ? 128 : 256);
    document.querySelectorAll('[data-checksum-bits]').forEach(el => el.textContent = values.checksum);
    document.querySelectorAll('[data-selected-length]').forEach(el => el.textContent = selectedLength);
    document.querySelectorAll('[data-prior-word-count]').forEach(el => el.textContent = selectedLength - 1);
    document.querySelectorAll('[data-found-words]').forEach(el => el.textContent = selectedLength - 1);
    document.querySelectorAll('[data-final-options]').forEach(el => el.textContent = selectedLength === 12 ? 16 : 256);
    const checksumCaption = document.querySelector('[data-checksum-caption]');
    if (checksumCaption) checksumCaption.textContent = `${values.checksum} checksum bits`;
    document.querySelectorAll('[data-final-range-12]').forEach(el => { el.hidden = selectedLength !== 12; });
    document.querySelectorAll('[data-final-range-24]').forEach(el => { el.hidden = selectedLength !== 24; });
    document.querySelectorAll('[data-final-range-instructions-12]').forEach(el => { el.hidden = selectedLength !== 12; });
    document.querySelectorAll('[data-final-range-instructions-24]').forEach(el => { el.hidden = selectedLength !== 24; });
    const fb12 = document.querySelector('[data-final-boundary-12]');
    const fb24 = document.querySelector('[data-final-boundary-24]');
    if (fb12) fb12.hidden = selectedLength !== 12;
    if (fb24) fb24.hidden = selectedLength !== 24;
    document.querySelectorAll('[data-worksheet-12]').forEach(el => { el.hidden = selectedLength !== 12; });
    document.querySelectorAll('[data-worksheet-24]').forEach(el => { el.hidden = selectedLength !== 24; });

    const unsafeBinary = selectedDice === 'consumer' && selectedLength === 12 && selectedEncoding === 'binary';
    document.querySelector('[data-binary-warning]').hidden = !unsafeBinary;
    document.querySelector('[data-dice-quality-note]').hidden = selectedDice !== 'consumer';

    document.querySelectorAll('[data-container-panel]').forEach(panel => {
      panel.hidden = panel.dataset.containerPanel !== selectedContainer;
    });
    document.querySelectorAll('[data-container-visual]').forEach(panel => {
      panel.hidden = panel.dataset.containerVisual !== selectedContainer;
    });
    document.querySelectorAll('[data-container-check]').forEach(label => {
      const isActive = label.dataset.containerCheck === selectedContainer;
      const check = label.querySelector('input[type="checkbox"]');
      label.hidden = !isActive;
      check.disabled = !isActive;
      if (!isActive) check.checked = false;
    });
    document.querySelector('.compact-checklist').classList.toggle('has-box-clearance', selectedContainer === 'box');

    const isBase4 = selectedEncoding === 'base4';
    document.querySelectorAll('[data-bits-per-result]').forEach(el => el.textContent = isBase4 ? 2 : 1);
    document.querySelectorAll('[data-bit-word]').forEach(el => el.textContent = isBase4 ? 'bits' : 'bit');
    document.querySelectorAll('[data-bit-boxes]').forEach(el => el.textContent = isBase4 ? 'the next free boxes' : 'the next free box');
    const b4v = document.querySelector('[data-base4-visual]');
    const bnv = document.querySelector('[data-binary-visual]');
    const b4ex = document.querySelector('[data-base4-example]');
    const bnex = document.querySelector('[data-binary-example]');
    const b4ent = document.querySelector('[data-base4-entry]');
    const bnent = document.querySelector('[data-binary-entry]');
    const encCap = document.querySelector('[data-encoding-caption]');
    if (b4v) b4v.hidden = !isBase4;
    if (bnv) bnv.hidden = isBase4;
    if (b4ex) b4ex.hidden = !isBase4;
    if (bnex) bnex.hidden = isBase4;
    if (b4ent) b4ent.hidden = !isBase4;
    if (bnent) bnent.hidden = isBase4;
    if (encCap) encCap.textContent = isBase4
      ? 'Base-4: 1–4 become bits; 5–6 are skipped.'
      : 'Binary: 1–3 become 0; 4–6 become 1.';
    document.dispatchEvent(new CustomEvent('guide:selectionchange', { detail: { length: selectedLength } }));
    updateForwardState();
  }

  function selectStep(step) {
    const stepIndex = stepNumbers.indexOf(step);
    if (stepIndex === -1) return;
    const previousStep = currentStep;
    currentStep = step;
    stepPanels.forEach(panel => panel.classList.toggle('is-active', Number(panel.dataset.stepPanel) === step));
    previous.disabled = step === firstStep;
    progressStep.textContent = step;
    progressTitle.textContent = stepPanels[stepIndex].dataset.stepTitle || titles[step];
    if (!document.body.classList.contains('offline-edition')) {
      progressBar.style.width = `${((stepIndex + 1) / totalSteps) * 100}%`;
    }
    document.body.dataset.stepIndex = String(stepIndex); // CSS fallback for offline progress bar
    updateSelections();
    updateForwardState();
    document.dispatchEvent(new CustomEvent('guide:stepchange', { detail: { previousStep, step } }));
    window.scrollTo({ top: 0, behavior: 'smooth' });
  }

  document.querySelector('.start-guide').addEventListener('click', () => {
    document.body.classList.add('wizard-active');
    selectStep(firstStep);
  });
  previous.addEventListener('click', () => {
    const stepIndex = stepNumbers.indexOf(currentStep);
    selectStep(stepNumbers[Math.max(0, stepIndex - 1)]);
  });
  next.addEventListener('click', () => {
    updateForwardState();
    if (next.disabled) return;
    if (currentStep === lastStep) {
      resetCheckpointsFrom(firstStep);
      selectStep(firstStep);
      return;
    }
    const stepIndex = stepNumbers.indexOf(currentStep);
    selectStep(stepNumbers[stepIndex + 1]);
  });

  document.querySelectorAll('.toggle').forEach(toggle => {
    toggle.addEventListener('click', () => {
      if (!toggle.dataset.length) return;
      const length = Number(toggle.dataset.length);
      if (selectedLength !== length) resetCheckpointsFrom(2);
      selectedLength = length;
      document.querySelectorAll('.toggle').forEach(button => {
        const active = button.dataset.length && button === toggle;
        if (button.dataset.length) {
          button.classList.toggle('is-selected', active);
          button.setAttribute('aria-pressed', String(active));
        }
      });
      updateSelections();
    });
  });

  document.querySelectorAll('[data-dice]').forEach(button => {
    button.addEventListener('click', () => {
      if (selectedDice !== button.dataset.dice) {
        resetCheckpoint('dice');
        resetCheckpointsAfter(1);
      }
      selectedDice = button.dataset.dice;
      document.querySelectorAll('[data-dice]').forEach(choice => {
        const active = choice === button;
        choice.classList.toggle('is-selected', active);
        choice.setAttribute('aria-pressed', String(active));
      });
      updateSelections();
    });
  });

  document.querySelectorAll('[data-container]').forEach(button => {
    button.addEventListener('click', () => {
      if (selectedContainer !== button.dataset.container) {
        resetCheckpoint('rolling-setup');
        resetCheckpoint('box-clearance');
        resetCheckpointsAfter(1);
      }
      selectedContainer = button.dataset.container;
      document.querySelectorAll('[data-container]').forEach(choice => {
        const active = choice === button;
        choice.classList.toggle('is-selected', active);
        choice.setAttribute('aria-pressed', String(active));
      });
      updateSelections();
    });
  });

  document.querySelectorAll('.encoding-tab').forEach(tab => {
    tab.addEventListener('click', () => {
      const selected = tab.dataset.encoding;
      if (selectedEncoding !== selected) resetCheckpointsFrom(2);
      document.querySelectorAll('.encoding-tab').forEach(button => {
        const active = button === tab;
        button.classList.toggle('is-selected', active);
        button.setAttribute('aria-selected', String(active));
      });
      document.querySelectorAll('[data-encoding-panel]').forEach(panel => {
        panel.classList.toggle('is-visible', panel.dataset.encodingPanel === selected);
      });
      selectedEncoding = selected;
      updateSelections();
    });
  });
  document.querySelectorAll('input[type="checkbox"]').forEach(check => {
    check.addEventListener('change', updateForwardState);
  });
  setupRollingEntryVisuals();
  updateSelections();
  if (document.body.classList.contains('offline-edition')) selectStep(firstStep);
})();

// evaluate.js - measures ScamFree's classifier on emails it has never seen.
// Put this file in the ScamFree folder and run:  node evaluate.js
// It shuffles your labeled emails, trains on 80%, tests on the other 20%,
// and prints accuracy, precision and recall.

const natural = require('natural');
const { loadEmails } = require('./CSV_Parser');

function shuffle(arr) {
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1));
    [arr[i], arr[j]] = [arr[j], arr[i]];
  }
  return arr;
}

async function evaluate() {
  const emails = shuffle(await loadEmails('./123.csv'));
  const split = Math.floor(emails.length * 0.8);
  const train = emails.slice(0, split);
  const test = emails.slice(split);

  const classifier = new natural.BayesClassifier();
  for (const e of train) classifier.addDocument(e.text, e.label);
  classifier.train();

  let tp = 0, fp = 0, tn = 0, fn = 0;
  for (const e of test) {
    const predicted = classifier.classify(e.text);
    const actualSpam = e.label === 'Spam';
    const predictedSpam = predicted === 'Spam';
    if (predictedSpam && actualSpam) tp++;
    else if (predictedSpam && !actualSpam) fp++;
    else if (!predictedSpam && !actualSpam) tn++;
    else fn++;
  }

  const pct = (x) => (x * 100).toFixed(1) + '%';
  console.log(`Emails loaded: ${emails.length} (trained on ${train.length}, tested on ${test.length})`);
  console.log(`Accuracy:  ${pct((tp + tn) / test.length)}   (correct labels overall)`);
  console.log(`Precision: ${pct(tp / (tp + fp || 1))}   (flagged emails that really were spam)`);
  console.log(`Recall:    ${pct(tp / (tp + fn || 1))}   (spam emails it caught)`);
}

evaluate().catch((err) => console.error(err));

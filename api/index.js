// api/index.js

const querystring = require('querystring');
const got = require('got');
const safeEval = require('safe-eval');
const token = require('google-translate-token');

const languages = require('./languages');

function translate(text, opts) {
  opts = opts || {};

  let e;
  [opts.from, opts.to].forEach((lang) => {
    if (lang && !languages.isSupported(lang)) {
      e = new Error();
      e.code = 400;
      e.message = `The language '${lang}' is not supported`;
    }
  });
  if (e) {
    return Promise.reject(e);
  }

  opts.from = opts.from || 'auto';
  opts.to = opts.to || 'en';

  opts.from = languages.getCode(opts.from);
  opts.to = languages.getCode(opts.to);

  return token.get(text)
    .then((token) => {
      const url = 'https://translate.google.com/translate_a/single';
      const data = {
        client: 't',
        sl: opts.from,
        tl: opts.to,
        hl: opts.to,
        dt: ['at', 'bd', 'ex', 'ld', 'md', 'qca', 'rw', 'rm', 'ss', 't'],
        ie: 'UTF-8',
        oe: 'UTF-8',
        otf: 1,
        ssel: 0,
        tsel: 0,
        kc: 7,
        q: text
      };
      data[token.name] = token.value;

      return `${url}?${querystring.stringify(data)}`;
    })
    .then((url) => {
      return got(url).then((res) => {
        const result = {
          text: '',
          from: {
            language: {
              didYouMean: false,
              iso: ''
            },
            text: {
              autoCorrected: false,
              value: '',

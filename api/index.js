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
              didYouMean: false
            }
          },
          raw: ''
        };

        var body = safeEval(res.body);

        body[0].forEach((obj) => {
          if (obj[0]) {
            result.text += obj[0];
          }
        });

        if (body[2] === body[8][0][0]) {
          result.from.language.iso = body[2];
        } else {
          result.from.language.didYouMean = true;
          result.from.language.iso = body[8][0][0];
        }

        if (body[7] && body[7][0]) {
          let str = body[7][0];
          str = str.replace(/<b><i>/g, '[').replace(/<\/i><\/b>/g, ']');

          result.from.text.value = str;
          if (body[7][5] === true) {
            result.from.text.autoCorrected = true;
          } else {
            result.from.text.didYouMean = true;
          }
        }

        return result;
      });
    });
}

export default async function handler(req, res) {
  const { text, from, to } = req.query;

  if (!text) {
    return res.status(400).json({ error: 'Missing `text` parameter' });
  }

  try {
    const result = await translate(text, { from, to });
    return res.status(200).json(result);
  } catch (err) {
    console.error(err);
    return res.status(500).json({ error: err.message || 'Internal error' });
  }
}

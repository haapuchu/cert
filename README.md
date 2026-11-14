# certificate editor

simple tool to change the name and date on the certificate in the same font and export as pdf.

## how to run

run the app:

```
python app.py
```

open your browser at:

```
http://localhost:8000
```

## deploying on netlify

the site is fully static and works on netlify with no server. `netlify.toml` publishes the `static` folder,
and the pdf is built in the browser with [pdf-lib](https://pdf-lib.js.org) (vendored in `static/vendor`).

the browser starts from two pre-redacted copies of `template_certificate.pdf`:

- `static/template_name.pdf`: original name removed, original date kept.
- `static/template_name_date.pdf`: original name and date removed.

if `template_certificate.pdf` ever changes, regenerate both files with the same redaction areas used in `certificate_engine.py`.

## features

- changes recipient name in roboto font (default: mtu skthu).
- changes issue date in roboto font (default: 13 november 2026).
- keeps all other certificate parts intact.
- small pdf file size (~350 kb).
- downloads as certificate.pdf.
- simple responsive layout for mobile and desktop.

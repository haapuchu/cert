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

## netlify

the site is fully static on netlify. `netlify.toml` publishes the `static` folder, and the pdf is built in the browser with pdf-lib (bundled in `static/vendor`). `template_noname.pdf` and `template_blank.pdf` are copies of the template with the original name (and date) already redacted.

## features

- changes recipient name in roboto font (default: mtu skthu).
- changes issue date in roboto font (default: 13 november 2026).
- keeps all other certificate parts intact.
- small pdf file size (~350 kb).
- downloads as certificate.pdf.
- simple responsive layout for mobile and desktop.

const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const nameInput = document.getElementById('name');
const dateInput = document.getElementById('date');
const datePicker = document.getElementById('datePicker');
const pdfBtn = document.getElementById('pdfBtn');

const scale = 300 / 72;
const img = new Image();

const months = [
  'January', 'February', 'March', 'April', 'May', 'June',
  'July', 'August', 'September', 'October', 'November', 'December'
];

// Coordinates
const nameX = 40.0 * scale;
const nameY = 308.280029296875 * scale;
const dateX = 611.6500244140625 * scale;
const dateY = 510.280029296875 * scale;

// Draw text on canvas
function draw() {
  if (!img.complete) return;
  ctx.clearRect(0, 0, canvas.width, canvas.height);
  ctx.drawImage(img, 0, 0);

  ctx.fillStyle = '#000';
  ctx.textBaseline = 'alphabetic';
  ctx.textAlign = 'left';

  // Draw name (Roboto 20pt)
  const name = nameInput.value.trim();
  if (name) {
    ctx.font = `${20 * scale}px Roboto, sans-serif`;
    ctx.fillText(name, nameX, nameY);
  }

  // Draw date (Roboto 14pt)
  const date = dateInput.value.trim();
  if (date) {
    ctx.fillStyle = '#ffffff';
    ctx.fillRect(605 * scale, 490 * scale, 200 * scale, 30 * scale);

    ctx.fillStyle = '#000000';
    ctx.font = `${14 * scale}px Roboto, sans-serif`;
    ctx.fillText(date, dateX, dateY);
  }
}

img.onload = draw;
img.src = 'template_clean.png';

document.fonts.ready.then(draw);

nameInput.addEventListener('input', draw);
dateInput.addEventListener('input', draw);

// When a date is chosen from calendar, format to "DD MMMM YYYY"
datePicker.addEventListener('change', (e) => {
  if (!e.target.value) return;
  const parts = e.target.value.split('-');
  if (parts.length === 3) {
    const y = parts[0];
    const m = months[parseInt(parts[1], 10) - 1];
    const d = parseInt(parts[2], 10);
    dateInput.value = `${d} ${m} ${y}`;
    draw();
  }
});

// Download helper
function download(url, filename) {
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Build the PDF in the browser from the pre-redacted templates
const DEFAULT_NAME = 'mtu skthu';
const DEFAULT_DATE = '13 November 2026';
const assetCache = {};

async function loadAsset(url) {
  if (!assetCache[url]) {
    assetCache[url] = fetch(url).then((res) => {
      if (!res.ok) throw new Error(`failed to load ${url}`);
      return res.arrayBuffer();
    });
  }
  return assetCache[url];
}

async function buildPdf(rawName, rawDate) {
  const { PDFDocument, rgb } = PDFLib;
  const name = (rawName || '').trim() || DEFAULT_NAME;
  const date = (rawDate || '').trim() || DEFAULT_DATE;
  const replaceDate = date !== DEFAULT_DATE;

  const [templateBytes, fontBytes] = await Promise.all([
    loadAsset(replaceDate ? 'template_name_date.pdf' : 'template_name.pdf'),
    loadAsset('Roboto-Regular.ttf')
  ]);

  const doc = await PDFDocument.load(templateBytes);
  doc.registerFontkit(fontkit);
  const font = await doc.embedFont(fontBytes, { subset: true });
  const page = doc.getPage(0);
  const height = page.getHeight();
  const black = rgb(0, 0, 0);

  page.drawText(name, { x: 40.0, y: height - 308.28, size: 20, font, color: black });
  if (replaceDate) {
    page.drawText(date, { x: 611.65, y: height - 510.28, size: 14, font, color: black });
  }

  return doc.save();
}

// Download PDF
pdfBtn.addEventListener('click', async () => {
  pdfBtn.disabled = true;
  pdfBtn.textContent = 'downloading...';
  try {
    const bytes = await buildPdf(nameInput.value, dateInput.value);
    const blob = new Blob([bytes], { type: 'application/pdf' });
    const url = URL.createObjectURL(blob);
    download(url, 'certificate.pdf');
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  } catch (err) {
    console.error(err);
    alert('error creating pdf');
  } finally {
    pdfBtn.disabled = false;
    pdfBtn.textContent = 'download pdf';
  }
});

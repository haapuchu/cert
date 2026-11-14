const canvas = document.getElementById('canvas');
const ctx = canvas.getContext('2d');

const nameInput = document.getElementById('name');
const dateInput = document.getElementById('date');
const pdfBtn = document.getElementById('pdfBtn');

const scale = 300 / 72;
const img = new Image();

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

// Download helper
function download(url, filename) {
  const a = document.createElement('a');
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  document.body.removeChild(a);
}

// Download PDF
pdfBtn.addEventListener('click', async () => {
  pdfBtn.disabled = true;
  pdfBtn.textContent = 'downloading...';
  try {
    const res = await fetch('/api/export/pdf', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        name: nameInput.value,
        date: dateInput.value
      })
    });
    const blob = await res.blob();
    const url = URL.createObjectURL(blob);
    download(url, 'certificate.pdf');
    URL.revokeObjectURL(url);
  } catch (err) {
    alert('error downloading pdf');
  } finally {
    pdfBtn.disabled = false;
    pdfBtn.textContent = 'download pdf';
  }
});

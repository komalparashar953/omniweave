document.addEventListener('DOMContentLoaded', () => {
    const urlInput = document.getElementById('urlInput');
    const scrapeBtn = document.getElementById('scrapeBtn');
    const loadingDiv = document.getElementById('loading');
    const errorDiv = document.getElementById('error');
    const resultDiv = document.getElementById('result');
    const sectionsDiv = document.getElementById('sections');
    const downloadBtn = document.getElementById('downloadBtn');
    const metaInfoDiv = document.querySelector('.meta-info');

    let currentResult = null;

    scrapeBtn.addEventListener('click', async () => {
        const url = urlInput.value.trim();
        if (!url) return;

        // Reset UI
        errorDiv.classList.add('hidden');
        resultDiv.classList.add('hidden');
        loadingDiv.classList.remove('hidden');
        sectionsDiv.innerHTML = '';
        currentResult = null;

        try {
            const response = await fetch('/scrape', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ url })
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.detail || 'Failed to scrape URL');
            }

            currentResult = data.result;
            renderResult(currentResult);

        } catch (err) {
            errorDiv.textContent = err.message;
            errorDiv.classList.remove('hidden');
        } finally {
            loadingDiv.classList.add('hidden');
        }
    });

    downloadBtn.addEventListener('click', () => {
        if (!currentResult) return;
        const blob = new Blob([JSON.stringify({ result: currentResult }, null, 2)], { type: 'application/json' });
        const url = URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.href = url;
        a.download = `scrape-result-${Date.now()}.json`;
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    });

    function renderResult(result) {
        resultDiv.classList.remove('hidden');

        // Render Meta
        metaInfoDiv.innerHTML = `
            <h3>${result.meta.title || 'No Title'}</h3>
            <p>${result.meta.description || ''}</p>
            <p><strong>Scraped At:</strong> ${new Date(result.scrapedAt).toLocaleString()}</p>
            <p><strong>Sections:</strong> ${result.sections.length} | <strong>Interactions:</strong> Scrolls: ${result.interactions.scrolls}, Pages: ${result.interactions.pages.length}</p>
        `;

        // Render Sections
        result.sections.forEach(section => {
            const sectionEl = document.createElement('div');
            sectionEl.className = 'section-item';

            const header = document.createElement('div');
            header.className = 'section-header';
            header.innerHTML = `
                <span>
                    <span class="label-badge">${section.label}</span>
                    <span class="type-badge">${section.type}</span>
                </span>
                <span>+</span>
            `;

            const content = document.createElement('div');
            content.className = 'section-content';
            content.innerHTML = `<div class="json-view">${JSON.stringify(section, null, 2)}</div>`;

            header.addEventListener('click', () => {
                content.classList.toggle('open');
                header.querySelector('span:last-child').textContent = content.classList.contains('open') ? '-' : '+';
            });

            sectionEl.appendChild(header);
            sectionEl.appendChild(content);
            sectionsDiv.appendChild(sectionEl);
        });
    }
});

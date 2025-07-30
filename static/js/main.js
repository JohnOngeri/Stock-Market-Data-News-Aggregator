document.addEventListener('DOMContentLoaded', () => {
    const fetchDataBtn = document.getElementById('fetchData');
    const stockSymbolsInput = document.getElementById('stockSymbols');
    const stockTableContainer = document.getElementById('stockTable');
    const newsArticlesContainer = document.getElementById('newsArticles');
    const errorsContainer = document.getElementById('errors');

    if (fetchDataBtn) {
        fetchDataBtn.addEventListener('click', async () => {
            const symbols = stockSymbolsInput.value.trim();
            if (!symbols) {
                displayError('Please enter at least one stock symbol.');
                return;
            }

            // Clear previous data and errors
            clearContent();
            setLoading(true);

            try {
                const response = await fetch('/get_stock_data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ symbols }),
                });

                if (!response.ok) {
                    const errorData = await response.json();
                    throw new Error(errorData.error || `HTTP error! status: ${response.status}`);
                }

                const data = await response.json();
                displayStockData(data.stock_data);
                displayNewsData(data.news_data);

            } catch (error) {
                displayError(`Failed to fetch data: ${error.message}`);
            } finally {
                setLoading(false);
            }
        });
    }

    function displayError(message) {
        errorsContainer.innerHTML = `<p>${message}</p>`;
    }

    function clearContent() {
        errorsContainer.innerHTML = '';
        stockTableContainer.innerHTML = '';
        newsArticlesContainer.innerHTML = '';
    }

    function setLoading(isLoading) {
        fetchDataBtn.disabled = isLoading;
        if (isLoading) {
            stockTableContainer.innerHTML = '<p class="loading">Loading stock data...</p>';
            newsArticlesContainer.innerHTML = '<p class="loading">Loading news...</p>';
        }
    }

    function displayStockData(stockData) {
        if (!stockData || stockData.length === 0) {
            stockTableContainer.innerHTML = '<p class="no-data">No stock data available for the given symbols.</p>';
            return;
        }

        const table = document.createElement('table');
        table.innerHTML = `
            <thead>
                <tr>
                    <th>Symbol</th>
                    <th>Price</th>
                    <th>Change</th>
                    <th>Volume</th>
                </tr>
            </thead>
            <tbody>
                ${stockData.map(stock => `
                    <tr>
                        <td>${stock.symbol}</td>
                        <td>${stock.price}</td>
                        <td class="${parseFloat(stock.change) >= 0 ? 'positive' : 'negative'}">${stock.change}</td>
                        <td>${stock.volume}</td>
                    </tr>
                `).join('')}
            </tbody>
        `;
        stockTableContainer.appendChild(table);
    }

    function displayNewsData(newsData) {
        if (!newsData || newsData.length === 0) {
            newsArticlesContainer.innerHTML = '<p class="no-data">No news articles found.</p>';
            return;
        }

        newsArticlesContainer.innerHTML = newsData.map(article => `
            <div class="news-article">
                <h3><a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title}</a></h3>
                <p class="article-description">${article.description || ''}</p>
                <p class="article-date">${article.publishedAt ? `Published: ${new Date(article.publishedAt).toLocaleString()}` : ''}</p>
            </div>
        `).join('');
    }
});
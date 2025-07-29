document.getElementById('fetchData').addEventListener('click', fetchData);

async function fetchData() {
    const stockSymbols = document.getElementById('stockSymbols').value;
    const stockTableBody = document.querySelector('#stockTable tbody');
    const newsArticlesDiv = document.getElementById('newsArticles');
    const errorsDiv = document.getElementById('errors');

    stockTableBody.innerHTML = ''; // Clear previous data
    newsArticlesDiv.innerHTML = '';
    errorsDiv.innerHTML = '';

    if (!stockSymbols.trim()) {
        errorsDiv.textContent = "Please enter at least one stock symbol.";
        return;
    }

    try {
        const response = await fetch('/get_stock_data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ symbols: stockSymbols })
        });
        
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();

        if (data.errors && data.errors.length > 0) {
            errorsDiv.innerHTML = data.errors.map(err => `<p>${err}</p>`).join('');
        }

        // Display Stock Data
        if (data.stock_data && data.stock_data.length > 0) {
            data.stock_data.forEach(stock => {
                const row = stockTableBody.insertRow();
                row.insertCell().textContent = stock.symbol;
                row.insertCell().textContent = parseFloat(stock.price).toFixed(2);
                const changeCell = row.insertCell();
                const change = parseFloat(stock.change);
                changeCell.textContent = change.toFixed(2);
                changeCell.style.color = change >= 0 ? 'green' : 'red';
                row.insertCell().textContent = parseInt(stock.volume).toLocaleString();
            });
        } else if (data.errors.length === 0) {
            stockTableBody.innerHTML = '<tr><td colspan="4">No stock data found for the entered symbols.</td></tr>';
        }


        // Display News Articles
        if (data.news_data && data.news_data.length > 0) {
            data.news_data.forEach(news => {
                const articleDiv = document.createElement('div');
                articleDiv.classList.add('news-article');
                articleDiv.innerHTML = `
                    <h3><a href="${news.url}" target="_blank">${news.title}</a></h3>
                    <p>${news.description || 'No description available.'}</p>
                `;
                newsArticlesDiv.appendChild(articleDiv);
            });
        } else if (data.errors.length === 0) {
            newsArticlesDiv.innerHTML = '<p>No news articles found for the entered symbols.</p>';
        }

    } catch (error) {
        console.error('Error fetching data:', error);
        errorsDiv.textContent = `An unexpected error occurred: ${error.message}`;
    }
}
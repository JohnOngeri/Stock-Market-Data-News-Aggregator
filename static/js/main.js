// Global variables to store data
let stockData = [];
let newsData = [];
let currentSortColumn = 'symbol';
let currentSortDirection = 'asc';

// Event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the application
    setupEventListeners();
    loadDefaultData();
});

function setupEventListeners() {
    // Main data fetching
    document.getElementById('fetchData').addEventListener('click', fetchData);
    document.getElementById('stockSymbols').addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            fetchData();
        }
    });

    // Stock controls
    document.getElementById('stockSearch').addEventListener('input', debounce(filterStocks, 300));
    document.getElementById('stockSort').addEventListener('change', sortStocks);
    document.getElementById('refreshStocks').addEventListener('click', () => {
        if (stockData.length > 0) {
            displayStockData(stockData);
        }
    });

    // News controls
    document.getElementById('newsSearch').addEventListener('input', debounce(filterNews, 300));
    document.getElementById('newsFilter').addEventListener('change', filterNews);
    document.getElementById('refreshNews').addEventListener('click', () => {
        if (newsData.length > 0) {
            displayNewsData(newsData);
        }
    });

    // Table header sorting
    document.querySelectorAll('#stockTable th[data-sort]').forEach(header => {
        header.addEventListener('click', () => {
            const sortBy = header.getAttribute('data-sort');
            sortStocksByColumn(sortBy);
        });
    });

    // Add keyboard navigation
    document.addEventListener('keydown', handleKeyboardNavigation);
}

function loadDefaultData() {
    // Load some default popular stocks for better UX
    const defaultSymbols = 'AAPL,MSFT,GOOGL,AMZN,TSLA';
    document.getElementById('stockSymbols').value = defaultSymbols;
    fetchData();
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function handleKeyboardNavigation(e) {
    // Ctrl/Cmd + Enter to fetch data
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        e.preventDefault();
        fetchData();
    }
}

async function fetchData() {
    const stockSymbols = document.getElementById('stockSymbols').value;
    const stockTableBody = document.querySelector('#stockTable tbody');
    const newsArticlesDiv = document.getElementById('newsArticles');
    const errorsDiv = document.getElementById('errors');
    const fetchButton = document.getElementById('fetchData');

    // Clear previous data
    stockTableBody.innerHTML = '';
    newsArticlesDiv.innerHTML = '';
    errorsDiv.innerHTML = '';
    stockData = [];
    newsData = [];

    if (!stockSymbols.trim()) {
        showError("Please enter at least one stock symbol.");
        return;
    }

    // Validate input format
    const symbols = stockSymbols.split(',').map(s => s.trim()).filter(s => s);
    if (symbols.length > 10) {
        showError("Maximum 10 stock symbols allowed.");
        return;
    }

    // Show loading state
    setLoadingState(true);

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

        // Handle errors
        if (data.errors && data.errors.length > 0) {
            showErrors(data.errors);
        }

        // Store and display stock data
        if (data.stock_data && data.stock_data.length > 0) {
            stockData = data.stock_data;
            displayStockData(stockData);
        } else if (!data.errors || data.errors.length === 0) {
            stockTableBody.innerHTML = '<tr><td colspan="4" class="no-data">No stock data found for the entered symbols.</td></tr>';
        }

        // Store and display news data
        if (data.news_data && data.news_data.length > 0) {
            newsData = data.news_data;
            displayNewsData(newsData);
        } else if (!data.errors || data.errors.length === 0) {
            newsArticlesDiv.innerHTML = '<p class="no-data">No news articles found for the entered symbols.</p>';
        }

    } catch (error) {
        console.error('Error fetching data:', error);
        showError(`Failed to fetch data: ${error.message}`);
    } finally {
        setLoadingState(false);
    }
}

function setLoadingState(loading) {
    const fetchButton = document.getElementById('fetchData');
    const stockTableBody = document.querySelector('#stockTable tbody');
    const newsArticlesDiv = document.getElementById('newsArticles');

    if (loading) {
        fetchButton.disabled = true;
        fetchButton.textContent = 'Loading...';
        stockTableBody.innerHTML = '<tr><td colspan="4" class="loading">Loading stock data...</td></tr>';
        newsArticlesDiv.innerHTML = '<p class="loading">Loading news articles...</p>';
    } else {
        fetchButton.disabled = false;
        fetchButton.textContent = 'Fetch Data';
    }
}

function showError(message) {
    const errorsDiv = document.getElementById('errors');
    errorsDiv.innerHTML = `<p class="error">${message}</p>`;
    errorsDiv.scrollIntoView({ behavior: 'smooth' });
}

function showErrors(errors) {
    const errorsDiv = document.getElementById('errors');
    errorsDiv.innerHTML = errors.map(err => `<p class="error">${err}</p>`).join('');
    errorsDiv.scrollIntoView({ behavior: 'smooth' });
}

function displayStockData(data) {
    const tbody = document.querySelector('#stockTable tbody');
    tbody.innerHTML = '';

    data.forEach(stock => {
        const row = document.createElement('tr');
        const change = parseFloat(stock.change || 0);
        const changeClass = change >= 0 ? 'positive' : 'negative';
        const changeSymbol = change >= 0 ? '+' : '';

        row.innerHTML = `
            <td>${stock.symbol || 'N/A'}</td>
            <td>$${parseFloat(stock.price || 0).toFixed(2)}</td>
            <td class="${changeClass}">${changeSymbol}${change.toFixed(2)}</td>
            <td>${formatVolume(stock.volume)}</td>
        `;
        tbody.appendChild(row);
    });
}

function displayNewsData(data) {
    const newsDiv = document.getElementById('newsArticles');
    newsDiv.innerHTML = '';

    data.forEach(article => {
        const articleDiv = document.createElement('div');
        articleDiv.className = 'news-article';
        
        const publishedDate = article.publishedAt ? new Date(article.publishedAt).toLocaleDateString() : 'Unknown date';
        
        articleDiv.innerHTML = `
            <h3><a href="${article.url}" target="_blank" rel="noopener noreferrer">${article.title || 'No title'}</a></h3>
            <p class="article-description">${article.description || 'No description available'}</p>
            <p class="article-date">Published: ${publishedDate}</p>
        `;
        newsDiv.appendChild(articleDiv);
    });
}

function formatVolume(volume) {
    if (!volume) return 'N/A';
    const num = parseInt(volume);
    if (num >= 1000000) {
        return (num / 1000000).toFixed(1) + 'M';
    } else if (num >= 1000) {
        return (num / 1000).toFixed(1) + 'K';
    }
    return num.toLocaleString();
}

function filterStocks() {
    const searchTerm = document.getElementById('stockSearch').value.toLowerCase();
    const filteredData = stockData.filter(stock => 
        stock.symbol.toLowerCase().includes(searchTerm) ||
        stock.price.toString().includes(searchTerm)
    );
    displayStockData(filteredData);
}

function sortStocks() {
    const sortBy = document.getElementById('stockSort').value;
    const sortedData = [...stockData].sort((a, b) => {
        let aVal, bVal;
        
        switch(sortBy) {
            case 'symbol':
                aVal = a.symbol || '';
                bVal = b.symbol || '';
                return aVal.localeCompare(bVal);
            case 'price':
                aVal = parseFloat(a.price || 0);
                bVal = parseFloat(b.price || 0);
                return aVal - bVal;
            case 'change':
                aVal = parseFloat(a.change || 0);
                bVal = parseFloat(b.change || 0);
                return aVal - bVal;
            case 'volume':
                aVal = parseInt(a.volume || 0);
                bVal = parseInt(b.volume || 0);
                return aVal - bVal;
            default:
                return 0;
        }
    });
    
    displayStockData(sortedData);
}

function sortStocksByColumn(column) {
    const headers = document.querySelectorAll('#stockTable th[data-sort]');
    
    // Update sort direction
    if (currentSortColumn === column) {
        currentSortDirection = currentSortDirection === 'asc' ? 'desc' : 'asc';
    } else {
        currentSortColumn = column;
        currentSortDirection = 'asc';
    }
    
    // Update header indicators
    headers.forEach(header => {
        const headerColumn = header.getAttribute('data-sort');
        if (headerColumn === column) {
            header.textContent = `${headerColumn.charAt(0).toUpperCase() + headerColumn.slice(1)} ${currentSortDirection === 'asc' ? '↑' : '↓'}`;
        } else {
            header.textContent = `${headerColumn.charAt(0).toUpperCase() + headerColumn.slice(1)} ↕`;
        }
    });
    
    // Sort data
    const sortedData = [...stockData].sort((a, b) => {
        let aVal, bVal;
        
        switch(column) {
            case 'symbol':
                aVal = a.symbol || '';
                bVal = b.symbol || '';
                return currentSortDirection === 'asc' ? aVal.localeCompare(bVal) : bVal.localeCompare(aVal);
            case 'price':
                aVal = parseFloat(a.price || 0);
                bVal = parseFloat(b.price || 0);
                return currentSortDirection === 'asc' ? aVal - bVal : bVal - aVal;
            case 'change':
                aVal = parseFloat(a.change || 0);
                bVal = parseFloat(b.change || 0);
                return currentSortDirection === 'asc' ? aVal - bVal : bVal - aVal;
            case 'volume':
                aVal = parseInt(a.volume || 0);
                bVal = parseInt(b.volume || 0);
                return currentSortDirection === 'asc' ? aVal - bVal : bVal - aVal;
            default:
                return 0;
        }
    });
    
    displayStockData(sortedData);
}

function filterNews() {
    const searchTerm = document.getElementById('newsSearch').value.toLowerCase();
    const filterValue = document.getElementById('newsFilter').value;
    
    let filteredData = newsData.filter(article => {
        const matchesSearch = article.title.toLowerCase().includes(searchTerm) ||
                            article.description.toLowerCase().includes(searchTerm);
        
        if (filterValue === 'all') {
            return matchesSearch;
        }
        
        // Simple keyword-based filtering
        const title = article.title.toLowerCase();
        const description = article.description.toLowerCase();
        
        switch(filterValue) {
            case 'market':
                return matchesSearch && (title.includes('market') || description.includes('market'));
            case 'tech':
                return matchesSearch && (title.includes('tech') || title.includes('technology') || 
                                       description.includes('tech') || description.includes('technology'));
            case 'finance':
                return matchesSearch && (title.includes('finance') || title.includes('financial') || 
                                       description.includes('finance') || description.includes('financial'));
            default:
                return matchesSearch;
        }
    });
    
    displayNewsData(filteredData);
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        fetchData,
        displayStockData,
        displayNewsData,
        filterStocks,
        sortStocks,
        filterNews,
        formatVolume
    };
}
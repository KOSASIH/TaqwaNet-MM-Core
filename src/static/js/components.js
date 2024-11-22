import { debounce, fetchData } from './script.js';

// Component: Modal
class Modal {
    constructor(modalSelector) {
        this.modal = document.querySelector(modalSelector);
        this.closeButton = this.modal.querySelector('.close');
        this.init();
    }

    init() {
        this.closeButton.addEventListener('click', () => this.close());
        window.addEventListener('click', (event) => {
            if (event.target === this.modal) {
                this.close();
            }
        });
    }

    open() {
        this.modal.style.display = 'block';
    }

    close() {
        this.modal.style.display = 'none';
    }
}

// Component: Infinite Scroll
class InfiniteScroll {
    constructor(containerSelector, apiUrl) {
        this.container = document.querySelector(containerSelector);
        this.apiUrl = apiUrl;
        this.page = 1;
        this.loading = false;
        this.init();
    }

    async init() {
        window.addEventListener('scroll', debounce(() => this.onScroll(), 200));
        await this.loadMore();
    }

    async onScroll() {
        if (window.innerHeight + window.scrollY >= document.body.offsetHeight - 500 && !this.loading) {
            await this.loadMore();
        }
    }

    async loadMore() {
        this.loading = true;
        try {
            const data = await fetchData(`${this.apiUrl}?page=${this.page}`);
            this.render(data);
            this.page++;
        } catch (error) {
            console.error('Error loading more data:', error);
        } finally {
            this.loading = false;
        }
    }

    render(data) {
        data.forEach(item => {
            const div = document.createElement('div');
            div.className = 'item';
            div.innerText = item.title; // Assuming the data has a title property
            this.container.appendChild(div);
        });
    }
}

// Initialize components
document.addEventListener('DOMContentLoaded', () => {
    const modal = new Modal('#myModal');
    const infiniteScroll = new InfiniteScroll('#itemContainer', 'https://api.example.com/items');
});

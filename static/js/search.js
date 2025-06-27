

document.addEventListener('DOMContentLoaded', function() {
    // Elements
    const queryInput = document.getElementById('query');
    const stateSelect = document.getElementById('state');
    const cityInput = document.getElementById('city');
    
    if (queryInput) {
        queryInput.focus();
    }
    
    const clearFormButton = document.getElementById('clear-form');
    if (clearFormButton) {
        clearFormButton.addEventListener('click', function(e) {
            e.preventDefault();
            
            if (queryInput) queryInput.value = '';
            if (stateSelect) stateSelect.value = '';
            if (cityInput) cityInput.value = '';
            
            if (window.location.pathname.includes('/search')) {
                window.location.href = '/search';
            }
        });
    }
    
    if (stateSelect && cityInput) {
        stateSelect.addEventListener('change', function() {
            const selectedState = this.value;
            
            if (selectedState) {
                console.log('State selected:', selectedState);
            
            }
        });
    }
    
    const resultItems = document.querySelectorAll('.list-group-item');
    resultItems.forEach((item, index) => {
        item.setAttribute('tabindex', '0');
        
        item.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                this.click();
            }
        });
        
        item.addEventListener('mouseenter', function() {
            this.classList.add('active');
        });
        
        item.addEventListener('mouseleave', function() {
            this.classList.remove('active');
        });
    });
});
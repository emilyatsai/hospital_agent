// Kidney Stone Predictor - JavaScript functionality

document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    const tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Form validation and enhancement
    const predictionForm = document.getElementById('predictionForm');
    if (predictionForm) {
        setupFormValidation(predictionForm);
        setupInputFormatting();
        setupSampleDataLoader();
    }

    // Initialize any charts or visualizations
    initializeCharts();
});

// Form validation setup
function setupFormValidation(form) {
    form.addEventListener('submit', function(e) {
        const inputs = form.querySelectorAll('input[required]');
        let isValid = true;
        let firstInvalidInput = null;

        inputs.forEach(input => {
            if (!validateInput(input)) {
                isValid = false;
                if (!firstInvalidInput) {
                    firstInvalidInput = input;
                }
            }
        });

        if (!isValid) {
            e.preventDefault();
            firstInvalidInput.focus();
            showAlert('Please correct the highlighted fields.', 'danger');
        } else {
            // Show loading state
            showLoadingState(form);
        }
    });
}

// Input validation
function validateInput(input) {
    const value = input.value.trim();
    const fieldName = input.name;

    // Remove previous validation classes
    input.classList.remove('is-valid', 'is-invalid');

    if (!value) {
        input.classList.add('is-invalid');
        return false;
    }

    // Field-specific validation
    const validations = {
        gravity: { min: 1.000, max: 1.050, step: 0.001 },
        ph: { min: 0, max: 14, step: 0.01 },
        osmo: { min: 0, max: 2000, step: 1 },
        cond: { min: 0, max: 50, step: 0.1 },
        urea: { min: 0, max: 1000, step: 1 },
        calc: { min: 0, max: 20, step: 0.01 }
    };

    if (fieldName in validations) {
        const val = parseFloat(value);
        const rules = validations[fieldName];

        if (isNaN(val) || val < rules.min || val > rules.max) {
            input.classList.add('is-invalid');
            return false;
        }
    }

    input.classList.add('is-valid');
    return true;
}

// Input formatting
function setupInputFormatting() {
    const numberInputs = document.querySelectorAll('input[type="number"]');

    numberInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remove non-numeric characters except decimal point
            this.value = this.value.replace(/[^0-9.]/g, '');

            // Ensure only one decimal point
            const parts = this.value.split('.');
            if (parts.length > 2) {
                this.value = parts[0] + '.' + parts.slice(1).join('');
            }
        });

        input.addEventListener('blur', function() {
            validateInput(this);
        });
    });
}

// Sample data loader
function setupSampleDataLoader() {
    const sampleButtons = document.querySelectorAll('[data-sample]');

    sampleButtons.forEach(button => {
        button.addEventListener('click', function() {
            const sampleType = this.getAttribute('data-sample');
            loadSampleData(sampleType);
        });
    });
}

function loadSampleData(type) {
    const sampleData = {
        normal: {
            gravity: 1.021,
            ph: 4.91,
            osmo: 725,
            cond: 14.0,
            urea: 443,
            calc: 2.45
        },
        high_risk: {
            gravity: 1.034,
            ph: 5.24,
            osmo: 1236,
            cond: 27.3,
            urea: 620,
            calc: 12.68
        },
        moderate: {
            gravity: 1.025,
            ph: 5.77,
            osmo: 698,
            cond: 19.5,
            urea: 354,
            calc: 13.0
        }
    };

    if (sampleData[type]) {
        Object.keys(sampleData[type]).forEach(field => {
            const input = document.querySelector(`input[name="${field}"]`);
            if (input) {
                input.value = sampleData[type][field];
                validateInput(input);
            }
        });

        showAlert(`Loaded ${type.replace('_', ' ')} sample data.`, 'info');
    }
}

// Loading state
function showLoadingState(form) {
    const submitBtn = form.querySelector('button[type="submit"]');
    if (submitBtn) {
        submitBtn.disabled = true;
        submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm me-2" role="status" aria-hidden="true"></span>Analyzing...';
    }
}

// Alert system
function showAlert(message, type = 'info') {
    const alertContainer = document.createElement('div');
    alertContainer.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
    alertContainer.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alertContainer.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;

    document.body.appendChild(alertContainer);

    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (alertContainer.parentNode) {
            alertContainer.remove();
        }
    }, 5000);
}

// Clear form function
function clearForm() {
    const form = document.getElementById('predictionForm');
    if (form) {
        form.reset();
        form.querySelectorAll('.is-valid, .is-invalid').forEach(el => {
            el.classList.remove('is-valid', 'is-invalid');
        });
    }
}

// Initialize charts (if any)
function initializeCharts() {
    // Check if we have chart containers
    const chartContainers = document.querySelectorAll('.chart-container');
    if (chartContainers.length > 0 && typeof Chart !== 'undefined') {
        // Initialize Chart.js charts if needed
        chartContainers.forEach(container => {
            const chartType = container.getAttribute('data-chart-type');
            if (chartType) {
                createChart(container, chartType);
            }
        });
    }
}

// Create chart function (placeholder for future enhancements)
function createChart(container, type) {
    // This would be used for data visualization charts
    console.log(`Creating ${type} chart for ${container.id}`);
}

// API testing function (for development)
function testAPI() {
    const testData = {
        features: {
            gravity: 1.021,
            ph: 4.91,
            osmo: 725,
            cond: 14.0,
            urea: 443,
            calc: 2.45
        }
    };

    fetch('/api/predict', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify(testData)
    })
    .then(response => response.json())
    .then(data => {
        console.log('API Response:', data);
        showAlert(`API Test: ${data.prediction ? 'High Risk' : 'Low Risk'} (${data.confidence}% confidence)`, 'success');
    })
    .catch(error => {
        console.error('API Error:', error);
        showAlert('API test failed. Check console for details.', 'danger');
    });
}

// Export functions for global access
window.clearForm = clearForm;
window.loadSampleData = loadSampleData;
window.testAPI = testAPI;

// Keyboard shortcuts
document.addEventListener('keydown', function(e) {
    // Ctrl/Cmd + Enter to submit form
    if ((e.ctrlKey || e.metaKey) && e.key === 'Enter') {
        const form = document.getElementById('predictionForm');
        if (form) {
            form.dispatchEvent(new Event('submit'));
        }
    }

    // Ctrl/Cmd + L to clear form
    if ((e.ctrlKey || e.metaKey) && e.key === 'l') {
        e.preventDefault();
        clearForm();
    }
});
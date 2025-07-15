document.addEventListener('DOMContentLoaded', function() {
    console.log('assign_modal.js loaded');

    const modalContainer = document.getElementById('assign-modal-container');
    let currentInvitationId = null;

    // Function to show the modal
    function showModal(htmlContent) {
        modalContainer.innerHTML = htmlContent;
        modalContainer.style.display = 'flex';

        // Add event listeners for elements inside the modal once loaded
        const modalContent = modalContainer.querySelector('.modal-content');
        if (modalContent) {
             // Close button
            const closeButton = modalContent.querySelector('.close-modal');
            if (closeButton) {
                closeButton.addEventListener('click', hideModal);
            }

            // Form submission
            const assignForm = modalContent.querySelector('#assign-person-form');
            if (assignForm) {
                assignForm.addEventListener('submit', handleFormSubmit);
            }

            // Filter logic
            setupModalFilters(modalContent);
        }
    }

    // Function to hide the modal
    function hideModal() {
        modalContainer.innerHTML = ''; // Clear content on close
        modalContainer.style.display = 'none';
        currentInvitationId = null;
    }

    // Handle clicks on Assign buttons
    document.querySelectorAll('.assign-btn').forEach(button => {
        button.addEventListener('click', function() {
            currentInvitationId = this.dataset.id;
            // Construct the URL using dataset id
            const url = `/admin/invitations/invitation/assign-form/${currentInvitationId}/`;

            fetch(url)
                .then(response => {
                    if (!response.ok) {
                        throw new Error(`HTTP error! status: ${response.status}`);
                    }
                    return response.text();
                })
                .then(html => {
                    showModal(html);
                })
                .catch(error => {
                    console.error('Error fetching assignment form:', error);
                    alert('Could not load assignment form.');
                });
        });
    });

    // Handle form submission via AJAX
    function handleFormSubmit(event) {
        event.preventDefault();

        if (!currentInvitationId) return;

        const form = event.target;
        const formData = new FormData(form);

        // Add CSRF token
        const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

        // Construct the URL using currentInvitationId
        const url = `/admin/invitations/invitation/submit-assignment/${currentInvitationId}/`;

        fetch(url, {
            method: 'POST',
            headers: {
                'X-CSRFToken': csrfToken,
            },
            body: formData
        })
        .then(response => {
             // Check if response is JSON before parsing
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.indexOf('application/json') !== -1) {
                return response.json().then(data => ({ status: response.status, body: data }));
            } else {
                 // Handle non-JSON response (e.g., HTML error page)
                 return response.text().then(text => {
                     console.error('Received non-JSON response:', text);
                     throw new Error(`Server error: ${response.status} - ${text.substring(0, 100)}...`);
                 });
            }
        })
        .then(({ status, body }) => {
             if (status >= 200 && status < 300) {
                alert(body.message || 'Assignments saved successfully!');
                hideModal();
                // Optional: Reload the page or update the table row if needed
                // window.location.reload();
            } else {
                alert(body.error || 'An error occurred while saving assignments.');
            }
        })
        .catch(error => {
            console.error('Error submitting assignment form:', error);
            alert('An error occurred during submission.');
        });
    }

    // Setup dynamic filtering in the modal
    function setupModalFilters(modalContent) {
        const mandalFilter = modalContent.querySelector('#mandal-filter-modal');
        const areaFilter = modalContent.querySelector('#area-filter-modal');
        const personListContainer = modalContent.querySelector('#person-list-container');
        const giftHandlerSelect = modalContent.querySelector('select[name="gift_handler"]');
        const allPersonLabels = personListContainer ? personListContainer.querySelectorAll('label') : [];

        if (!mandalFilter || !areaFilter || !personListContainer || !giftHandlerSelect) return; // Exit if elements not found

        // Function to update Area dropdown based on selected Mandal
        function updateAreaFilter() {
            const selectedMandal = mandalFilter.value;
            const areas = new Set();

            // Collect unique areas for the selected Mandal from existing person data attributes
            allPersonLabels.forEach(label => {
                const personCheckbox = label.querySelector('input[type="checkbox"]');
                if (personCheckbox) {
                    const personMandal = personCheckbox.dataset.mandal;
                    const personArea = personCheckbox.dataset.area;

                    if (!selectedMandal || personMandal === selectedMandal) {
                        if (personArea) {
                            areas.add(personArea);
                        }
                    }
                }
            });

            // Clear and repopulate Area dropdown
            areaFilter.innerHTML = '<option value="">All</option>'; // Add 'All' option
            Array.from(areas).sort().forEach(area => {
                const option = document.createElement('option');
                option.value = area;
                option.textContent = area;
                areaFilter.appendChild(option);
            });

             // Reset Area filter to 'All' after Mandal change
             areaFilter.value = '';
             // Trigger person list update after updating areas
             filterPersonList();
        }

        // Function to filter person list based on selected Mandal and Area
        function filterPersonList() {
            const selectedMandal = mandalFilter.value;
            const selectedArea = areaFilter.value;
            const giftHandlerOptions = giftHandlerSelect.querySelectorAll('option');

            // Keep track of visible person IDs to update Gift Handler dropdown
            const visiblePersonIds = ['']; // Always include empty for 'Select Gift Handler'

            allPersonLabels.forEach(label => {
                const personCheckbox = label.querySelector('input[type="checkbox"]');
                if (personCheckbox) {
                    const personMandal = personCheckbox.dataset.mandal;
                    const personArea = personCheckbox.dataset.area;

                    const matchMandal = !selectedMandal || personMandal === selectedMandal;
                    const matchArea = !selectedArea || personArea === selectedArea;

                    if (matchMandal && matchArea) {
                        label.style.display = 'block';
                         visiblePersonIds.push(personCheckbox.value);
                    } else {
                        label.style.display = 'none';
                        personCheckbox.checked = false; // Uncheck if hidden
                    }
                }
            });

             // Update Gift Handler dropdown based on visible persons
             giftHandlerOptions.forEach(option => {
                // Keep 'Select Gift Handler' option visible
                if (option.value === '') {
                    option.style.display = '';
                } else {
                   option.style.display = visiblePersonIds.includes(option.value) ? '' : 'none';
                }
             });

             // If the currently selected gift handler is now hidden, reset the dropdown
             if(giftHandlerSelect.value && !visiblePersonIds.includes(giftHandlerSelect.value)) {
                 giftHandlerSelect.value = '';
             }
        }

        // Initial update of Area filter based on default/current Mandal
        updateAreaFilter();

        // Add event listeners to filters
        mandalFilter.addEventListener('change', updateAreaFilter); // Update Area and re-filter when Mandal changes
        areaFilter.addEventListener('change', filterPersonList); // Re-filter when Area changes
    }

     // Close modal when clicking outside (optional)
     window.addEventListener('click', function(event) {
         if (event.target === modalContainer) {
             hideModal();
         }
     });
}); 
document.addEventListener('DOMContentLoaded', function() {
    fetchProjects();
});

function fetchProjects(pageNumber = 1) {
    // Replace `/api/projects?page=${pageNumber}` with your actual API endpoint
    fetch(`/api/projects?page=${pageNumber}`)
        .then(response => response.json())
        .then(data => {
            displayProjects(data.projects);
            setupPagination(data.totalPages, pageNumber);
        })
        .catch(error => console.error('Error fetching projects:', error));
}

function displayProjects(projects) {
    const projectRows = document.getElementById('projectRows');
    projectRows.innerHTML = ''; // Clear existing rows

    projects.forEach(project => {
        const row = projectRows.insertRow();
        row.innerHTML = `
            <td>${project.name}</td>
            <td>${project.reason}</td>
            <td>${project.type}</td>
            <td>${project.division}</td>
            <td>${project.category}</td>
            <td>${project.priority}</td>
            <td>${project.department}</td>
            <td>${project.location}</td>
            <td>${project.status}</td>
            <td>
                <button onclick="updateStatus(${project.id}, 'Running')">Start</button>
                <button onclick="updateStatus(${project.id}, 'Closed')">Close</button>
                <button onclick="updateStatus(${project.id}, 'Cancelled')">Cancel</button>
            </td>
        `;
    });
}

function setupPagination(totalPages, currentPage) {
    const pagination = document.getElementById('pagination');
    pagination.innerHTML = ''; // Clear existing pagination buttons

    for (let i = 1; i <= totalPages; i++) {
        const button = document.createElement('button');
        button.textContent = i;
        if (i === currentPage) button.disabled = true;
        button.addEventListener('click', function() {
            fetchProjects(i);
        });
        pagination.appendChild(button);
    }
}

function updateStatus(projectId, newStatus) {
    // Implement the function to send an AJAX request to update the status
}

document.getElementById('addSquare').addEventListener('click', addSquare);
document.getElementById('applyFilter').addEventListener('click', applyFilter);

let squares = [];

function addSquare() {
    const squareContainer = document.getElementById('squareContainer');

    // Create a new square div
    const square = document.createElement('div');
    square.classList.add('square');

    // Random properties for the square
    const size = Math.floor(Math.random() * 100) + 50; // random size between 50 and 150px
    const step = Math.floor(Math.random() * 10) + 1; // random step
    const locationX = Math.floor(Math.random() * 500);
    const locationY = Math.floor(Math.random() * 500);
    const origin = `${locationX}, ${locationY}`;

    // Set the square properties
    square.style.width = size + 'px';
    square.style.height = size + 'px';
    square.style.transform = `translate(${locationX}px, ${locationY}px)`;

    // Add properties to the square for future filtering
    square.dataset.size = size;
    square.dataset.step = step;
    square.dataset.location = `${locationX}, ${locationY}`;
    square.dataset.origin = origin;

    // Display properties under the square
    const properties = document.createElement('div');
    properties.classList.add('property-list');
    properties.innerHTML = `
        <div>Size: ${size}px</div>
        <div>Step: ${step}</div>
        <div>Location: (${locationX}, ${locationY})</div>
        <div>Origin: ${origin}</div>
    `;

    square.appendChild(properties);
    squareContainer.appendChild(square);

    // Store square details
    squares.push({ square, size, step, location: `${locationX}, ${locationY}`, origin });
}

function applyFilter() {
    const filter = document.getElementById('filterProperty').value;

    squares.forEach(({ square, size, step, location, origin }) => {
        if (filter === 'all') {
            square.style.display = 'flex';
        } else if (filter === 'size' && size > 100) {
            square.style.display = 'flex';
        } else if (filter === 'location' && location.split(',')[0] > 200) {
            square.style.display = 'flex';
        } else if (filter === 'origin' && origin.includes('100')) {
            square.style.display = 'flex';
        } else {
            square.style.display = 'none';
        }
    });
}

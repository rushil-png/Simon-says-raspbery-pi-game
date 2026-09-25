function highlightButton(index) {
    const map = ['blue', 'red', 'yellow', 'green'];

    map.forEach(color => {
        document.getElementById(`btn-${color}`).classList.remove('lit');
    });

    if (index !== null) {
        document.getElementById(`btn-${map[index]}`).classList.add('lit');
    }
}

// Poll every 100ms for smooth effect
setInterval(() => {
    fetch('/current_light')
        .then(res => res.json())
        .then(data => {
            if (data.length > 0) {
                highlightButton(data[0]);
            } else {
                highlightButton(null);
            }
        });
}, 100);
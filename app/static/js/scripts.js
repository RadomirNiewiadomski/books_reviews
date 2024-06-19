function submitReview(bookId) {
    const content = document.getElementById('review-content').value;
    const rating = document.querySelector('input[name="rating"]:checked').value;

    fetch(`/book/${bookId}/add_review/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken'),
        },
        body: JSON.stringify({
            content: content,
            rating: rating,
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log('Response data:', data);
        if (data.success) {
            alert('Review added successfully!');
            // Dodajemy nową recenzję do listy bez przeładowania strony
            const reviewList = document.getElementById('review-list');
            const newReview = `
                <div class="card mb-2">
                    <div class="card-body">
                        <h5 class="card-title">${data.reviewer}</h5>
                        <p class="card-text">${content}</p>
                        <p class="card-text"><strong>Rating: ${rating}</strong></p>
                    </div>
                </div>
            `;
            reviewList.innerHTML += newReview;

            // Aktualizujemy średnią ocenę
            document.getElementById('average-rating').textContent = data.new_average_rating.toFixed(1);

            // Czyszczenie formularza po dodaniu recenzji
            document.getElementById('review-content').value = '';
            document.querySelector('input[name="rating"]:checked').checked = false;
        } else {
            alert(data.message);
        }
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

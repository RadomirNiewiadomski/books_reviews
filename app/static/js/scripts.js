function submitReview(bookId) {
    var rating = document.querySelector('input[name="rating"]:checked').value;
    var content = document.getElementById('review-content').value;
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    fetch(`/books/${bookId}/add_review/`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
        },
        body: JSON.stringify({
            rating: rating,
            content: content
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.success) {
            // Add the new review to the review list
            var reviewList = document.getElementById('review-list');
            var newReview = document.createElement('div');
            newReview.classList.add('card', 'mb-2');
            newReview.innerHTML = `
                <div class="card-body">
                    <h5 class="card-title">${data.reviewer}</h5>
                    <p class="card-text">${data.content}</p>
                    <p class="card-text"><strong>Rating: ${data.rating}</strong></p>
                </div>
            `;
            reviewList.appendChild(newReview);

            // Reset the review form
            document.getElementById('review-form').reset();
        } else {
            alert('An error occurred while adding your review.');
        }
    });
}

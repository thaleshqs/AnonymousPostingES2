const searchInput = document.getElementById('search_posts');
const noResultsMessage = document.getElementById('no-results');
const button = document.getElementById("search_button");

/*
button.addEventListener("click", function(event){
   performSearch();
});

searchInput.addEventListener('input', function (event) {
    if (event.key === 'Enter') {
        performSearch();
    }
});

function performSearch() {
    const searchQuery = searchInput.value.trim().toLowerCase();
	noResultsMessage.style.display = 'none';
	
	if (searchInput.value == null || searchInput.value === '') {
		noResultsMessage.style.display = 'block';
	}
    const posts = document.getElementsByClassName('post-text');

    

    let matchingPosts = false;
	for (const post of posts) {
		const postText = post.innerText.toLowerCase();
		if (postText.includes(searchQuery)) {
			post.parentElement.style.display = 'none';
			matchingPosts = true;
		} else {
			post.parentElement.style.display = 'none';
		}
	}
	
    if (!matchingPosts) {
        noResultsMessage.style.display = 'block';
    }
}
*/
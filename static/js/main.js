const searchInput = document.getElementById("searchInput");
const searchResults = document.getElementById("searchResults");

searchInput.addEventListener("input", async (event) => {
  const query = event.target.value.trim();
  if (query.length === 0) {
    searchResults.innerHTML = ""; // Clear search results if search input is empty
    return;
  }

  // Fetch search results from backend API
  const response = await fetch(`/api/v1/search?q=${query}`);
  const data = await response.json();

  // Clear previous search results
  searchResults.innerHTML = "";

  // Display search results
  data.forEach((result) => {
    const listItem = document.createElement("li");
    listItem.innerHTML = `${result.name_en} - (${result.name_kr}) - ${highlightMatch(result.description, query)}`;
    searchResults.appendChild(listItem);
  });
});

function highlightMatch(text, query) {
  const regex = new RegExp(`(${query})`, "gi");
  return text.replace(regex, '<span class="highlight">$1</span>');
}

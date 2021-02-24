var sql_query_login = "SELECT * \nFROM Users \nWHERE username = '{username}' AND Users.password = '{password}'"
var sql_query_search = "SELECT * \nFROM Product \nWHERE product_name LIKE '%{product}%';"


document.addEventListener("DOMContentLoaded", (event) => {});
$("#email").keyup(function () {
  updateLoginQuery();
});
$("#password").keyup(function () {
  updateLoginQuery();
});

function updateLoginQuery() {
  $("#sql-code").html(
    sql_query_login
    .replace("{username}", $("#email").val())
    .replace("{password}", $("#password").val())
  );
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightBlock(block);
  });
}

function updateSearchQuery() {
  $("#sql-code").html(
    sql_query_search.replace("{product}", $("#search-box").val())
  );
  document.querySelectorAll("pre code").forEach((block) => {
    hljs.highlightBlock(block);
  });
}
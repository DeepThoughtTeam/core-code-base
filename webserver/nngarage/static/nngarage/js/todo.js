function populateList() {
    $.get("/nngarage/get-tasks")
      .done(function(data) {
          var list = $("#tasks_table");
          // list.data('max-entry', data['max-entry']);
          list.html('')
          for (var i = 0; i < data.tasks.length; i++) {
              task = data.tasks[i];
              var new_task = $(task.html);
              // new_task.data("item-id", item.id);
              list.append(new_task);
          }
      });
}


function addItem(){
    var itemField = $("#item-field");
    $.post("/shared-todo-list/add-item", {item: itemField.val()})
      .done(function(data) {
          getUpdates();
          itemField.val("").focus();
      });
}


function deleteItem(e){
    var id = $(event.target).parent().data("item-id");
    $.post("/shared-todo-list/delete-item/" + id)
      .done(function(data) {
          getUpdates();
          $("#item-field").val("").focus()
      });
}


function getUpdates() {
    var list = $("#todo-list")
    var max_entry = list.data("max-entry")
    $.get("shared-todo-list/get-changes/"+ max_entry)
      .done(function(data) {
          list.data('max-entry', data['max-entry']);
          for (var i = 0; i < data.items.length; i++) {
              var item = data.items[i];
              if (item.deleted) {
                  $("#item_" + item.id).remove();
              } else {
                  var new_item = $(item.html);
                  new_item.data("item-id", item.id);
                  list.append(new_item);
              }
          }
      });
}

$(document).ready(function () {
  // Add event-handlers
  $("#add-btn").click(addItem);
  $("#item-field").keypress(function (e) { if (e.which == 13) addItem(); } );
  $("#todo-list").click(deleteItem);

  // Set up to-do list with initial DB items and DOM data
  populateList();
  //$("#item-field").focus();
  //
  //// Periodically refresh to-do list
  //window.setInterval(getUpdates, 5000);
  //
  //// CSRF set-up copied from Django docs
  //function getCookie(name) {
  //  var cookieValue = null;
  //  if (document.cookie && document.cookie != '') {
  //      var cookies = document.cookie.split(';');
  //      for (var i = 0; i < cookies.length; i++) {
  //          var cookie = jQuery.trim(cookies[i]);
  //          // Does this cookie string begin with the name we want?
  //          if (cookie.substring(0, name.length + 1) == (name + '=')) {
  //              cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
  //              break;
  //          }
  //      }
  //  }
  //  return cookieValue;
  //}
  //var csrftoken = getCookie('csrftoken');
  //$.ajaxSetup({
  //  beforeSend: function(xhr, settings) {
  //      xhr.setRequestHeader("X-CSRFToken", csrftoken);
  //  }
  //});
});

document.addEventListener('DOMContentLoaded', function() {
  
  
  document.querySelectorAll('.like_unlike_button').forEach(item => {
    item.addEventListener('click', (event)=>{
      let post_id = parseInt(event.target.id);
      let user_id = parseInt(document.querySelector('#user_id').innerHTML);
      let count_element = document.querySelector(`#total_likes_${post_id}`);
      let count_value = parseInt(count_element.innerHTML);
      
      //console.log(count);
      //console.log(event.target.id);
      if(event.target.innerHTML === '❤️'){
        event.target.innerHTML = '🤍';
        count_element.innerHTML = count_value - 1;
      }
      else{
        event.target.innerHTML = '❤️';
        count_element.innerHTML = count_value + 1;
      }
      fetch(`/posts/${post_id}`, {
        method: 'PUT',
        body: JSON.stringify({
            user_id: user_id
        })
      })
      .then(()=>console.log('success'))
      .catch(() => console.log('failed'));
    })
  })

  document.querySelectorAll('.edit-button').forEach(item => {
    item.addEventListener('click',(event)=>{
      
      let post_id = event.target.id.slice(1);
      //console.log(`trying to edit post ${post_id}`);
      let current_text = document.querySelector(`#post_content_${post_id}`).innerHTML.trim();
      //console.log(current_text);
      document.querySelector('#post-edit-textbox').value = current_text;
      document.querySelector('#original-post-id').value = post_id;
      $('#post-edit-modal').modal();
    })
  });

  document.querySelector('#post-edit-form').onsubmit = (event)=>{
    
    let post_id = document.querySelector('#original-post-id').value;
    let new_content = document.querySelector('#post-edit-textbox').value.trim();    
    console.log(`replacing ${post_id} with ${new_content}`);
    document.querySelector(`#post_content_${post_id}`).innerHTML = new_content;
    
    fetch(`/posts/${post_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          new_content: new_content
      })
    })
    .then(()=>console.log('success'))
    .catch(() => console.log('failed'));
  

    $('#post-edit-modal').modal('hide');
    event.preventDefault();
  }
});
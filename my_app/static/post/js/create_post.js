

function removeSection(id){
    $('#' + id).remove()
}

// generate unique seciton
function generateUniqueTextSection(id=null,tagType){
  if(id==null){
    id=generateUniqueId()
  }
  //generate variables
  if (tagType != '<img>'){
    var template = $('#text-template').html();
  }else{
    var template = $('#img-template').html();
  }
  var id = `${id}`
  var idTextareaContainter = `${id}-textarea-containter`;
  var idUserTextarea = `${id}-user-textarea`;
  var idHiddenInputsContainter = `${id}-hidden-inputs-containter`;
  var idIdInput = `${id}-id-input`;
  var idOrderInput = `${id}-order-input`;
  var idTextareaInput = `${id}-textarea-input`
  var tagInput = `${id}-tag-input`
  var imgContainer = `${id}-image-containter`
  var idImageInput= `${id}-image-input`
  var search = null;
  var replace = null;
  // in below list order is important for one kw not to replace another kw
  itemsToReplace = [
    [id,'primary-key'],
    [idTextareaContainter,'id-textarea-containter'],
    [idUserTextarea, 'id-user-textarea'],
    [idHiddenInputsContainter,'id-hidden-inputs-containter'],
    [idIdInput,'id-id-input'],
    [idOrderInput,'id-order-input'],
    [idTextareaInput,'id-textarea-input'],
    [tagType,'tag-type'],
    [tagInput, 'id-tag-input'],
    [imgContainer,'id-image-containter'],
    [idImageInput,'id-image-input'],
  ]
  // update html with correct id numbers and so son
  for(i = 0; i < itemsToReplace.length; i++){
    while(template.search(itemsToReplace[i][1]) > -1){
      search = itemsToReplace[i][1];
      replace = itemsToReplace[i][0];
      template = template.replace(search, replace);
    }
  }
  return template // retruns to addSection(),
}// generateUniqueSection end function

// move section up and down
function move(direction,id){
  // create list of all div wrappers
  var orderList = []
  $('.section').each(function(){
    orderList.push(this.id)
  });
  if(direction=='up'){
    // move up
    for(i=0; i<orderList.length;i++){
      if(orderList[i]==id  && i != 0){
        // change position
        $(('#'+id)).insertBefore('#'+orderList[i-1]);
      }
    }
  }else{
    //move down
    for(i=0; i<orderList.length;i++){
      if(orderList[i]==id && i+1 != orderList.length ){
        // change position
        $(('#'+id)).insertAfter('#'+orderList[i+1]);
      }
    }
  }
  updateSectionsOrder();
}

function generateUniqueId(){
  while(true){
        new_id = Math.ceil(Math.random() * 100000).toString()
      if (document.getElementById(new_id) == null && document.getElementById(new_id.toString()) == null){
        return new_id
      }else{
        continue;
      }
  }
}


// Adds entire new text sectino to the document
function addTextSection(after_div_id=null, tagType){
  id = generateUniqueId();
  template = generateUniqueTextSection(id,tagType)
  // check if this section will be inserted as last one or in the middle.
  if (after_div_id != null){after_div_id = '#' + after_div_id;}
  if( after_div_id == null ){
    $('#contentContainer').append(template)
  }else{
    $(after_div_id).before(template)
  }
  // show code options if relevant
  if(tagType=='<code>'){
    $('#'+id+'-select-code-type').show()
  }


  updateSectionsOrder();
}

//update hidden text area input every time user types sth new
function updateTextareaInput(sourceId, targetId, tagType=null){
  sectionId = sourceId.split('-')[0]
  text =$('#'+sourceId).val()
  // create ending divs form type input
  if(tagType != null){
    if(tagType=='<ul>'){
      //add <li> tag to evety line
      newText = '';
      textArray = text.split('\n');
      for(i=0; i<textArray.length; i++){
        tempText = '<li>' + textArray[i] + '</li>'
        newText = newText + tempText
      }
      text = newText
    }
    if(tagType=='<code>'){
      text = replaceItems(text, '\n', '&#10;');
      text = replaceItems(text, '<', '&lt;');
      text = replaceItems(text, '>', '&gt;');
    }

    // TAGOPEN
    if (tagType == '<code>'){
      codeType = $('#' + sectionId + '-select-code-type :selected').val()
      tagOpen = `<code class="language-${codeType}" style="white-space: pre-wrap;">`
    }else{
      tagOpen = tagType
    }
    // TAGCLOSE
    tagClose = tagType.replace('<','</')

    value = tagOpen + text + tagClose;
    // add <pre> tag if text is a code
    if (tagType == '<code>'){
      value = '<pre>' + value + '</pre>'

    }

    $('#'+targetId).show()
    $('#'+targetId).val(value)
  }else{
    alert(`Error, remove this seciton: ${after_div_id}`)
  }
}

function replaceItems(text, target, replacement){
  while(text.search(target)>-1){
    text = text.replace(target, replacement)
  }
  return text
}

// removes tags form PostSection.text
function removeTags(text, tag){
  // if it is list add new line sign \n
  text = replaceItems(text, '</li>','\n') // replave all </li> with \n
  text = replaceItems(text, '&#10;','\n') //  replace linebreaks

//  check if there is still opening bracket in text
  if(tag!='<code>'){
    while( text.search('<')>-1 ){
      open = text.search('<')
      close = text.search('>')+1
      text = text.slice(0,open)+text.slice(close, text.length)
    }
  }else{
    var iterator = 0;
    while( text.search('<')>-1 && iterator<2){
      iterator++;
      open = text.search('<')
      close = text.search('>')+1
      text = text.slice(0,open)+text.slice(close, text.length)
      if(iterator == 2){
        text = text.split("").reverse().join("");
        while(iterator<4){
          iterator++;
          open = text.search('>')
          close = text.search('<')+1
          text = text.slice(0,open)+text.slice(close, text.length)

        }
        text = text.split("").reverse().join("");
      }
    }
  }


  // while( text.search('&lt;')>-1){
  //   open = text.search('&lt;')+2
  //   close = text.search('&gt;')-2
  //   text = text.slice(0,open)+text.slice(close, text.length)
  // }
  return text
}

function updateSectionsOrder(){
  iterator = 0
  $('.input-order').each(function(){
    this.value = iterator;
    iterator ++;
  })
}

// MAIN LOOP
$(document).ready(function() {
  console.log('create_post.js initialized.');

  $('.user-text-input').each(function(){
    tag = this.onchange.toString().split(',')[2].split('\'')[1]
    text = removeTags($('#'+this.id).text(), tag);
    $('#'+this.id).text(text);
  })

  $('textarea').each(function () {
    this.setAttribute('style', 'height:' + (this.scrollHeight) + 'px;overflow-y:hidden;');
  }).on('input', function () {
    this.style.height = 'auto';
    this.style.height = (this.scrollHeight) + 'px';
  });

});

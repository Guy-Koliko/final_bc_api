//Book Constructor
function Book(title,author,isdn){
    this.title = title;
    this.author = author;
    this.isdn = isdn;
}
//UI Constructor 

function UI(){

}

//Add Book to list
UI.prototype.addBookToList = function(book){
    const list = document.getElementById('book-list')
    const row = document.createElement('tr')
    
    //insert col
    row.innerHTML = `
    
        <td>${book.title}</td>
        <td>${book.author}</td>
        <td>${book.isdn}</td>
        <td><a href="#" class="delete">x</a></td>


    `;
   
    //add to list 
    list.appendChild(row)
}

//clear field
UI.prototype.clearField = function(){
    document.getElementById('title').value = '';
    document.getElementById('author').value = '';
    document.getElementById('isdn').value = '';

}
//show Alert

UI.prototype.showAlert = function(message,classname){
    //Create div
    const div = document.createElement('div')
    //add className
    div.className = `alert ${classname}`
    //create text
    div.appendChild(document.createTextNode(message))

    //get parent
    const container = document.querySelector('.container')

    const form = document.querySelector('#book-form')

    //insert alert
    container.insertBefore(div,form)

    //disappear
    setTimeout(function(){
        document.querySelector('.alert').remove();
    },3000);

}

//UI remove 
UI.prototype.deleteBook = function(target){
    if(target.className ==='delete'){
        target.parentElement.parentElement.remove();
    }
}


//Add Book to LS
UI.prototype.addBookToLocalStorage = function(book){
    let books;
    if(localStorage.getItem('books') === null){
        books = []
    }else{
        books = JSON.parse(localStorage.getItem('books'))
    }
    books.push(book)
    localStorage.setItem('books',JSON.stringify(books))
}

//display Book from LS
UI.prototype.displayBookFromLS = function(book){

    const list = document.getElementById('book-list')
    const row = document.createElement('tr')
    
    //insert col
    row.innerHTML = `
    
        <td>${book.title}</td>
        <td>${book.author}</td>
        <td>${book.isdn}</td>
        <td><a href="#" class="delete">x</a></td>


    `;
   
    //add to list 
    list.appendChild(row)
}


//Get book List from LS
document.addEventListener('DOMContentLoaded',function(e){

    let books;
    if(localStorage.getItem('books') === null){
        books = []
    }else{
        books = JSON.parse(localStorage.getItem('books'))
    }
        // const ui = new UI()

      
    books.forEach(function(book){
        
        const ui = new UI()

        ui.displayBookFromLS(book)
    })
    
});
//Event Listener

document.getElementById('book-form').addEventListener('submit',
function(e){

    //get form values

    const title = document.getElementById('title').value,
    author = document.getElementById('author').value,
    isdn = document.getElementById('isdn').value;

    //Instantiating Book
    const book = new Book(title,author,isdn)

    //Add Book to List
    const ui = new UI()

    //validation
    if(title === '' || author === '' || isdn === ''){
       ui.showAlert('Please fill in all field','error')
    }else{

        ui.addBookToList(book)

        //Add to LS
        ui.addBookToLocalStorage(book)

        //sucess
        ui.showAlert('Book Added !','success')

        //clear input
        ui.clearField()

        //displayBook LS
        ui.displayBookFromLS()

    }
    ui.
    
    e.preventDefault()
});

UI.prototype.removLSBook = function(e){
    let books;
    if(localStorage.getItem('books') === null){
        books = []
    }else{
        books = JSON.parse(localStorage.getItem('books'))
    }
  
    if(e.parentElement.parentElement){
    // console.log(e.parentElement.previousElementSibling.textContent)

    books.forEach(function(book,index){
        if(book){
            // books.splice(index,1)
            console.log('Deleting',e.parentElement.parentElement)
            books.splice(index, 1);
          
        }
    });
    localStorage.setItem('books',JSON.stringify(books))
    

}

}

//Event Listener for delete

document.getElementById('book-list').addEventListener('click',function(e){

     const ui = new UI()

     ui.deleteBook(e.target);

     //remove from LS
     ui.removLSBook(e.target)

     //show alert
     ui.showAlert('Book Removed','success')


    e.preventDefault()
});

//submit the form to BC
document.getElementById('blocks-chain').addEventListener('submit',function(e){
    const ui = new UI()
    
 
    ui.submitToBC(e)


    e.preventDefault();
    
});

//BC submit
UI.prototype.submitToBC = function(block){
    let author = document.getElementById('author').value;
    let title = document.getElementById('title').value;
    let isdn = document.getElementById('isdn').value;
    
    if(block){
       
        
      
        let books;
        if(localStorage.getItem('books') === null){
            books = []
        }else{
            books = JSON.parse(localStorage.getItem('books'))
        }
        books.forEach(function(vote){

            author = vote.author
            title = vote.title
            isdn = vote.isdn
           
         console.log(author)
        });

       

        
    }
   


}

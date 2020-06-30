
console.log(`Logged in as ${user}`)

document.querySelector('#order-list').style.display = 'none'

document.querySelector('#order').onclick = () => {
  document.querySelector('#order-list').style.display = 'block'
  document.querySelector('#order').style.display = 'none'
  document.querySelector('.cross').onclick = () => {
    document.querySelector('#order-list').style.display = 'none'
    document.querySelector('#order').style.display = 'block'
  }
}

document.querySelectorAll('.cart-add').forEach(food => {

  food.onclick = () => {

    const foo = food.dataset.item
    const itemType = food.dataset.type

    console.log(`Clicked on ${itemType} of id ${foo}`)

  }
})

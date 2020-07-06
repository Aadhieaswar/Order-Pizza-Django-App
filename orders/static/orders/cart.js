
const form_select = document.querySelector('#select-items')
const warn = document.querySelector('#warn')

document.querySelector('#order-item').onclick = () => {
    if (form_select.value === 'default') {
        warn.style.display = 'block'
    } else {
        warn.style.display = 'none'
        form_select.disabled = true
    }

    if (form_select.value === 'Pizza') {
        document.querySelector('.pizza-options').style.display = 'block'
    } else if (form_select.value === 'Sub') {
        document.querySelector('.Sub-options').style.display = 'block'
    }
}

let popup = document.getElementById("address__order-popup");
let popupWindow = document.getElementById("address__popup-window");
let body = document.body

function openPopup() {
    popup.classList.add("order-popup-active");
    popupWindow.classList.add("popup-window-active");
    body.classList.add("none-scroll-body")
}

function closePopup(){
    popup.classList.remove("order-popup-active");
    popupWindow.classList.remove("popup-window-active");
}

window.onload = setTimeout(openPopup, 1000);
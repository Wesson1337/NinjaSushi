let orderPopup = document.getElementById("order-popup");
let orderPopupWindow = document.getElementById("order-popup__window");
let body = document.body

function openOrderPopup() {
    orderPopup.classList.add("order-popup-active");
    orderPopupWindow.classList.add("order-popup__window-active");
    body.classList.add("none-scroll-body")
}

function closeOrderPopup(){
    orderPopup.classList.remove("order-popup-active");
    orderPopupWindow.classList.remove("order-popup__window-active");
    body.classList.remove("none-scroll-body")
}

function openLoginPopup(){

}
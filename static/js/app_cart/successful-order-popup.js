let popup = document.getElementById("address__order-popup");
let popupWindow = document.getElementById("address__popup-window");

window.onload = function openPopup() {
    popup.classList.add("order-popup-active");
    popupWindow.classList.add("popup-window-active");
}

function closePopup(){
    popup.classList.remove("order-popup-active");
    popupWindow.classList.remove("popup-window-active");
}

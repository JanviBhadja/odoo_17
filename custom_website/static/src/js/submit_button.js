/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SubmitButton = publicWidget.Widget.extend({
    selector: '.submitButton',  
    events: {
        "click": "_onChangeButton",
    },

    start: function () {
        console.log("SubmitButton");
        return this._super.apply(this, arguments);
    },

    _onChangeButton: function (ev) {
        console.log("Button clicked");
        var button = ev.currentTarget;

        var email = document.querySelector('#email');  
        var password = document.querySelector('#password');  

        var emailValue = email.value;
        var passwordValue = password.value;

        var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

        if (!emailRegex.test(emailValue)) {
            alert("Please enter a valid email address.");
            email.focus();
            return;
        }

        if (passwordValue.trim() === "") {
            alert("Password cannot be empty.");
            password.focus();
            return;
        }

        if (button) {
            button.textContent = "Janvi";
            button.style.color = "yellow";
            button.style.backgroundColor = "green";
            console.log("Hello Good Morning");
        }
    },
});

export default publicWidget.registry.SubmitButton;

/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SubmitButton = publicWidget.Widget.extend({
    selector: '.submitButton',  
    events: {
        "click": "_onChangeButton",
    },

    start: function () {
        // console.log("SubmitButton widget initialized");
        return this._super.apply(this, arguments);
    },

    _onChangeButton: function (ev) {
        // console.log("Button clicked");
        var button = ev.currentTarget;

        if (button) {
            button.textContent = "Janvi";
            button.style.color = "yellow";
            button.style.backgroundColor = "green";
            // console.log("Button text and style changed");
        }
    },
});

export default publicWidget.registry.SubmitButton;

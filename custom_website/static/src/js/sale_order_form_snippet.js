/** @odoo-module **/

import publicWidget from "@web/legacy/js/public/public_widget";

publicWidget.registry.SaleOrderForm = publicWidget.Widget.extend({
    selector: '.sale_order_form_snippet',

    start: function () {
        console.log("sale Order");
        return this._super.apply(this, arguments);
    },
    

});

export default publicWidget.registry.SaleOrderForm;

/** @odoo-module */

import { Order } from "@point_of_sale/app/store/models" 
import { patch } from "@web/core/utils/patch";

patch(Order.prototype, {
    export_as_JSON(){
        const result = super.export_as_JSON(...arguments);
        result.note = this.getCustomerNote();
        return result;
    },

    getCustomerNote() {
        return this.note || "";
    },

    setCustomerNote(note) {
        this.note = note;
    },

});
/** @odoo-module */

import { OrderWidget } from "@point_of_sale/app/generic_components/order_widget/order_widget";

export class CustomOrderWidget extends OrderWidget {
    static template = 'point_of_sale.quantityAdded'; 

    static props = {
        ...OrderWidget.props, 
        productCount: { type: Number, optional: true },
    };

    setup() {
        super.setup();
        this.productCount = this._getProductCount();
    }

    get _getProductCount() {
        return this.pos.get_order().get_orderlines().length;
    }
}
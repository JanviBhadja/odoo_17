/* @odoo-module */

import publicWidget from "@web/legacy/js/public/public_widget";
import { jsonrpc } from "@web/core/network/rpc_service";

publicWidget.registry.saleOrderFormSnippet = publicWidget.Widget.extend({
    selector: '.sale-order-form-snippet',

    /**
     * @override
     */
    start: function () {
        this._super.apply(this, arguments);
        this._fetchSaleOrder();
        this._bindEvents();
    },

    _bindEvents: function () {
        this.$('.o_select_sale_order').on('change', this._sale_order_data.bind(this));
    },

    _fetchSaleOrder: async function () {
        const orders = await jsonrpc('/sale_order_snippet', {});
        const ordersContainer = this.el.querySelector('.o_select_sale_order');
        if (ordersContainer) {
            ordersContainer.innerHTML = '<option value="-1">Select order ........</option>' + orders.map(order => `<option value="${order.id}">${order.name}</option>`).join('');
        } else {
            console.error('Orders container not found.');
        }
    },

    _sale_order_data: function () {
        const ordersContainer = this.el.querySelector('.o_select_sale_order');
        const selectedValue = ordersContainer.value;

        console.log("Selected Order ID:", selectedValue);

        const orderDataShow = this.el.querySelector('.sale_order_data');
        if (orderDataShow) {
            if (selectedValue != -1) {
                orderDataShow.innerHTML = `<p>Selected Order ID: ${selectedValue}</p>`;
            } else {
                orderDataShow.innerHTML = `<p></p>`;
            }
        } else {
            console.error('Order data container not found.');
        }
    },
});

export default publicWidget.registry.saleOrderFormSnippet;

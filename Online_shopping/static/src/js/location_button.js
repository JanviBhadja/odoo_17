/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { Component, useState } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { CustomDroapDownPopup } from "@Online_shopping/js/custom_popup";

export class Location extends Component {
    static template = "point_of_sale.LocationButton";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
        this.orm = useService("orm");
        this.state = useState({ selectedLocation: _t("Location") });
    }

    async onLocationButton(){
        console.log("Hello Janvi!!!..")
        const selectedOrderline = this.pos.get_order().get_selected_orderline();
        const order = this.pos.get_order();
        if (!selectedOrderline) {
            return;
        }
        const locations = await this.orm.call('pos.order', 'get_location', ['true']);
        console.log(locations)
        const { confirmed, payload: input } = await this.popup.add(CustomDroapDownPopup, {
            // startingValue: selectedOrderline.get_customer_note(),
            title: _t("Add Location"),
            locations: locations, 
        });
        console.log('input',input)
        if (confirmed) {
            this.state.selectedLocation = input; 
        }
    }
}

ProductScreen.addControlButton({
    component: Location,
    position: ["after", "PosButton"],
});

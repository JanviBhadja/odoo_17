/** @odoo-module */

import { Component } from "@odoo/owl";
import { useService } from "@web/core/utils/hooks";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

export class Template extends Component {
    static template = "point_of_sale.Template";

    setup() {
        this.orm = useService("orm");
        this.pos = usePos();
    }

    async onButtonTemplate(){
        console.log("dfgserdfrfdgh");
    }
}

ProductScreen.addControlButton({
    component: Template,
    position: ["after", "PosButton"],
});

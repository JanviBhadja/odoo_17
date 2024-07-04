/** @odoo-module **/

import { registry } from "@web/core/registry";
import { TicketScreen } from "@point_of_sale/app/screens/ticket_screen/ticket_screen";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { useService } from "@web/core/utils/hooks";

class ProductOrdersScreen extends TicketScreen {
    static template = "Online_shopping.ProductOrdersScreen";
    setup() {
        super.setup();
        this.pos = usePos();
        this.orm = useService("orm");
    }
    back() {
        this.pos.showScreen('ProductScreen');
    }  
}
registry.category("pos_screens").add("ProductOrdersScreen", ProductOrdersScreen);

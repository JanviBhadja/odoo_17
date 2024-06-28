/** @odoo-module */

import { useService } from "@web/core/utils/hooks";
import { NumberPopup } from "@point_of_sale/app/utils/input_popups/number_popup";
import { ErrorPopup } from "@point_of_sale/app/errors/popups/error_popup";
import { Component } from "@odoo/owl";
import { _t } from "@web/core/l10n/translation";
import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";

export class Discount extends Component {
    static template = "point_of_sale.Discount";

    setup() {
        this.pos = usePos();
        this.popup = useService("popup");
    }

    async discountPopup(){
        const { confirmed, payload: note } = await this.popup.add(NumberPopup, {
            title: _t("Add Notes"),
            startingValue: 1,
        });
        return { confirmed, note };

    }

    async onButtonDiscount(){
        console.log("dfgshdh");
        // console.log(products)
        // console.log(this.pos.get_order())
        let status = true;
        while (status) {
            const products = this.pos.get_order().get_orderlines();
            if (!products.length) {
                return;
            }

            const {confirmed, note} =  await this.discountPopup();
            if (confirmed) {
                // console.log(note);
                const vals = Number(note)
                if (vals < 100 && vals > 0){
                    for (const orderline of products){
                        orderline.set_discount(vals);
                        console.log(note);
                    }
                    status = false;
                } else {
                    await this.popup.add(ErrorPopup, {
                        title: _t("Error Message"),
                        body: _t("Discount must be between 0 to 100."),
                    });
                }
            }
            else {
                break;
            }
        }
    }
}

ProductScreen.addControlButton({
    component: Discount,
    position: ["after", "AddNote"],
});
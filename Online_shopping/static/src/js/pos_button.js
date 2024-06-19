/** @odoo-module */

import { usePos } from "@point_of_sale/app/store/pos_hook";
import { ProductScreen } from "@point_of_sale/app/screens/product_screen/product_screen";
import { Component } from "@odoo/owl";

export class PosButton extends Component {
    static template = "point_of_sale.PosButton";

    setup() {
        this.pos = usePos();
    }

    async onClick(){
        console.log("dsrsrstrstrsstrs");
    }
}

ProductScreen.addControlButton({
    component: PosButton,
    position: ["after", "CustomerButton"],
});

// export class PosButton2 extends Component {
//     static template = "point_of_sale.PosButton2";

//     setup() {
//         this.pos = usePos();
//     }
    
//     async onClick(){
//         console.log("dsrsrstrstrsstrs");
//     }
// }

// ProductScreen.addControlButton({
//     component: PosButton2,
// });

// export class PosButton3 extends Component {
//     static template = "point_of_sale.PosButton3";

//     setup() {
//         this.pos = usePos();
//     }
    
//     async onClick(){
//         console.log("dsrsrstrstrsstrs");
//     }
// }

// ProductScreen.addControlButton({
//     component: PosButton3,
// });
/* @odoo-module */
import { FormController } from "@web/views/form/form_controller";
import { formView } from "@web/views/form/form_view";
import { ListController } from "@web/views/list/list_controller";
import { listView } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

class jsClassModelInfo extends FormController {
    actionInfoForm() {
                alert("Hi")
    }
}
jsClassModelInfo.template = "Online_shopping.modelInfoBtn";

export const modelInfoView = {
    ...formView,
    Controller: jsClassModelInfo,
};
registry.category("views").add("model_info", modelInfoView);

// class jsClassModelInfo extends FormController {
//     constructor() {
//         super(...arguments);
//         this.actionInfoForm = this.actionInfoForm.bind(this); // Bind the method to the class instance
//     }

//     async actionInfoForm(ev) {
//         alert("Hi");
//         try {
//             // Call Odoo RPC to trigger the server-side action for report generation
//             const result = await this._rpc({
//                 model: 'sale.order',
//                 method: 'generate_report',
//                 args: [[this.handle], {}], // Pass the selected record ID(s) if needed
//             });
//             // Handle the response if needed
//             console.log(result);
//         } catch (error) {
//             console.error("Error:", error);
//         }
//     }
// }

class jsClassModelListInfo extends ListController {
    actionNewButton() {
                alert("Hii Janvii")
    }
}
jsClassModelListInfo.template = "Online_shopping.NewButton";

export const modelInfoListView = {
    ...listView,
    Controller: jsClassModelListInfo,
};
registry.category("views").add("model_hr", modelInfoListView);

// class jsClassModelListInfo extends ListController {
//     actionNewButton() {
//                 alert("Hii Janvii")
//     }
// }
// jsClassModelSaleInfo.template = "Online_shopping.actionButton";

// export const modelInfoSaleView = {
//     ...listView,
//     Controller: jsClassModelSaleInfo,
// };
// registry.category("views").add("model_sale", modelInfoSaleView);

/* @odoo-module */
import { FormController } from "@web/views/form/form_controller";
// import { ListController } from "@web/views/list/list_controller";
import { formView as formViewForm } from "@web/views/form/form_view";
// import { formView as listViewList } from "@web/views/list/list_view";
import { registry } from "@web/core/registry";

class jsClassModelInfo extends FormController {
    actionInfoForm() {
                alert("Hi")
    }
}
// class jsClassListModelInfo extends ListController {
//     actionNewButton() {
//                 alert("Janvi")
//     }
// }
jsClassModelInfo.template = "Online_shopping.modelInfoBtn";
// jsClassListModelInfo.template = "hr_expence.NewButton";

export const modelInfoView = {
    formView : formViewForm,
    // listView : listViewList,
    Controller: jsClassModelInfo,
    // Controller: jsClassListModelInfo
};

registry.category("views").add("model_info", modelInfoView);
/* @odoo-module */
import { AbstractAwaitablePopup } from "@point_of_sale/app/popup/abstract_awaitable_popup";
import { _t } from "@web/core/l10n/translation";

export class CustomDroapDownPopup extends AbstractAwaitablePopup {
    static template = "Online_shopping.CustomDropDownPopup";
    static defaultProps = {
        closePopup: _t("Cancel"),
        confirmText: _t("Save"),
        title: _t("Customer Details"),
        locations: [],
    };
}
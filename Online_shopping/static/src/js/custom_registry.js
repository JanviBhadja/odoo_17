/** @odoo-module */

import { registry } from "@web/core/registry";
import { CustomOrderWidget } from "./quantity";

registry.category("widgets").add("CustomOrderWidget", CustomOrderWidget);

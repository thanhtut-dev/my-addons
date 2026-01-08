/** @odoo-module **/

import { ActionpadWidget } from "@point_of_sale/app/screens/product_screen/action_pad/action_pad";
import { patch } from "@web/core/utils/patch";

//Patching ActionpadWidget
patch(ActionpadWidget, {
    props: {
        ...ActionpadWidget.props,
        disable_refund_btn : { type: Boolean, optional: true },
    },
});
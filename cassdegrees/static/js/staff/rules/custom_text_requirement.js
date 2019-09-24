Vue.component('rule_custom_text_req', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("text")) {
                    value.text = "";
                }

                return true;
            }
        }
    },
    data: function() {
        return {
            "is_blank": false
        }
    },
    created: function() {
        this.check_options();
    },
    methods: {
        check_options: function() {
            this.is_blank = this.details.text === "";

            return !this.is_blank;
        },
        update_units: function() {
            // To be called whenever the unit count is updated. Will ask the OR rule to re-evaluate the unit count
            this.parent_count_units_fn();
            this.check_options();
        },
    },
    template: '#customTextReqRuleTemplate'
});

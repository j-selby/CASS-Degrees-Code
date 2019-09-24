Vue.component('rule_custom_text_req', {
    props: {
        "details": {
            type: Object,

            validator(value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("text")) {
                    value.text = "";
                }

                return true;
            }
        }
    },
    data() {
        return {
            "is_blank": false
        }
    },
    created() {
        this.check_options();
    },
    methods: {
        check_options() {
            this.is_blank = this.details.text === "";

            return !this.is_blank;
        },
        update_units() {
            // To be called whenever the unit count is updated. Will ask the OR rule to re-evaluate the unit count
            this.parent_count_units_fn();
            this.check_options();
        },
    },
    template: '#customTextReqRuleTemplate'
});

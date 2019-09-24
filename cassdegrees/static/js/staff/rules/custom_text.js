Vue.component('rule_custom_text', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("text")) {
                    value.text = "";
                }

                if (!value.hasOwnProperty("unit_count")) {
                    value.unit_count = "0";
                }

                if (!value.hasOwnProperty("show_course_boxes")) {
                    value.show_course_boxes = false;
                }

                return true;
            }
        }
    },
    data: function() {
        return {
            "not_divisible": false,
            "is_blank": false
        }
    },
    created: function() {
        this.check_options();
        // Keep a copy of the Or Rule's "count_units" function (Or a blank function if unavailable)
        this.parent_count_units_fn = this.$parent.get_or_rule_count_units_fn();
    },
    methods: {
        check_options: function() {
            this.is_blank = this.details.text === "";

            this.not_divisible = this.details.unit_count % 6 !== 0;

            return !this.not_divisible && !this.is_blank;
        },
        update_units: function() {
            // To be called whenever the unit count is updated. Will ask the OR rule to re-evaluate the unit count
            this.parent_count_units_fn();
            this.check_options();
        },
    },
    template: '#customTextRuleTemplate'
});

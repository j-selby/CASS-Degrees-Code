//! Vue.js based means of adding/removing rules. Excludes serialization (see programmanagement.js)

// Translation table between internal names for components and human readable ones.
const COMPONENT_NAMES = {
    'subplan': "Subplan",
    'custom_text': "Custom (Text)"
};

Vue.component('rule_subplan', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("ids")) {
                    value.ids = [-1];
                }

                return true;
            }
        }
    },
    data: function() {
        return {
            "subplans": [],
            // Verification message box
            "non_unique_options": false,

            "redraw": false
        }
    },
    created: function() {
        // Javascript has the best indirection...
        var rule = this;

        var request = new XMLHttpRequest();

        request.addEventListener("load", function() {
            rule.subplans = JSON.parse(request.response);
        });
        request.open("GET", "/api/model/subplan/?format=json");
        request.send();
    },
    methods: {
        add_subplan: function() {
            // Mutable modification - redraw needed
            this.details.ids.push(-1);
            this.do_redraw();
            this.check_options();
        },
        remove_subplan: function(index) {
            // Mutable modification - redraw needed
            this.details.ids.splice(index, 1);
            this.do_redraw();
            this.check_options();
        },
        // Verify that all options in the list are unique
        check_options: function() {
            var found = [];

            this.non_unique_options = false;

            for (var index in this.details.ids) {
                var value = this.details.ids[index];
                if (found.includes(value)) {
                    this.non_unique_options = true;
                    break;
                }
                found.push(value);
            }
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#subplanRuleTemplate'
});

Vue.component('rule_custom_text', {
    props: {
        "details": {
            type: Object,

            validator: function (value) {
                // Ensure that the object has all the attributes we need
                if (!value.hasOwnProperty("text")) {
                    value.text = "";
                }

                if (!value.hasOwnProperty("units")) {
                    value.units = 0;
                }

                return true;
            }
        }
    },
    computed: {
        // Checks to see if the unit count is divisible by 6
        not_divisible: function () {
          return this.details.units % 6 !== 0;
        }
    },
    template: '#customTextRuleTemplate'
});

// Handler for different Vue components, redirecting to the right component
Vue.component('rule', {
    props: {
        "details": {
            type: Object
        }
    },
    data: function() {
        return {
            component_names: COMPONENT_NAMES
        }
    },
    template: '#ruleTemplate'
});

// Contains a set of rules, with a button to add more
Vue.component('rule_container', {
    props: {
        "rules": {
            type: Array
        },
        // Message inserted between rules
        "separator": {
            type: String,
            default: ""
        }
    },
    data: function() {
        return {
            show_add_a_rule_modal: false,
            add_a_rule_modal_option: 'subplan',

            component_names: COMPONENT_NAMES,

            // Forces the element to re-render, if mutable events occurred
            redraw: false
        }
    },
    methods: {
        add_rule: function() {
            this.show_add_a_rule_modal = false;
            this.rules.push({
                type: this.add_a_rule_modal_option,
            });
            this.do_redraw();
        },
        remove: function(index) {
            this.rules.splice(index, 1);
            this.do_redraw();
        },
        // https://michaelnthiessen.com/force-re-render/
        do_redraw: function() {
            this.redraw = true;

            this.$nextTick(() => {
                this.redraw = false;
            });
        }
    },
    template: '#ruleContainerTemplate'
});

var app = new Vue({
    el: '#manualSerializedForm',
    data: {
        rules: []
    }
});
